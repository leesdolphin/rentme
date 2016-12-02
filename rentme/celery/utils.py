import asyncio
import time


def asyncio_task(fn=None):
    async def wrapper(*args, **kwargs):
        # Kill the old event loop and any tasks currently running.
        old_loop = asyncio.get_event_loop()
        while old_loop.is_running():
            old_loop.stop()
            time.sleep(0.5)
        old_loop.close()
        new_loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(new_loop)
            return new_loop.run_until_complete(fn(*args, **kwargs))
        finally:
            ex = None
            if any(map(lambda task: not task.done(),
                       asyncio.Task.all_tasks(new_loop))):
                ex = TypeError("Function did not clean up tasks.")
            new_loop.close()
            del new_loop
            if ex:
                raise ex

    return wrapper
