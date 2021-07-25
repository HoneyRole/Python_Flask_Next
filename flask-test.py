from flask_unittest import ClientTestCase
from app import create_app


class TestFoo(ClientTestCase):
    # Assign the flask app object
    app = create_app()

    def test_dynamic_routes_with_client(self, client):
        # Use the client here
        # Example request to a route returning "hello world" (on a hypothetical app)
        for route in [
            "/hello",
            "/hello/html",
            "/",
            "/login",
            "/test",
            "/test/flong/andrew",
            "/test/integer/200",
            "/test/update/100",
            "/test/update_things/100",
        ]:
            rv = client.get(route)
            self.assertEqual(200, rv.status_code, route)
