import jwt
from jwt.exceptions import DecodeError


class Token:
    def __init__(self, token: str) -> None:
        self._token = token
        try:
            self._roles = jwt.decode(token, options={"verify_signature": False}).get(
                "roles", []
            )
        except DecodeError:
            self._roles = []

    @property
    def roles(self):
        return self._roles
