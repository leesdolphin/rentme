import asyncio
import functools


def asyncio_loop(fn=None, *, loop_kwarg='loop', possible_loop_args=None):
    def wrapper(fn):
        @functools.wraps(fn)
        def aiofn(*args, **kwargs):
            loop = asyncio.get_event_loop()
            for arg_name in possible_loop_args:
                if kwargs.get(arg_name, None) is not None:
                    loop = kwargs.pop(arg_name)
                    break
            kwargs[loop_kwarg] = loop
            return fn(*args, **kwargs)
        return aiofn

    if possible_loop_args is None:
        possible_loop_args = (loop_kwarg, )

    if fn is None:
        return wrapper
    else:
        return wrapper(fn)


def asyncio_loop_method(fn=None, *, loop_kwarg='loop', loop_attr='loop',
                        possible_loop_args=None):
    def wrapper(fn):
        @functools.wraps(fn)
        def aiofn(self, *args, **kwargs):
            loop = getattr(self, loop_attr, None)
            loop = loop or asyncio.get_event_loop()
            for arg_name in possible_loop_args:
                if kwargs.get(arg_name, None) is not None:
                    loop = kwargs.pop(arg_name)
                    break
            kwargs[loop_kwarg] = loop
            return fn(self, *args, **kwargs)
        return aiofn

    if possible_loop_args is None:
        possible_loop_args = (loop_kwarg, )

    if fn is None:
        return wrapper
    else:
        return wrapper(fn)
