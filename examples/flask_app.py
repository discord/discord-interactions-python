import os

from flask import Flask, jsonify

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
