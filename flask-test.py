import string
from random import randint, choice

from flask_unittest import ClientTestCase

from app import create_app


def random_int():
    return randint(234, 85098)


def random_string(length=20):
    return "".join([choice(string.ascii_letters) for c in range(length)])


class TestRoutes(ClientTestCase):
    # Assign the flask app object
    app = create_app()

    def test_dynamic_routes_with_client(self, client):
        # Use the client here
        # Example request to a route returning "hello world" (on a hypothetical app)
        s = random_string()
        x = random_int()
        for route in [
            ("/hello", "Hello there"),
            ("/hello/html", "This is html"),
            ("/", "Flask_next Index Page"),
            ("/login", "Login"),
            ("/test", "Farewell"),
            (f"/test/flong/{s}", s),
            (f"/test/integer/{x}", f"{x + 100}"),
            (f"/test/update/{x}", f"{x}"),
            (f"/test/update_things/{x}", f"{x}"),
        ]:
            rv = client.get(route[0])
            self.assertEqual(200, rv.status_code, route)
            self.assertIn(route[1], rv.data.decode("utf-8"))
