from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import request
from werkzeug import exceptions

from .models import User
from .settings import JWT_SECRET

JWT_ALGORITHM = "HS256"

# Normally we wouldn't want such long tokens. But the data here is not sensitive
# and the auth is meant to provide just a thin layer of protection. Long browser
# sessions are most important.
# TODO: Extend this. This is short just for testing sakes early on.
TOKEN_LIFETIME = timedelta(hours=1)
JWT_AUDIENCE = "350bt"
JWT_ISSUER = "350bt"


def create_jwt(user_id):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + TOKEN_LIFETIME,
        "aud": JWT_AUDIENCE,
        "iss": JWT_ISSUER,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_jwt(token):
    return jwt.decode(
        token, JWT_SECRET, audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM]
    )


# TODO: Rewrite this to invert the auth check
def auth_required(view_fn):
    @wraps(view_fn)
    def check_auth_and_run(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth:
            raise exceptions.Unauthorized("No authorization header")
        if not auth.startswith("JWT "):
            raise exceptions.Unauthorized("Expecting JWT auth type")

        jwt = verify_jwt(auth[4:])

        # Make sure the user still exists
        if not User.query.get(jwt["sub"]):
            raise exceptions.Forbidden("User from JWT no longer exists")

        return view_fn(*args, **kwargs)

    return check_auth_and_run
