import asyncio
import json
from pprint import pprint as pp
import re
from urllib.parse import urljoin

import aioutils.aiohttp
import aiohttp
import bs4
from bs4 import BeautifulSoup
import more_itertools

from aioutils.task_queues import SizeBoundedTaskList
from .parse_types import load_enum_into_item, parse_type_format


class TypesEncoder(json.JSONEncoder):

    def default(self, o):
        if hasattr(o, 'items'):
            return dict(o)
        else:
            super().default(o)


error_definitions = {
    'ErrorResult': {
        'type': 'object',
        'properties': {
            'Request': {'type': 'string'},
            'ErrorDescription': {'type': 'string'},
            'Error': {'$ref': '#/definitions/Error'},
        },
    },
    'Error': {
        'type': 'object',
        'properties': {
            'Code': {'type': 'string'},
            'UserDescription': {'type': 'string'},
            'DeveloperDescription': {'type': 'string'},
            'ErrorData': {
                'type': 'array',
                'items': {'$ref': '#/definitions/ErrorDataItem'},
            },
        },
    },
    'ErrorDataItem': {
        'type': 'object',
        'properties': {
            'Name': {'type': 'string'},
            'Value': {'type': 'string'},
        },
    },
}

standard_responses = {
    '304': {
        'description': 'Used with caching to indicate that the cached copy is'
                       ' still valid.'
    },
    '400': {
        'description': 'The request is believed to be invalid in some way. The'
                       ' response body will contain an error message. You'
                       ' should display the error message to the user.',
        'schema': {'type': 'object', '$ref': '#/definitions/ErrorResult'},
    },
    '401': {
        'description': 'An OAuth authentication failure occurred. You should'
                       ' ask the user to log in again.',
        'schema': {'type': 'object', '$ref': '#/definitions/ErrorResult'},
    },
    '429': {
        'description': 'Your rate limit has been exceeded. Your rate limit'
                       ' will reset at the start of the next hour. You should'
                       ' not attempt to make any more calls until then.',
        'schema': {'type': 'object', '$ref': '#/definitions/ErrorResult'},
    },
    '500': {
        'description': 'A server error occurred. You should display a generic'
                       ' “whoops” error message to the user.',
        'schema': {'type': 'object', '$ref': '#/definitions/ErrorResult'},
    },
    '503': {
        'description': 'Planned server maintenance is underway. General error'
                       ' details and auction extension details are provided in'
                       ' the response. You should consume this information to'
                       ' inform the end user.',
        'schema': {'type': 'object', '$ref': '#/definitions/ErrorResult'},
    },
}


class DefinitionContainer():

    def __init__(self):
        self.definitions = {}
        self.reverse = {}

    def add_definition(self, prefered_name, definition):
        if not prefered_name.isidentifier():
            print("Invalid identifier {!r}".format(prefered_name))
        rev_lookup = json.dumps(definition, indent=2, sort_keys=True, cls=TypesEncoder)
        rev_names = self.reverse.setdefault(rev_lookup, [])
        if prefered_name in rev_names:
            return prefered_name
        elif prefered_name not in self.definitions:
            self.reverse[rev_lookup].append(prefered_name)
            self.definitions[prefered_name] = definition
            return prefered_name
        print("could not create definition with prefered name {!r}. Clashes with {!r}".format(prefered_name, rev_names))
        attempts = 0
        while attempts < 10:
            new_name = prefered_name + str(attempts)
            if new_name in rev_names:
                return new_name
            elif new_name not in self.definitions:
                self.reverse[rev_lookup].append(new_name)
                self.definitions[new_name] = definition
                return new_name
            attempts += 1
        raise Exception('Failed to generate unique name for'
                        ' model {}.{}'.format(prefered_name))


def iter_heading_contents(children):
    heading_tags = frozenset({'h1', 'h2', 'h3', 'h4'})
    last_heading = None
    last_table = None
    last_paragraphs = []
    expanded_children = []
    is_private = False
    for child in children:
        if child.name == 'div':
            div_children = child.contents
            child_tag_names = {c.name for c in div_children}
            if heading_tags & child_tag_names:
                expanded_children += div_children
        else:
            expanded_children.append(child)
    for child in expanded_children:
        if child.name in heading_tags:
            if last_paragraphs or last_table or last_heading:
                yield last_heading, last_table, last_paragraphs
            last_heading = child
            last_paragraphs = []
            is_private = False
        elif is_private or '[/tm_private]' in text(child):
            is_private = True
        elif not child.name:
            last_paragraphs.append(child)
        elif child.name == 'table':
            last_table = child
        elif child.find('table'):
            last_table = child.find('table')
        else:
            last_paragraphs.append(child)
    if last_paragraphs or last_table or last_heading:
        yield last_heading, last_table, last_paragraphs


def safe_add(orig, *new):
    orig = dict(orig)
    for new_dict in new:
        for key, value in dict(new_dict).items():
            if key in orig:
                if value != orig[key]:
                    print('Warning. Key already defined, ', key)
                    # from pprint import pformat
                    # import difflib
                    # print(''.join(difflib.ndiff(
                    #     pformat(orig[key]).splitlines(keepends=True),
                    #     pformat(value).splitlines(keepends=True),
                    # )))
            else:
                orig[key] = value
    return orig


def definition_union(orig, *new):
    out = dict(orig)
    for new_dict in new:
        for key, value in dict(new_dict).items():
            if key not in out:
                out[key] = value
            else:
                new_props = value['properties']
                out_props = out[key]['properties']
                out_props.update(new_props)
    return out


def split_definition_paragraphs(paragraphs):
    paragraphs = iter(paragraphs)
    def_line = None
    lines = []
    for para in paragraphs:
        if def_line is None:
            ptext = text(para)
            if ptext:
                def_line = ptext
        else:
            lines.append(para)
    assert def_line
    return def_line, paragraphs_to_markdown(*lines)


def paragraphs_to_markdown(*paras, indent=0):
    paragraphs = []
    for item in paras:
        if item.name in ['ul', 'ol']:
            lst = []
            prefix = ' - ' if item.name == 'ul' else '1. '
            for li in item.children:
                if li.name == 'li':
                    lst.append(prefix + paragraphs_to_markdown(
                        li, indent=indent + 3))
            paragraphs.append('\n'.join(lst))
        elif item.name is None or not (item.find('ul,ol')):
            paragraphs.append(text(item))
        else:
            paragraphs.append(paragraphs_to_markdown(
                *item.children, indent=indent))
    paragraphs = filter(lambda s: s.strip(), paragraphs)
    if indent != 0:
        new_paras = []
        i_chars = ' ' * indent
        for para in paragraphs:
            para = '\n'.join(i_chars + line for line in para.splitlines())
            new_paras.append(para)
        paragraphs = new_paras
    return '\n\n'.join(paragraphs)


def text(*elms, one_line=True, strip=True, sep=' '):
    text_elms = []
    for elm in elms:
        if elm.name is None:
            child_elms = [elm]
        else:
            child_elms = elm.children
        for e in child_elms:
            if isinstance(e, bs4.NavigableString):
                txt = str(e)
                txt = re.sub(r'[ \n\t]+', ' ', txt)
                text_elms.append(txt)
            elif e.name == 'br':
                text_elms.append(' ' if one_line else '\n')
            elif e.name not in ['script', 'style']:
                text_elms.append(text(e, one_line=one_line, strip=False))
        text_elms.append(sep)
    t = ''.join(text_elms)
    t = re.sub(r'[ ]+', ' ', t)
    if not one_line:
        t = re.sub(r'[ ]*\n[ ]*', '\n', t)
    if strip:
        t = t.strip()
    return t


async def generate_swagger_from_docs(session, url, definitions):
    KNOWN_BAD_HEADINGS = {
        'Request Builder',
        'Request',
        'Response',
        'Examples',
        'Example XML Request (switch to JSON)',
        'Example JSON Request (switch to XML)',
        'Example XML Response (switch to JSON)',
        'Example JSON Response (switch to XML)',
    }
    soup = None
    while soup is None:
        try:
            async with session.get(url) as o:
                soup = BeautifulSoup(await o.text(), 'lxml')
        except aiohttp.ServerDisconnectedError:
            soup = None
            print('Server disconnect for', url)
            continue
    u = url.replace('https://developer.trademe.co.nz/api-reference/api-index/', '').replace('/', '-')
    content = soup.select('div.generated-content', limit=1)[0]
    content_iter = iter(iter_heading_contents(content.children))
    path = {
        'externalDocs': {
            'description': 'Original TradeMe Documentation',
            'url': url
        },
    }
    params = []
    metadata = None
    response = None
    for heading, table, paragraphs in content_iter:
        if heading is None:
            metadata = parse_metadata(table)
            path['produces'] = convert_supported_formats_to_mime(
                metadata['Supported Formats'])
            path['description'] = paragraphs_to_markdown(*paragraphs)
            continue
        heading_text = text(heading)
        if heading_text in ['URL parameters', 'Query String parameters']:
            if heading_text == 'URL parameters':
                in_type = 'path'
            elif heading_text == 'Query String parameters':
                in_type = 'query'
            else:
                raise Exception('Unkown Heading')
            params += parse_params(in_type, table)
        elif heading_text in ['POST Data', 'Returns']:
            name, desc = split_definition_paragraphs(paragraphs)
            dfn_obj = parse_type_format(name)
            dfn_ref = get_refname(dfn_obj)
            if dfn_ref:
                dfn_obj = parse_response(dfn_obj, desc, definitions, table=table)
            else:
                dfn_obj['description'] = desc
            if heading_text == 'POST Data':
                params += [{
                    'in': 'body',
                    'schema': dfn_obj,
                }]
            elif heading_text == 'Returns':
                response = {
                    'description': desc,
                    'schema': dfn_obj,
                }
            else:
                raise Exception('Unkown Heading')

        elif heading_text in KNOWN_BAD_HEADINGS:
            continue
        else:
            print(heading_text)
            raise Exception()
    path['responses'] = safe_add({
        '200': response,
    }, standard_responses)
    return {
        metadata['URL'].replace('https://api.trademe.co.nz/v1', ''): {
            metadata['HTTP Method'].lower(): path,
            'parameters': params,
        }
    }


def convert_supported_formats_to_mime(supported_formats):
    formats = map(str.strip, supported_formats.split(','))
    format_mapping = {
        'JSON': 'application/json',
        'XML': 'text/xml'
    }
    mime_types = []
    for fmt in formats:
        if fmt in format_mapping:
            mime_types.append(format_mapping[fmt])
        elif fmt.upper() in format_mapping:
            mime_types.append(format_mapping[fmt.upper()])
        else:
            print('Unsupported format', fmt)
            raise Exception('Fmt')
    return mime_types


def parse_metadata(table):
    data = {}
    for row in table.find_all('tr'):
        key = text(row.find('th'))
        value = text(row.find('td'))
        if key.endswith('?'):
            value = (value == 'Yes')
        key = key[:-1]
        data[key] = value
    return data


def parse_params(in_type, table):
    table_iter = iter(iter_parse_nested_table(table))
    params = []
    for t, key, value, desc in table_iter:
        if t != 'kv':
            print('NOTKV', t, key, value, desc)
            raise Exception('not kv')
        data = parse_type_format(value)
        data['name'] = key
        data['description'] = desc
        if in_type:
            data['in'] = in_type
        if 'enum' in data:
            enum_row = next(table_iter)
            data = load_enum_into_item(enum_row, data)
        if '$ref' in data:
            print('Unsupported type', data['$ref'])
            raise Exception()
        params.append(data)
    return params


def get_refname(data):
    try:
        return data.ref_name
    except AttributeError:
        return None


def parse_response(dfn_obj, docs, definitions, *, table=None, table_iter=None):
    if table_iter is None:
        assert table is not None
        table_iter = iter(iter_parse_nested_table(table))
    else:
        assert table is None
    table_iter = more_itertools.peekable(table_iter)
    this_dfn = {}
    for t, key, value, desc in table_iter:
        if t != 'kv':
            print('NOTKV', t, key, value, desc)
            print(this_dfn)
            raise Exception('Not KV')
            continue
        data = parse_type_format(value)
        ref_name = get_refname(data)
        data['description'] = desc
        if 'enum' in data:
            enum_row = next(table_iter)
            data = load_enum_into_item(enum_row, data)
        if 'enum' in data.get('items', []):
            enum_row = next(table_iter)
            data['items'] = load_enum_into_item(enum_row, data['items'])
        elif ref_name:
            if table_iter.peek([None])[0] == 'nested':
                t, _, values, _ = next(table_iter)
                if values is not None:
                    data = parse_response(data, desc, definitions, table_iter=values)
            else:
                print('xx', table_iter.peek([None]))
        this_dfn[key] = data
    dfn_obj.ref_name = definitions.add_definition(get_refname(dfn_obj), {
        'type': 'object',
        'properties': this_dfn,
    })
    return dfn_obj


def iter_parse_nested_table(table):
    for row in filter(lambda e: e.name == 'tr', table.children):
        td = row.find('td')
        next_td = td.find_next_sibling('td') if td else None
        if not next_td:
            if td.find('table'):
                yield ('nested', None,
                       iter_parse_nested_table(td.find('table')), None)
            else:
                assert text(td) == '(This type has already been defined)'
                yield ('nested', None, None, None)
        elif 'colspan' in next_td.attrs:
            yield ('enum', None, parse_enum_table(next_td.find('table')), None)
        elif row.find('th'):
            key = text(row.find('th'))
            value = text(td)
            description = text(next_td)
            yield ('kv', key, value, description)
        else:
            print('ROW:', row.prettify())
            print('TD', td.prettify())
            raise Exception()


def parse_enum_table(table):
    return list(iter_parse_enum_table(table))


def iter_parse_enum_table(table):
    enum_values = set()
    for row in table.find_all('tr'):
        tds = row.find_all('td')
        if len(tds) == 2:
            name = text(tds[0])
            value = None
            description = text(tds[1])
            ev = name
        elif len(tds) == 3:
            name = text(tds[0])
            value = text(tds[1])
            description = text(tds[2])
            ev = value
        else:
            print(row)
            continue
        if ev not in enum_values:
            enum_values.add(ev)
            yield (name, value, description)


async def iter_api_index(session):
    url = 'https://developer.trademe.co.nz/api-reference/api-index/'
    async with session.get(url) as o:
        soup = BeautifulSoup(await o.text(), 'lxml')
    x = []
    for item in soup.select('.content tr'):
        if '(deprecated)' in text(item):
            continue
        link = item.find('a')
        print(link, link and 'href' in link.attrs)
        if link and 'href' in link.attrs:
            href = urljoin(url, link.attrs['href'])
            if '/api-reference/' in href:
                x.append(href)
    return x


async def iter_api_methods_page(session, url):
    if not url.startswith('http'):
        url = 'https://developer.trademe.co.nz/api-reference/' + url + '/'
    async with session.get(url) as o:
        soup = BeautifulSoup(await o.text(), 'lxml')
    x = []
    for item in soup.select('div.generated-content li'):
        if '(deprecated)' in text(item):
            continue
        link = item.find('a')
        print(link, link and 'href' in link.attrs)
        if link and 'href' in link.attrs:
            href = urljoin(url, link.attrs['href'])
            if '/api-reference/' in href:
                x.append(href)
    return x


async def main():
    paths = {}
    definitions = DefinitionContainer()
    async with aioutils.aiohttp.CachingClientSession(
        cache_strategy=aioutils.aiohttp.OnDiskCachingStrategy(
            cache_folder='./.cache')
    ) as session:
        urls = await iter_api_index(session)
        # Set your own definition pages here.

        urls = sorted(set(urls))
        async with SizeBoundedTaskList(1) as tl:
            for url in urls:
                print(url)
                await generate_swagger_from_docs(
                    session,
                    url,
                    definitions
                )
            for doc_task in tl.as_completed():
                gen_path = await doc_task
                # TODO: union paths taking into account the http method and url.
                paths = safe_add(paths, gen_path)

    swagger = {
        'swagger': '2.0',
        'info': {
            'title': 'TradeMe API',
            'version': '0.0',
        },
        'schemes': ['https'],
        'host': 'api.trademe.co.nz',
        'basePath': '/v1/',
        'paths': paths,
        'definitions': definitions.definitions,
    }

    with open('swagger.json', 'w') as f:
        json.dump(swagger, f, sort_keys=True, indent=2, cls=TypesEncoder)
    with open('swagger.json') as f:
        names = set()
        for line in f:
            if '#/definitions/' in line:
                pos = line.index('#/definitions/') + len('#/definitions/')
                name = line[pos:-3]
                names.add(name)
        for name in sorted(names):
            if name not in definitions.definitions:
                print(name)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
