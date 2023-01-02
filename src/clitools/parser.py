#!/usr/bin/env python3

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

import sys
from typing import List

import click

from src.model.document import Document
from src.parser.parse_anything import parse_file
from src.validation.document_validator import validate_full_spdx_document
from src.validation.validation_message import ValidationMessage
from src.writer.tagvalue.tagvalue_writer import write_document


@click.command()
@click.option("--file", prompt="File name", help="The file to be parsed")
@click.option("--version", prompt="SPDX version", help="The SPDX version to be used during validation")
@click.option("--validate", is_flag=True, help="validate the provided document")
@click.option("--printout", is_flag=True, help="print the parsed document to stdout in tag-value format")
def main(file, version, validate, printout):
    """
    CLI-tool for parsing file of RDF, TAG-VALUE, JSON, YAML and XML format.
    To use : run `pyspdxtools_parser` using terminal or run `pyspdxtools_parser --file <file name>`
    """
    try:
        document: Document = parse_file(file)
    except NotImplementedError as err:
        print(err.args[0])
        print("Please note that this project is currently undergoing a major refactoring and therefore missing "
              "a few features which will be added in time.\n"
              "In the meanwhile, please use the current PyPI release version 0.7.0.")
        return

    if printout:
        write_document(document, sys.stdout)
        print("")

    if validate:
        validation_messages: List[ValidationMessage] = validate_full_spdx_document(document, version)
        if validation_messages:
            print("The document is invalid. The following issues have been found:")
            for message in validation_messages:
                print(message.validation_message)
        else:
            print("The document is valid.")


if __name__ == "__main__":
    main()
