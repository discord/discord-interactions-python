import os

from flask import Flask, jsonify, request

from discord_interactions import verify_key_decorator, InteractionType, InteractionResponseType, InteractionResponseFlags

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
    elif request.json['type'] == InteractionType.MESSAGE_COMPONENT:
        return jsonify({
            'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
            'data': {
                'content': 'Hello, you interacted with a component.',
                'flags': InteractionResponseFlags.EPHEMERAL
            }
        })
        
