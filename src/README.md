# Development Guide

This folder contain all sources for development.

## Dev Environment Setup

Overall, there are two components required:
- Backend: FastAPI, and underlying python 3
- Datastore: Elasticsearch

The general procedure of setting up a dev environment should not vary much for different OSes.

### Backend

Make sure python 3 is installed on dev machine. At the time of writing, the latest version of python 3 release is 3.8.6.
- Make sure python executables (`python`, `pip`) are in `$PATH` on Windows. If an error says `python` or `pip` is not a command in terminal, re-install python and tick "Add to PATH" in installer, then restart computer.
- Be careful where to install python. If it is a system level installation (e.g. python directory is located in `C:\Program Files\python`), all operations below should be done with escalated privilege. If an error message says not enough permission to install package, run terminal as administrator.
- To use python 3 under macOS or Linux, use `python3` and `pip3` as commands.
- `pip3` may not be installed under Linux even if `python3` exists. Search for how to install package for a specific Linux distribution.
- In case python versions and dependencies may be difficult to manage under Linux, consider using [pyenv](https://github.com/pyenv/pyenv) for manage python environments.

Run commands below in a terminal:
```sh
$ pip install fastapi
$ pip install uvicorn
$ pip install elasticsearch[async]
$ pip install aiofiles
```

### Datastore

Follow download and install guide on [elasticsearch website](https://www.elastic.co/downloads/elasticsearch).
- Do not put unzipped elasticsearch directory under a path with spaces on Windows, or `elasticsearch.bat` file will complain.
    - `C:\elasticsearch` is a safe and easy place.
- Install elasticsearch as a service is _not_ necessary. Run elasticsearch while developing the project is sufficient.

## Run Application

- Run elasticsearch
    - Windows: [Run from archive `.zip`](https://www.elastic.co/guide/en/elasticsearch/reference/current/starting-elasticsearch.html#start-zip)
    - macOS or Linux: [Run from archive `.tar.gz`](https://www.elastic.co/guide/en/elasticsearch/reference/current/starting-elasticsearch.html#start-targz)
    - **The terminal used for running elasticsearch will be used exclusively by elasticsearch to output logs,** open a new terminal to perform the following steps
    - `control-C` can be pressed to stop elasticsearch, but do not stop it now
- Run local backend server
    - Change to project `src` directory
    - `uvicorn --port 8080 --reload main:app`
- Verify application is running
    - Open http://localhost:8080/docs in browser
        - A swagger-ui API documentation page should appear
- Verify application is working with elasticsearch
    - Postman: An API testing tool
    - [Download postman](https://www.postman.com/downloads/)
    - Import project `postman` folder, open "elasticsearch" collection and check "local" environment
        - Environment is on top right, click on "eyes" icon to show values of variables
        - Whenever postman collection is updated, delete local environment and collection, then re-import the folder
    - Navigate to "elasticsearch" collection on the left
    - Go to "Post Doc" API, press "Send"
        - Response should be 200 with a JSON body
        - Copy the `_id` field in JSON into current value of local environment `doc_id` field
    - Go to "Get Index" API, press "Send"
        - Response should be both 200 with a JSON body
        - Previous message stored in elasticsearch should appear

## Future Goals

- **Frontend**
- Figure out elasticsearch concepts
- **Separate APIs into different modules**
- API versioning
- Configure routing with static files
