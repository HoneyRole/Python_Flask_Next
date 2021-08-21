from functools import wraps
from typing import Any, Callable

from flask import request, abort, Response


def get_request_value(arg_name:str, arg_type: Any = str, arg_default: Any = None) -> Any:
    """
    get a form or arg value from a Flask request object
    """
    arg_value = request.form.get(arg_name) or request.args.get(arg_name) or arg_default
    if arg_value is not None:
        try:
            arg_value = arg_type(arg_value)
        except Exception as e:
            abort(
                Response(
                    f"""Required argument failed type conversion: {arg_name}, {str(e)}""",
                    status=400,
                )
            )
    return arg_value


def request_arg(arg_name: str, arg_type: Any = str, arg_default=None) -> Callable:
    """
    decorator to auto convert arg or form fields to
    named method parameters with the correct type
    conversion

        @route('/something/<greeting>/')
        @request_arg('repeat', int, 1)
        def route_something(greeting='', repeat):
            return greeting * repeat

        # /something/yo/?repeat=10

        # yoyoyoyoyoyoyoyoyoyo

    :param arg_name: name of the form field or arg
    :param arg_type: (optional) the type to convert to
    :param arg_default: (optional) a default value.  Use '' or 0 when allowing optional fields
    :return: a decorator
    """

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            value = get_request_value(arg_name, arg_type, arg_default)
            if value is None:
                abort(Response(f"""Required argument missing: {arg_name}""", status=400))

            kwargs[arg_name] = value
            return f(*args, **kwargs)

        return decorated

    return decorator
