# -*- coding: utf-8 -*-
# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""Swagger controller"""


import datetime

from .. import contexts, model, wsgihelpers


SWAGGER_BASE_PATH = '/api/1/formula'


@wsgihelpers.wsgify
def api1_swagger(req):
    ctx = contexts.Ctx(req)
    headers = wsgihelpers.handle_cross_origin_resource_sharing(ctx)

    paths = {
        '/' + name: {
            'get': map_to_swagger(column)
        }
        for name, column in model.tax_benefit_system.column_by_name.iteritems()
        if column.formula_class is not None  # output variables only, not input parameters
    }

    return wsgihelpers.respond_json(ctx,
        {
            'swagger': '2.0',
            'info': {
                'version': '1.0.0',
                'title': 'OpenFisca',
                'description': '',
                'termsOfService': 'http://github.com/openfisca/openfisca-web-api',
                'contact': {
                    'name': 'OpenFisca team',
                    'email': 'contact@openfisca.fr',
                    'url': 'http://github.com/openfisca/openfisca-web-api/issues'
                },
                'license': {
                    'name': 'AGPL',
                    'url': 'https://www.gnu.org/licenses/agpl-3.0.html'
                }
            },
            'basePath': SWAGGER_BASE_PATH,
            'paths': paths
        },
        headers = headers,
        )


# Transforms the description of a column into a Swagger representation.
def map_to_swagger(column):
    return map_path_to_swagger(column)


def map_path_to_swagger(column):
    result = map_path_base_to_swagger(column.to_json())
    result['parameters'] = map_parameters_to_swagger(column)

    return result

def map_path_base_to_swagger(column_json):
    result = {
        'summary'      : column_json.get('label'),
        'tags'         : [ column_json.get('entity') ],
        'responses': {
            200: {
                'description': column_json.get('label'),
                'schema': map_type_to_swagger(column_json.get('@type', ''))
            }
        }
    }

    if column_json.get('url'):
        result['externalDocs'] = { 'url': column_json.get('url') }

    return result

def map_parameters_to_swagger(column):
    input_variables = []

    try:
        input_variables = model.input_variables_extractor.get_input_variables(column)
    except Exception, e:
        print(e)

    return [
        map_parameter_to_swagger(model.tax_benefit_system.column_by_name[variable_name])
        for variable_name in input_variables
    ]

def map_parameter_to_swagger(column):
    column_json = column.to_json()

    default = column.default

    if isinstance(default, datetime.date):
        default = '%s-%s-%s' % (default.year, default.month, default.day)

    result = map_type_to_swagger(column_json.get('@type'))
    result.update({
        'name'        : column_json.get('name'),
        'description' : column_json.get('label'),
        'default'     : default,
        'in'          : 'query'
    })

    return result

# Transforms a Python type to a Swagger type
def map_type_to_swagger(type):
    result = { 'type': type.lower() }

    if type == 'Integer':
        result['format'] = 'int32'
    elif type == 'Float':
        result['type'] = 'number'
        result['format'] = 'float'
    elif type == 'Date':
        result['type'] = 'string'
        result['format'] = 'date'
    elif type == 'Enumeration':
        result['type'] = 'string'

    return result
