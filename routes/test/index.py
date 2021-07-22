# /test

# /test
from flask import request


def index():
    return '<h1>Farewell</h1>'


# /test/flong/<flong_name>
def get_flong(flong_name='Default'):
    return f'<p>Flong {flong_name}</p>'


# /test/integer/<int:number>
def get_integer(number: int = 0):
    number += 100
    return f'<p>number = {number}</p>'


def get_put_update(item_id: int = None):
    return f'<p>update: {item_id}: {request.method}</p'


def get_put_update_things(item_id: int = None):
    return f'<p>update_things: {item_id}: {request.method}</p'

