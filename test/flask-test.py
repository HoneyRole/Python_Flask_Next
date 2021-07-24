import flask_unittest

from flask_app import create_app

class TestFoo(flast_unittest.ClientTestCase):
    # Assign the flask app object
    app = create_app()

    def test_foo_with_client(self, client):
        # Use the client here
        # Example request to a route returning "hello world" (on a hypothetical app)
        rv = client.get('/hello')
        self.assertInResponse(rv, 'hello world!')