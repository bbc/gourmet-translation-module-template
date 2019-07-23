from integrate import init, translate
from flask import Flask, jsonify, request, abort, Response
from werkzeug.exceptions import BadRequest, InternalServerError

import socket
import os
import json
import logging

# Configure logging format
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
model = None
app = Flask(__name__)


@app.route("/", methods=['GET'])
def root():
    return "This is a translation module. Use the /translation endpoint for translating text."


@app.route("/translation", methods=['POST'])
def translation():
    return handle_POST(translate)


def handle_POST(func):
    """
    Handles POST requests where the body of the request is JSON where one of the keys is "q". E.g. {"q": "hello world"}
    :param func. A function that takes a translation model, a string and a logger object and returns a python dictionary.
    """
    payload = request.json
    if not (payload or payload.get('q')):
        return BadRequest("No payload given")
    try:
        data = func(model, payload["q"], logging)
        return jsonify(data)
    except Exception as e:
        logging.exception(
            "Unexpected Error when handling a POST request. Exception caught: %s.", e)
        return InternalServerError(e)


if __name__ == "__main__":
    model = init()
    app.run(host='0.0.0.0', port=4000)
