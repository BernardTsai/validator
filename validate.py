#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import yaml
import json
import jsonschema
import logging
import traceback
import textwrap

#-------------------------------------------------------------------------------

version = "0.0.0" # version of this program
model   = {}      # the model as parsed from stdin
schema  = {}      # the schema for a model

# ------------------------------------------------------------------------------
# loadModel: loads yaml model
# ------------------------------------------------------------------------------
def loadModel():
    global model

    # A. read yaml from stdin
    yaml_file = ''
    for line in sys.stdin:
        yaml_file += line

    # B. parse yaml into a model
    try:
        model = yaml.safe_load(yaml_file)
    except Exception as exc:
        print("Loading the model has failed:")
        print(textwrap.indent("{}".format(exc), '  ', lambda line: True))
        exit(1)

# ------------------------------------------------------------------------------
# loadSchema: loads schema
# ------------------------------------------------------------------------------
def loadSchema():
    global model
    global schema

    # A. derive schema version from model
    if not 'schema' in model:
        print("Model does not have a schema attribute")
        exit(1)

    # B. determine path of module
    script_path = os.path.dirname(os.path.realpath(__file__))

    # C. determine path of schema
    schema_path = os.path.join(script_path, "schema", "V" + model['schema'] + ".json")

    # D. check if schema is available
    if not os.path.isfile(schema_path):
        print("Schema '" + schema + "' is not supported")
        exit(1)

    # E. load schema as json
    try:
        file        = open(schema_path, "r")
        schema_json = file.read()
    except Exception as exc:
        print("Unable to read schema '" + model['schema'] + "'")
        exit(1)

    # F. convert json into schema object
    try:
        schema = json.loads(schema_json)
    except Exception as exc:
        print("Unable to parse schema 'V" + model['schema'] + ".json' as json:")
        print(textwrap.indent("{}".format(exc), '  ', lambda line: True))
        exit(1)

    return

# ------------------------------------------------------------------------------
# validateModel: validate model
# ------------------------------------------------------------------------------
def validateModel():
    global model
    global schema

    # A. create a validator
    try:
        validator = jsonschema.Draft7Validator(schema)
    except Exception as exc:
        print("Invalid schema '" + model.schema + "':")
        print(textwrap.indent("{}".format(exc), '  ', lambda line: True))
        exit(1)

    # B. validate model
    errors = sorted(validator.iter_errors(model), key=lambda e: e.path)

    # C. print errors if any
    has_errors = False
    for error in errors:
        if not has_errors:
            print( "Schema errors:")
        has_errors = True
        print(textwrap.indent(str(error), '  ', lambda line: True))

    # D. exit if errors occured
    if has_errors:
        exit(1)

    return

#-------------------------------------------------------------------------------

def main():
    # load yaml model and validate
    try:
        # load model
        loadModel()

        # load schema
        loadSchema()

        # validate model
        validateModel()

    except Exception as exc:
        print("Unknown error:")
        print(textwrap.indent("{}".format(traceback.format_exc()), '  ', lambda line: True))
        return 1

    return 0

#-------------------------------------------------------------------------------

if __name__ == "__main__":
    main()

#-------------------------------------------------------------------------------
