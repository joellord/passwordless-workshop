from functools import wraps
from jose import jwt
from flask import _request_ctx_stack, request

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def get_token_auth_header():
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({
            "code": "authorization_header_missing",
            "description": "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must start with 'Bearer'"
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            "code": "invalid_header",
            "description": "Token not found"
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            "code": "invalid_header",
            "desription": "Authorization header must be 'Bearer token'"
        }, 401)

    token = parts[1]
    return token


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()

        try:
            payload = jwt.decode(token, "my-super-secret-key", algorithms="HS256", audience="my-random-clickbait-api", issuer="my-small-auth-server")

        except jwt.ExpiredSignatureError:
            raise AuthError({"code": "token_expired", "description": "Token is expired"}, 401)

        except jwt.JWTClaimsError:
            raise AuthError({"code": "invalid_claims", "description": "Incorrect claims, please check aud and iss"}, 401)

        except Exception:
            raise AuthError({"code": "invalid_header", "description": "Unable to parse authentication token."}, 401)

        _request_ctx_stack.top.current_user = payload


        return f(*args, **kwargs)

    return decorated
