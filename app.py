from integrate import init, translate, is_valid_input
from flask import Flask, jsonify, request, abort, Response
from werkzeug.exceptions import BadRequest

import socket
import os
import json

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
        return handle_POST(isValidInput)
    else:
        return abort(Response(response="GET method not allowed", status=405))


def handle_POST(func):
    try:
        input = request.json
        data = func(input["q"])
        return jsonify(data)
    except BadRequest:
        abort(Response(response="No input", status=400))
    except KeyError:
        abort(Response(response="Missing 'q' value from json", status=400))
    except:
        abort(Response(response="Failed to translate", status=400))


if __name__ == "__main__":
    init()
    app.run(host='0.0.0.0', port=4000)
