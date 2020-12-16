discord-interactions-python
---
![PyPI - License](https://img.shields.io/pypi/l/discord-interactions)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/discord-interactions)

Types and helper functions for Discord Interactions webhooks.

# Installation

Available via [pypi](https://pypi.org/project/discord-interactions/):

```
pip install discord-interactions
```

# Usage

Use the `InteractionType` and `InteractionResponseType` enums to process and respond to webhooks.

Use `verify_key` to check a request signature:

```py
if verify_key(request.data, signature, timestamp, 'my_client_public_key'):
    print('Signature is valid')
else:
    print('Signature is invalid')
```

Use `verify_key_decorator` to protect routes in a Flask app:

```py
import os

from flask import Flask, request, jsonify

from discord_interactions import verify_key_decorator, InteractionType, InteractionResponseType

CLIENT_PUBLIC_KEY = os.getenv('CLIENT_PUBLIC_KEY')

app = Flask(__name__)

@app.route('/interactions', methods=['POST'])
@verify_key_decorator(CLIENT_PUBLIC_KEY)
def interactions():
  if request.json['type'] == InteractionType.APPLICATION_COMMAND:
    return jsonify({
        'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        'data': {
            'content': 'Hello world'
        }
    })
```

# Exports

This module exports the following:

### InteractionType

An enum of interaction types that can be POSTed to your webhook endpoint.

### InteractionResponseType

An enum of response types you may provide in reply to Discord's webhook.

### InteractionResponseFlags

An enum of flags you can set on your response data.

### verify_key(raw_body: str, signature: str, timestamp: str, client_public_key: str) -> bool:

Verify a signed payload POSTed to your webhook endpoint.

### verify_key_decorator(client_public_key: str)

Flask decorator that will verify request signatures and handle PING/PONG requests.
