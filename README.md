# Translation Module Format

This is the template for delivery of translation modules for the GoURMET project.

## Purpose

To provide a consistent interface for all translation models delivered over the course of the project.

## How it works

This a basic API build using [python](https://www.python.org/) and [flask](http://flask.pocoo.org/).

There are 3 endpoints:

```
GET /
POST /translate
POST /checkInput
```

### `/`

Root. Provides basic information about the API

### `/translate`

POST endpoint. Translates from the source language to the target language. Expects JSON data of the form `{"q"="hello world"}`.

For example: `curl -X POST -d '{"q":"hello world"}' -H "Content-Type: application/json" localhost:4000/translation`

### `/checkInput`

POST endpoint. Checks that a string contains only valid characters. Returns true if it does and false otherwise. Expects JSON data of the form `{"q"="hello world"}`.

For example: `curl -X POST -d '{"q":"hello world"}' -H "Content-Type: application/json" localhost:4000/checkInput`

## What you need to do

### Some set up.

You will need [Docker](https://www.docker.com/) installed on your machine. Installation instructions are [here](https://docs.docker.com/install/).

### Implement some functions:

Implement three functions in the `integrate.py` file. There is placeholder code in the functions which can be deleted. You can add additional functions and variables to the file but the `init`, `translate` and `is_valid_input` functions should not be deleted and the function signatures should not be changed. You can add additional directories and files but the `app.py`, `Dockerfile`, and `requirements.txt` need to remain in the root directory and remain as they are. The `integrate.py` file also needs to remain in the root directory.

#### `init()`

This function is run once when the application starts. This is where all set up required by you should be done

#### `translate(input)`

This is the translation function. There is a parameter `input` which is the text that needs to be translated. The function must return a [python dictionary](https://docs.python.org/3.7/tutorial/datastructures.html#dictionaries) of the following shape:

```
{
    "translation": string/None,
    "original": string/None,
    "error": string/None,
    "model": string
}
```

e.g.

```
{
    "translation": "translated text here",
    "original": "original text here",
    "error": None,
    "model": "0.1"
}
```

#### `is_valid_input(input)`

This function checks that the input, which will be a string, is valid. The purpose of this function is to define what characters are allowed and as a result will be handled correctly by the translation model. The function must return a [python dictionary](https://docs.python.org/3.7/tutorial/datastructures.html#dictionaries) of the following shape:

```
{
    "isValidInput": boolean,
    "original": string/None,
    "error": string/None,
    "model": string
}
```

e.g.

```
{
    "isValidInput": "translated text here",
    "original": "original text here",
    "error": None,
    "model": "0.1"
}
```

### Build Docker Image

The [Dockerfile](./Dockerfile) defines how to build a docker image. Running:

```
docker build --tag=<tagname> .
```

Check this worked by running:

```
docker run -p 4000:4000 <tagname>
```

The endpoints can be checked using cURL

```
curl localhost:4000 -v

curl -X POST -d '{"q":"hello world"}' -H "Content-Type: application/json" -v localhost:4000/translation

curl -X POST -d '{"q":"hello world"}' -H "Content-Type: application/json" -v localhost:4000/checkInput
```

# TODO:

- Add info on how to tag docker images
- Add info on how to push image to a docker repository
