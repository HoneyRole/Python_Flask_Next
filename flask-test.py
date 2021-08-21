import os
import string
from random import randint, choices

from flask_unittest import ClientTestCase

from app import create_app

random_ints = {}


def random_int(item_id=0):
    if item_id in random_ints:
        return random_ints[item_id]
    random_ints[item_id] = randint(234, 85098)
    return random_ints[item_id]


random_strings = {}


def random_string(item_id=1):
    if item_id in random_strings:
        return random_strings[item_id]
    random_strings[item_id] = "".join(choices(string.ascii_letters, k=20))
    return random_strings[item_id]


class TestRoutes(ClientTestCase):
    # Assign the flask app object

    app = create_app("./routes")
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'Testing'
    app.config['WTF_CSRF_ENABLED'] = False

    def test_dynamic_routes_with_client(self, client):
        # Use the client here
        # Example request to a route returning "hello world" (on a hypothetical app)
        for route in [
            ("/hello", "Hello there"),
            ("/hello/html", "This is html"),
            ("/", """<div id="jsx_content"></div>"""),
            ("/test", "Farewell"),
            (f"/test/flong/{random_string(1)}", random_string(1)),
            (f"/test/integer/{random_int(2)}", f"{random_int(2) + 100}"),
            (f"/test/update/{random_int(3)}", f"{random_int(3)}"),
            (f"/test/update_things/{random_int(4)}", f"{random_int(4)}"),
        ]:
            rv = client.get(route[0])
            self.assertEqual(200, rv.status_code, route)
            self.assertIn(route[1], rv.data.decode("utf-8"), route[0])
