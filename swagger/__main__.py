import asyncio
import json
import re
from urllib.parse import urljoin

import aiohttp
import bs4
from bs4 import BeautifulSoup
import more_itertools



def iter_heading_contents(children):
    last_heading = None
    last_table = None
    last_paragraphs = []
    for child in children:
        if child.name in ['h1', 'h2', 'h3', 'h4']:
            if last_paragraphs or last_table or last_heading:
                yield last_heading, last_table, last_paragraphs
            last_heading = child
            last_paragraphs = []
        elif not child.name:
            if last_paragraphs is not None:
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
                print("Warning. Key already defined, ", key)
            else:
                orig[key] = value
    return orig


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


async def generate_swagger_from_docs(session, url):
    async with session.get(url) as o:
        soup = BeautifulSoup(await o.text(), 'lxml')
    with open('bs4-debug.html', 'w') as f:
        f.write(soup.prettify())
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
    definitions = {}
    response = None
    for heading, table, paragraphs in content_iter:
        if heading is None:
            metadata = parse_metadata(table)
            path['produces'] = convert_supported_formats_to_mime(
                metadata['Supported Formats'])
            path['description'] = paragraphs_to_markdown(*paragraphs)
            continue
        heading_text = text(heading)
        print(heading_text)
        if heading_text == 'URL parameters':
            params += parse_params('path', table)
        elif heading_text in ['POST Data', 'Returns']:
            name, desc = split_definition_paragraphs(paragraphs)
            dfn_obj = parse_type_format(name)
            dfn_ref = get_refname(dfn_obj)
            assert dfn_ref
            definitions = safe_add(definitions, parse_response(dfn_ref, desc, table))
            if heading_text == 'POST Data':
                params += [{
                    'in': 'body',
                    'schema': dfn_obj,
                }]
            elif heading_text == 'Returns':
                response = {
                    'description': desc,
                    "schema": dfn_obj,
                }
        elif heading_text in ['Request Builder', 'Request', 'Response']:
            break
        else:
            print(heading_text)
            raise Exception()

    data_tables = []
    description = None
    definition_name = None
    definition_description = []
    for child in content.children:
        if not child.name:
            continue
        elif len(data_tables) >= 4:
            break
        elif child.name == 'p':
            if description is None:
                description = text(child)
            elif definition_name is None:
                definition_name = text(child)
            else:
                definition_description.append(child)
        elif child.name == 'table':
            data_tables.append(child)
        elif child.find('table'):
            data_tables.append(child.find('table'))
        else:
            print('-', child.name, bool(child.find('table')),
                  (child.prettify() if child.name else ''))
    metadata = parse_metadata(data_tables[0])
    print(metadata)
    query_params = parse_params('query', data_tables[2])
    dfn_desc = text(*definition_description)

    params = [] + url_params + query_params
    path = {
        metadata['URL'].replace('https://api.trademe.co.nz/v1', ''): {
            metadata['HTTP Method'].lower(): {
                'description': description,
                'responses': {
                    '200': response
                },
            },
            'parameters': params,
        },
    }
    return ({
        metadata['URL'].replace('https://api.trademe.co.nz/v1', ''): {
            metadata['HTTP Method'].lower(): path
        }
    }, response)


def paragraphs_to_markdown(*paras, indent=0):
    paragraphs = []
    for item in paras:
        if item.name in ['ul', 'ol']:
            lst = []
            prefix = ' - ' if item.name == 'ul' else '1. '
            for li in item.children:
                if li.name == 'li':
                    lst.append(prefix + paragraphs_to_markdown(li, indent=indent + 3))
            paragraphs.append('\n'.join(lst))
        elif item.name is None or not (item.find('ul,ol')):
            paragraphs.append(text(item))
        else:
            paragraphs.append(paragraphs_to_markdown(*item.children, indent=indent))
    paragraphs = filter(lambda s: s.strip(), paragraphs)
    if indent != 0:
        new_paras = []
        i_chars = ' ' * indent
        for para in paragraphs:
            para = '\n'.join(i_chars + line for line in para.splitlines())
            new_paras.append(para)
        paragraphs = new_paras
    return '\n\n'.join(paragraphs)


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
            print("Unsupported format", fmt)
            raise Exception("Fmt")
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
            print("NOTKV", t, key, value, desc)
            raise Exception("not kv")
            continue
        data = parse_type_format(value)
        data['name'] = key
        data['description'] = desc
        if in_type:
            data['in'] = in_type
        if 'enum' in data:
            enum_row = next(table_iter)
            data = load_enum_into_item(enum_row, data)
        if '$ref' in data:
            print("Unsupported type", data['$ref'])
            raise Exception()
        params.append(data)
    return params


def get_refname(data):
    if '$ref' in data or '$ref' in data.get('items', []):
        return data.get('x-ref-name') or data['items']['x-ref-name']
    return None


def parse_response(definition_name, docs, table=None, *, table_iter=None):
    if table_iter is None:
        assert table is not None
        table_iter = iter(iter_parse_nested_table(table))
    else:
        assert table is None
    table_iter = more_itertools.peekable(table_iter)
    all_dfns = {}
    this_dfn = {}
    for t, key, value, desc in table_iter:
        if t != 'kv':
            print("NOTKV", t, key, value, desc)
            raise Exception("Not KV")
            continue
        data = parse_type_format(value)
        ref_name = get_refname(data)
        data['description'] = desc
        if 'enum' in data:
            enum_row = next(table_iter)
            data = load_enum_into_item(enum_row, data)
        elif ref_name:
            if table_iter.peek([None])[0] == 'nested':
                t, _, values, _ = next(table_iter)
                if values is not None:
                    resp = parse_response(ref_name, desc, table_iter=values)
                    all_dfns.update(resp)
        this_dfn[key] = data
    all_dfns[definition_name] = {
        'type': 'object',
        'properties': this_dfn,
    }
    return all_dfns


def load_enum_into_item(enum_row, data):
    t, _, values, _ = enum_row
    assert t == 'enum'
    _, has_value, _ = values[0]
    if has_value is None:
        data['enum'] = [k for k, _, _ in values]
        data['type'] = 'string'
        data['x-named-enum'] = [
            {
                'key': k,
                'value': k,
                'description': desc,
            }
            for k, _, desc in values
        ]
    else:
        data['enum'] = [v for _, v, _ in values]
        data['type'] = 'integer'
        data['format'] = 'int64'
        data['x-keyed-enum'] = [
            {
                'key': k,
                'value': v,
                'description': desc,
            }
            for k, v, desc in values
        ]
    return data


def parse_type_format(value):
    if value[0] == '<':
        ref = value[1:-1]
        return {
            '$ref': '#/definitions/' + ref,
            'x-ref-name': ref
        }
    if value.startswith('Collection of '):
        return {
            'type': 'array',
            'items': parse_type_format(value[len('Collection of '):]),
        }
    types = {
        'Integer': ('integer', 'int64'),
        'String': ('string', ''),
        'Number': ('number', 'double'),
        'DateTime': ('string', 'date-time'),
        'Boolean': ('boolean', ''),
    }
    if value.startswith('Long Integer'):
        v_type = 'Integer'
        extra = value[len('Long Integer'):]
    else:
        v_type, _, extra = value.partition(' ')
    if v_type == 'Enumeration':
        data = {
            'enum': True,
        }
    elif v_type == 'DateTime':
        data = {
            'type': 'string',
            'format': 'date-time',
            'x-tm-datetime': True,
        }
    elif v_type in types:
        t, f = types[v_type]
        data = {'type': t}
        if f:
            data['format'] = f
    else:
        print(value, repr(v_type))
        raise Exception("ssss")
    if extra == '(optional)':
        data['required'] = False
    elif extra == '(required)':
        data['required'] = False
    return data


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
            print("ROW:", row.prettify())
            print("TD", td.prettify())
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


async def iter_apis(session):
    url = 'https://developer.trademe.co.nz/api-reference/api-index/'
    async with session.get(url) as o:
        soup = BeautifulSoup(await o.text(), 'lxml')
    x = []
    for link in soup.select('div.generated-content a'):
        if 'href' in link.attrs:
            x.append(urljoin(url, link.attrs['href']))
    return x


async def main():
    paths = {}
    definitions = {}
    async with aiohttp.client.ClientSession() as session:
        await generate_swagger_from_docs(session, 'https://developer.trademe.co.nz/api-reference/branding-methods/adds-an-image-to-the-authenticated-users-list-of-branding-images/')
        for url in await iter_apis(session):
            print(url)
            p, d = await generate_swagger_from_docs(session, url)
            paths.update(p)
            definitions.update(d)

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
        'definitions': definitions,
    }

    with open('swagger.json', 'w') as f:
        json.dump(swagger, f, sort_keys=True, indent=2)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
