from functools import wraps


def call_once(function):
    called = False
    return_value = None

    @wraps(function)
    def wrap(*args, **kwargs):
        nonlocal called
        nonlocal return_value
        if not called:
            return_value = function(*args, **kwargs)
            called = True
        return return_value

    return wrap
