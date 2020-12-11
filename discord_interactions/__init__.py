__version__ = '0.1.0'

from functools import wraps

from nacl.encoding import HexEncoder
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

class InteractionType:
    PING = 1
    APPLICATION_COMMAND = 2

class InteractionResponseType:
    PONG = 1
    ACKNOWLEDGE = 2
    CHANNEL_MESSAGE = 3
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    ACKNOWLEDGE_WITH_SOURCE = 5

class InteractionResponseFlags:
    EPHEMERAL = 1 << 6

def verify_key(raw_body: str, signature: str, timestamp: str, client_public_key: str) -> bool:
    message = timestamp.encode() + raw_body
    try:
        vk = VerifyKey(bytes.fromhex(client_public_key))
        vk.verify(message, bytes.fromhex(signature))
        return True
    except Exception as ex:
        print(ex)
        pass
    return False

def verify_key_decorator(client_public_key):
    from flask import request, jsonify

    # https://stackoverflow.com/questions/51691730/flask-middleware-for-specific-route
    def _decorator(f):
        @wraps(f)
        def __decorator(*args, **kwargs):
            # Verify request
            signature = request.headers.get('X-Signature-Ed25519')
            timestamp = request.headers.get('X-Signature-Timestamp')
            if not verify_key(request.data, signature, timestamp, client_public_key):
                return 'Bad request signature', 403

            # Automatically respond to pings
            if request.json and request.json['type'] == InteractionType.PING:
                return jsonify({
                    'type': InteractionResponseType.PONG
                })

            # Pass through
            return f(*args, **kwargs)
        return __decorator
    return _decorator

