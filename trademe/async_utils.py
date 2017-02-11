import asyncio


class AIter():

    def __init__(self, it):
        self._iter = it

    async def __anext__(self):
        try:
            return await next(self._iter)
        except StopIteration:
            raise StopAsyncIteration


class KeyedAIter():

    def __init__(self, it):
        self._iter = it

    async def __anext__(self):
        try:
            key, val = next(self._iter)
            return key, await val
        except StopIteration:
            raise StopAsyncIteration


class _MultiAsyncBlock():

    @asyncio.coroutine
    def __aenter__(self):
        return self

    @asyncio.coroutine
    def __aexit__(self, error, *a):
        if error:
            self.cancel()
        return (yield from self.__await__())

    def __iter__(self):
        return iter([])

    def __aiter__(self):
        return AIter(iter(self))

    def __await__(self):
        return (yield from asyncio.gather(*list(self)))


class MultiAsyncBlock(_MultiAsyncBlock):

    def __init__(self):
        self._futs = []

    def __iter__(self):
        return iter(self._futs)

    async def clear(self):
        futs = self.__await__()
        self._futs = []
        return await futs

    def clear_now(self):
        self._futs = []

    def add(self, fut):
        self._futs.append(asyncio.ensure_future(fut))


class KeyedMutliAsyncBlock(_MultiAsyncBlock):

    def __init__(self):
        self._futs = {}

    def __iter__(self):
        return iter(self._futs.items())

    def __aiter__(self):
        return KeyedAIter(iter(self))

    async def clear(self):
        futs = self.__await__()
        self._futs = {}
        return await futs

    def clear_now(self):
        self._futs = {}

    def add(self, key, fut):
        self._futs[key] = asyncio.ensure_future(fut)

    def __await__(self):
        return dict(zip(
            list(self._futs.keys()),
            (yield from asyncio.gather(*list(self._futs.values())))))
