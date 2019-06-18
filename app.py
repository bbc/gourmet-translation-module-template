from integrate import init, translate, is_valid_input
from flask import Flask, jsonify, request, abort, Response
from werkzeug.exceptions import BadRequest

import socket
import os
import json
import logging

# Configure logging format
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)


@app.route("/", methods=['GET'])
def root():
    return "This is a translation module. Use the /translation endpoint for translating text and the /checkInput endpoint to check that the input is valid."


@app.route("/translation", methods=['POST', 'GET'])
def translation():
    if request.method == 'POST':
        return handle_POST(translate)
    else:
        return abort(Response(response="GET method not allowed", status=405))


@app.route("/checkInput", methods=['POST', 'GET'])
def character_check():
    if request.method == 'POST':
        return handle_POST(is_valid_input)
    else:
        return abort(Response(response="GET method not allowed", status=405))


def handle_POST(func):
    """
    Handles POST requests where the body of the request is JSON where one of the keys is "q". E.g. {"q": "hello world"}
    :param func. A function that takes a string and a logger object and returns a python dictionary.
    """
    try:
        input = request.json
        data = func(input["q"], logging)
        return jsonify(data)
    except BadRequest:
        abort(Response(response="No input", status=400))
    except KeyError:
        abort(Response(response="Missing 'q' value from json", status=400))
    except:
        logging.exception(
            "Unexpected Error when handling a POST request. Exception caught.")
        abort(Response(response="Failed to translate", status=400))


if __name__ == "__main__":
    init(logging)
    app.run(host='0.0.0.0', port=4000)
