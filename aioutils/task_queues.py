import asyncio

from aioutils import asyncio_loop


class NoOpSemaphore():

    def __aenter__(self):
        pass

    def __aexit__(self, *a, **k):
        pass

    async def acquire():
        return True

    def locked():
        return False

    def release():
        pass


class TaskList():

    """
    A list of tasks that were started. Their completion can be waited on.
    """

    def __init__(self, *, raise_exceptions=True, squelch_cancels=True):
        self.task_list = []
        self.completed_tasks = []
        self.errored_tasks = []
        self.raise_exceptions = raise_exceptions
        self.squelch_cancels = squelch_cancels

    @asyncio.coroutine
    def __aenter__(self):
        return self

    @asyncio.coroutine
    def __aexit__(self, exc_type, exc_value, traceback):
        self.check_tasks()
        while self.task_list:
            tasks = tuple(self.task_list)
            if exc_type is not None:
                for task in tasks:
                    if not task.done():
                        task.cancel()
            yield from asyncio.wait(tasks)
            self.check_tasks()
        if exc_type is None:
            # Validate that we haven't finished a task that failed.
            self.check_exceptions()

    @property
    def all_tasks(self):
        return tuple(self.task_list + self.completed_tasks + self.errored_tasks)

    @asyncio_loop(loop_kwarg='loop')
    async def wait(self, *, loop, **kwargs):
        if not self.task_list and not self.errored_tasks:
            return tuple(self.completed_tasks), ()
        try:
            return await asyncio.wait(self.all_tasks, loop=loop, **kwargs)
        finally:
            self.check_tasks()

    @asyncio_loop(loop_kwarg='loop')
    async def gather(self, *, loop, **kwargs):
        try:
            return await asyncio.gather(self.all_tasks, loop=loop, **kwargs)
        finally:
            self.check_tasks()

    @asyncio_loop(loop_kwarg='loop')
    def as_completed(self, *, loop, **kwargs):
        try:
            # We are proxying the iterator that as_completed returns.
            # And wrapping it in a try/finally block.
            yield from asyncio.as_completed(self.all_tasks, loop=loop, **kwargs)
        finally:
            self.check_tasks()

    @asyncio_loop(loop_kwarg='loop')
    async def add_task(self, coro_or_future, *, loop):
        self._add_task(coro_or_future, loop=loop)

    def _add_task(self, coro_or_future, *, loop):
        self.check_exceptions()
        future = asyncio.ensure_future(coro_or_future, loop=loop)
        self.task_list.append(future)
        future.add_done_callback(self.task_complete)
        return future

    def check_exceptions(self, *, force_check=False):
        """Raises exceptions from tasks that errored."""
        if not self.raise_exceptions and not force_check:
            return
        self.check_tasks()
        while self.errored_tasks:
            err = self.errored_tasks.pop()
            self.completed_tasks.append(err)
            assert err.done()
            assert err.cancelled() or err.exception()
            if err.cancelled() and self.squelch_cancels:
                continue
            else:
                raise err.exception()

    def check_tasks(self):
        for item in list(self.task_list):
            if item.cancelled():
                self.task_list.remove(item)
                if self.squelch_cancels:
                    self.completed_tasks.append(item)
                else:
                    self.errored_tasks.append(item)
            elif item.done():
                self.task_list.remove(item)
                if item.exception():
                    self.errored_tasks.append(item)
                else:
                    self.completed_tasks.append(item)

    def task_complete(self, future):
        self.check_tasks()


class SizeBoundedTaskList(TaskList):

    def __init__(self, max_tasks, **kwargs):
        super().__init__(**kwargs)
        assert max_tasks > 0
        self.task_lock = asyncio.BoundedSemaphore(max_tasks)

    @asyncio_loop(loop_kwarg='loop')
    async def add_task(self, coro_or_future, *, loop):
        self.check_exceptions()
        await self.task_lock.acquire()
        try:
            self.check_exceptions()
            await super().add_task(coro_or_future, loop=loop)
        except:
            self.task_lock.release()

    def task_complete(self, future):
        self.task_lock.release()
        super().task_complete(future)


AsyncTaskTracker = SizeBoundedTaskList

#
# class RateLimitingTaskList(TaskList):
#
