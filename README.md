# OpenFisca Web-API

[![Build Status via Travis CI](https://travis-ci.org/openfisca/openfisca-web-api.svg?branch=master)](https://travis-ci.org/openfisca/openfisca-web-api)

## Presentation

[OpenFisca](http://www.openfisca.fr/) is a versatile microsimulation free software.
This is the source code of the Web-API module.

Please consult http://www.openfisca.fr/presentation

## Documentation

Please consult http://www.openfisca.fr/documentation

## Installation

> An unrestricted instance of the OpenFisca API is hosted online at http://api.openfisca.fr/.
> You need to install this Python package if you want to contribute to its source code or run a local instance
> on your computer.

Clone the OpenFisca-Web-API Git repository on your machine and install the Python package.
Assuming you are in your working directory:

```
git clone https://github.com/openfisca/openfisca-web-api.git
cd openfisca-web-api
pip install --editable .[dev] --user
python setup.py compile_catalog
```

Run the Python HTTP server:

    paster serve --reload development-france.ini

To stop the server, interrupt the command with Ctrl-C.

To check if it's OK, open the following URL in your browser:
http://localhost:2000/ (2000 is the port number defined in the development-france.ini config file).
You should see a JSON response telling that the path is not found (which is normal as no endpoint corresponds to "/"):

    {"apiVersion": "1.0", "error": {"message": "Path not found: /", "code": 404}}

## Docker containers

Docker containers are available:
[docker-france](https://github.com/openfisca/openfisca-web-api/tree/master/docker-france),
[docker-tunisia](https://github.com/openfisca/openfisca-web-api/tree/master/docker-tunisia) and
[docker-mes-aides](https://github.com/openfisca/openfisca-web-api/tree/master/docker-mes-aides).

## Contribute

OpenFisca is a free software project.
Its source code is distributed under the [GNU Affero General Public Licence](http://www.gnu.org/licenses/agpl.html)
version 3 or later (see COPYING).

Feel free to join the OpenFisca development team on [GitHub](https://github.com/openfisca) or contact us by email at
contact@openfisca.fr

## Code architecture

Each API endpoint (`calculate`, `simulate`, etc.) source code has its own controller (a function responding to a HTTP request) in `openfisca_web_api/controllers`.

Each controller function consists basically of 3 steps:
* reading and validating user input (with `req.params`)
* doing some computations
* returning the results in JSON (with `wsgihelpers.respond_json`)

The configuration of the application is stored in `development-<country>.ini` files, `<country>` being either
`france` or `tunisia`.
The configuration is validated once when the application starts. The validation code is in `openfisca_web_api/environment.py` at the beginning of the `load_environment` function.

The tests are in `openfisca_web_api/tests`.

The function `make_app` in `openfisca_web_api/application.py` returns a [WSGI](http://wsgi.readthedocs.org/) application. It is the main entry point of the application and is declared in `setup.py`.

All conversion and validation steps are done using the [Biryani](https://biryani.readthedocs.org) library.
