import functools
import logging
import types


def partial(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return functools.partial(func, *args, **kwargs)
    setattr(func, '_f3_partial', True)
    return inner


def tap(func, data):
    func(data)
    return data


def pipe(func, data):
    return func(data)


def raise_if(value_or_func, ex, data):
    if callable(value_or_func):
        if value_or_func(data):
            raise ex
    elif value_or_func == data:
        raise ex

    return data


class Chain(object):
    def __init__(self, value=None):
        self._value = value

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    value = property(get_value, set_value)
    
    @classmethod
    def add_chain_function(cls, func, name=None):
        if not name:
            name = func.__name__

        # Curry if needed
        if not hasattr(func, '_f3_partial'):
            func = curry(func)

        # Wrap with the call adapter
        @functools.wraps(func)
        def call_wrapper(func):
            def inner(self, *args, **kwargs):
                logging.info(self)
                self.value = func(*args, **kwargs)(self.value)
                return self
            return inner

        func = call_wrapper(func)

        setattr(cls, name, func)

    @classmethod
    def add_chain_functions(cls, *funcs):
        for func in funcs:
            cls.add_chain_function(func)

# Add built-ins
Chain.add_chain_functions(
    tap,
    pipe,
    raise_if
)
