import asyncio
from concurrent.futures import ThreadPoolExecutor
import functools

from celery import current_task
from celery.local import PromiseProxy
from celery.utils.log import get_task_logger
# from django.db import connections


logger = get_task_logger(__name__)


def asyncio_task(app, **kwargs):
    kwargs.setdefault('track_started', True)

    def wrapper(fn):
        task = app.task(**kwargs)(wrap_async_fn_in_new_event_loop(fn))
        return AsyncioPromiseProxy(task, fn, __doc__=fn.__doc__)

    return wrapper


def wrap_async_fn_in_new_event_loop(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        new_loop = asyncio.new_event_loop()
        with ThreadPoolExecutor(max_workers=2) as executor:
            new_loop.set_default_executor(executor)
            try:
                # asyncio.set_event_loop(new_loop)
                result = fn(*args, loop=new_loop, **kwargs)
                return new_loop.run_until_complete(result)
            finally:
                # Try and force all connections to close themselves.
                # connections.close_all()
                # for _ in range(executor._max_workers * 2):
                #     executor.submit(connections.close_all)
                # asyncio.set_event_loop(old_loop)
                ex = None
                if any(map(lambda task: not task.done(),
                           asyncio.Task.all_tasks(new_loop))):
                    ex = TypeError('Function did not clean up tasks.')
                new_loop.close()
                del new_loop
                if ex:
                    raise ex

    return wrapper


class AsyncioPromiseProxy(PromiseProxy):

    __slots__ = ('__original_fn')

    def __init__(self, proxy, original_fn, name=None, __doc__=None):
        super().__init__(lambda: proxy, (), {},
                         name=name, __doc__=__doc__)
        object.__setattr__(self, '_AsyncioPromiseProxy__original_fn', original_fn)

    def __call__(self, *a, **k):
        k.setdefault('loop', asyncio.get_event_loop())
        return self.__original_fn(*a, **k)


async def delay_or_call(fn, *a, **k):
    if current_task and current_task.request.id:
        # Dispatched onto a worker. Call delay
        fn.delay(*a, **k)
    else:
        return await fn(*a, **k)
