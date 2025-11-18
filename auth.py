import functools
import json

from logger import log


def auth_required():
    """Decorate methods with this to require that the user session."""

    def decorater(method):
        @functools.wraps(method)
        async def wrapper(*args, **kwargs):
            request = kwargs["request"]

            try:
                body = await request.json()
            except json.decoder.JSONDecodeError:
                body = {}

            log.info(f"[auth_required] {request.headers} | Body({body})")
            request.state.auth = {}
            result = await method(*args, **kwargs)
            log.info(f"[response_result] {result}")
            return result

        return wrapper

    return decorater
