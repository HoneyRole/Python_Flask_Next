from flask import g
from flask_login import current_user

from flask_next.d_serialize import d_serialize


def get_g_json():
    g.authenticated = current_user.is_authenticated
    g_json = d_serialize(g)
    g_json["user"] = d_serialize(current_user)
    g_json["user"]["id"] = current_user.is_authenticated and current_user.id or 0
    return g_json
