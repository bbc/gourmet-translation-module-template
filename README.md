# Translation Module Format

This is the template for delivery of translation modules for the GoURMET project.

## Purpose

To provide a consistent interface for all translation models delivered over the course of the project.

## How it works

This a basic API build using [python](https://www.python.org/) and [flask](http://flask.pocoo.org/).

There are 2 endpoints:

```
GET /
POST /translate
```

### `/`

Root. Provides basic information about the API

### `/translate`

POST endpoint. Translates from the source language to the target language. Expects JSON data of the form `{"q"=string}` e.g. `{"q"="hello world"}`. Returns:

```
{
    "result": string/None,
    "time_taken: int/None,
    "error": Object/None,
}
```

Where time_taken is in milliseconds and error is of the form:

```
{
    "reason" : string
    "timestamp" : int,
    "model_version" : string
}
```

For example: `curl -X POST -d '{"q":"hello world"}' -H "Content-Type: application/json" localhost:4000/translation`

## What you need to do

### Some set up.

You will need [Docker](https://www.docker.com/) installed on your machine. Installation instructions are [here](https://docs.docker.com/install/).

### Implement some functions:

Implement two functions in the `integrate.py` file. There is placeholder code in the functions which can be deleted. You can add additional functions and variables to the file but the `init` and `translate` functions should not be deleted and the function signatures should not be changed. You can add additional directories and files but the `app.py`, `Dockerfile`, and `requirements.txt` need to remain in the root directory. The `integrate.py` file also needs to remain in the root directory.

#### `init()`

This function is run once when the application starts. This is where all set up required by you should be done. `init` should return a translationModel. This model will be passed into the translate function whenever it is called.

#### `translate(initialisedModel, textToTranslate, logger)`

This is the translation function. There are three parameters:

- `initialisedModel` which is the model created by the `init` function
- `textToTranslate` which is the text that needs to be translated
- `logger` which is a logger object that is either the [python default logger](https://docs.python.org/3/library/logging.html) or an instance of a class that matches the default python logging interface.

The function must return a [python dictionary](https://docs.python.org/3.7/tutorial/datastructures.html#dictionaries) of the following shape:

```
{
    "result": string/None,
    "time_taken: int/None,
    "error": string/None,
}
```

e.g.

```
{
    "result": "translated text here",
    "time_taken": 100,
    "error": None,
}
```

Time taken must be in milliseconds. The [Handle Errors](#handle-errors) section of the README outlines how to handle errors and the shape of the 'error' object.

### Handle Errors

Errors should be handled by either raising an exception or logging to the logger passed into each of the functions. Errors should be surfaced by either raising an exception or manually adding a log to the logger provided and error messages should contain as much information as possible. As a minimum and error message shall report the reason for failure. The python documentation on [logging](https://docs.python.org/3/howto/logging.html#logging-basic-tutorial) should be used to determine the appropriate logging level for a given incident.

In addition the `translate` function should also return an error object as part of larger object returned by both of these functions. The structure of the error object shall be as follows:

```
{
    "reason": string
    "timestamp": int
    "model_version": string
}
```

e.g

```
{
    "reason": "stack overflow"
    "timestamp": 1560865674
    "model_version": "0.1"
}
```

### Change the Dockerfile if you need to

No commands should be removed from the Dockerfile template provided but additional commands can be added. The `CMD ["python", "app.py"]` must be the final step in the Dockerfile. The base image can be changed to be something other than `python:3}` providing the new base image also includes [Python 3](https://www.python.org/) and [pip](https://pypi.org/project/pip) or they are added via the Dockerfile.

For example you could use [apt](https://wiki.debian.org/Apt) in the Dockerfile if your base image was not `python:3`:

```
RUN apt-get update
RUN apt-get install -y python3 python3-pip
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
```

or curled with the data in a json file

```
curl -X POST -d '@data.json' -H "Content-Type: application/json" -v localhost:4000/translation
```

Where `data.json` is a file in the directory the curl command is run from and contains the data for the curl command e.g. `{"q":"hello world"}`

### Export Image

Export and compress an image using:

```
docker save <image name> | gzip > filename.tar.gz
```

## General useful Docker commands

- List all images: `docker images`
- List all running containers: `docker ps`
- List all containers: `docker container ls --all`

- Stop a container: `docker container stop <container id>`
- Stop all containers: `docker stop $(docker ps -q)`

- Remove an image: `docker rmi <image id>`
- Remove a container: `docker rm <container id>`

- See the logs for a container: `docker logs <container id>`
- See events from docker: `docker events`