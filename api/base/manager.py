import warnings

from aioutils import asyncio_loop

from api.base.endpoint import BaseEndpoint


class APIManagerBase:

    class Endpoints:
        pass

    @asyncio_loop
    def __init__(self, http_requester, *args, loop, **kwargs):
        super().__init__()
        self.http_requester = http_requester
        endpoints = {}
        for cls in reversed(self.__class__.mro()):
            if hasattr(cls, 'Endpoints'):
                for attr, val in cls.Endpoints.__dict__.items():
                    if len(attr) <= 1 or attr[0] == '_' or attr[-1] == '_':
                        continue
                    elif issubclass(val, APIManagerBase) or \
                            issubclass(val, BaseEndpoint):
                        endpoints[attr] = val
                    else:
                        warnings.warn(('{}.Endpoints.{} is not a supported'
                                       ' value. Check that you are listing the'
                                       ' class, and not constructing it.')
                                      .format(cls.__qualname__, attr))
        for endpoint, endpoint_cls in endpoints.items():
            endpoint_instance = endpoint_cls(
                *args,
                **kwargs,
                http_requester=http_requester,
                loop=loop
            )
            setattr(self, endpoint, endpoint_instance)

    def __enter__(self):
        self.http_requester.__enter__()
        return self

    def __exit__(self, *a):
        self.http_requester.__exit__(*a)

    async def __aenter__(self):
        await self.http_requester.__aenter__()
        return self

    async def __aexit__(self, *a):
        await self.http_requester.__aexit__(*a)
