import os

from flask import Flask

from discord_interactions import verify_key_decorator

CLIENT_PUBLIC_KEY = os.getenv('CLIENT_PUBLIC_KEY')

app = Flask(__name__)

@app.route('/interactions', methods=['POST'])
@verify_key_decorator(CLIENT_PUBLIC_KEY)
def interactions():
    return 'Hello, World!'
