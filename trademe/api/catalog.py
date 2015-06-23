from trademe.api.tag import no_auth
import asyncio
__author__ = 'lee'


@no_auth
@asyncio.coroutine
def get_localities():
