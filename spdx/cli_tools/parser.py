#!/usr/bin/env python

# Copyright (c) 2020 Yash Varshney
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
from examples.parse_json import parse_JSON
from examples.parse_rdf import parse_RDF
from examples.parse_tv import parse_TAG
from examples.parse_yaml import parse_YAML
from examples.parse_xml import parse_XML
from spdx.parsers.builderexceptions import FileTypeError

import click


@click.command()
# @click.argument('file')
@click.option("--file", prompt="File name", help="The file to be parsed")
def main(file):
    """
    COMMAND-LINE TOOL for parsing file of RDF, XML, JSON, YAML and XML format.

    To use : run `parser` using terminal or run `parser --file <file name>`

    """
    if file.endswith(".rdf"):
        parsed_result = parse_rdf(file)
        click.echo(parsed_result)
    elif file.endswith(".rdf.xml"):
        parsed_result = parse_rdf(file)
        click.echo(parsed_result)
    elif file.endswith(".spdx"):
        parsed_result = parse_tag(file)
        click.echo(parsed_result)
    elif file.endswith(".tag"):
        parsed_result = parse_tag(file)
        click.echo(parsed_result)
    elif file.endswith(".json"):
        parsed_result = parse_json(file)
        click.echo(parsed_result)
    elif file.endswith(".xml"):
        parsed_result = parse_xml(file)
        click.echo(parsed_result)
    elif file.endswith(".yaml"):
        parsed_result = parse_yaml(file)
        click.echo(parsed_result)
    else:
        raise FileTypeError("FileType Not Supported")


def parse_json(file):
    file = str(file)
    try:
        return parse_JSON(os.path.join(file))
    except EnvironmentError as e:
        print(os.strerror(e.errno))


def parse_rdf(file):
    file = str(file)
    try:
        return parse_RDF(os.path.join(file))
    except EnvironmentError as e:
        print(os.strerror(e.errno))


def parse_tag(file):
    file = str(file)
    try:
        return parse_TAG(os.path.join(file))
    except EnvironmentError as e:
        print(os.strerror(e.errno))


def parse_yaml(file):
    file = str(file)
    try:
        return parse_YAML(os.path.join(file))
    except EnvironmentError as e:
        print(os.strerror(e.errno))


def parse_xml(file):
    file = str(file)
    try:
        return parse_XML(os.path.join(file))
    except EnvironmentError as e:
        print(os.strerror(e.errno))


if __name__ == "__main__":
    main()
