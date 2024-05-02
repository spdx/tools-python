#!/usr/bin/env python3

# Copyright (c) 2020 Yash Varshney
# Copyright (c) 2023 spdx contributors
# SPDX-License-Identifier: Apache-2.0
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import sys
from json import JSONDecodeError
from xml.parsers.expat import ExpatError
from xml.sax import SAXParseException

import click
from beartype.typing import List
from yaml.scanner import ScannerError

from spdx_tools.spdx.graph_generation import export_graph_from_document
from spdx_tools.spdx.model import Document
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.parse_anything import parse_file
from spdx_tools.spdx.validation.document_validator import validate_full_spdx_document
from spdx_tools.spdx.validation.validation_message import ValidationMessage
from spdx_tools.spdx.writer.tagvalue import tagvalue_writer
from spdx_tools.spdx.writer.write_anything import write_file


@click.command()
@click.option("--infile", "-i", required=True, help="The file containing the document to be validated or converted.")
@click.option(
    "--outfile",
    "-o",
    help="The file to write the converted document to (write a dash for output to stdout or omit for no conversion). "
    "If you add the option --graph to the command the generated graph will be written to this file.",
)
@click.option(
    "--version",
    help='The SPDX version to be used during parsing and validation ("SPDX-2.2" or "SPDX-2.3"). '
    "Will be read from the document if not provided.",
    default=None,
)
@click.option("--novalidation", is_flag=True, help="Don't validate the provided document.")
@click.option(
    "--graph",
    is_flag=True,
    default=False,
    help="Generate a relationship graph from the input file. "
    "The generated graph is saved to the file specified with --outfile. "
    "Note: You need to install the optional dependencies 'networkx' and 'pygraphviz' for this feature.",
)
def main(infile: str, outfile: str, version: str, novalidation: bool, graph: bool):
    """
    CLI-tool for validating SPDX documents and converting between RDF, TAG-VALUE, JSON, YAML and XML formats.
    Formats are determined by the file endings.
    To use, run: 'pyspdxtools --infile <input file name> --outfile <output file name>'
    """
    try:
        document: Document = parse_file(infile)

        if not novalidation:
            if not version:
                version = document.creation_info.spdx_version

            if version not in ["SPDX-2.2", "SPDX-2.3"]:
                logging.error(f"This tool only supports SPDX versions SPDX-2.2 and SPDX-2.3, but got: {version}")
                sys.exit(1)

            validation_messages: List[ValidationMessage] = validate_full_spdx_document(document, version)
            if validation_messages:
                log_string = "\n".join(
                    ["The document is invalid. The following issues have been found:"]
                    + [message.validation_message for message in validation_messages]
                )
                logging.error(log_string)
                sys.exit(1)
            else:
                logging.info("The document is valid.")

        if outfile == "-":
            tagvalue_writer.write_document(document, sys.stdout)

        elif graph:
            try:
                export_graph_from_document(document, outfile)
            except ImportError:
                logging.error(
                    "To be able to draw a relationship graph of the parsed document "
                    "you need to install 'networkx' and 'pygraphviz'. Run 'pip install \".[graph_generation]\"'."
                )
                sys.exit(1)

        elif outfile:
            write_file(document, outfile, validate=False)

    except NotImplementedError as err:
        logging.error(
            err.args[0]
            + "\nPlease note that this project is currently undergoing a major refactoring and therefore missing "
            "a few features which will be added in time (refer to https://github.com/spdx/tools-python/issues "
            "for insights into the current status).\n"
            "In the meantime, please use the current PyPI release version."
        )
        sys.exit(1)

    except SPDXParsingError as err:
        log_string = "\n".join(
            ["There have been issues while parsing the provided document:"]
            + [message for message in err.get_messages()]
        )
        logging.error(log_string)
        sys.exit(1)

    except JSONDecodeError as err:
        logging.error(f"Invalid JSON provided: {err.args[0]}")
        sys.exit(1)

    except ScannerError as err:
        logging.error("Invalid YAML provided: " + "\n".join([str(arg) for arg in err.args]))
        sys.exit(1)

    except ExpatError as err:
        logging.error(f"Invalid XML provided: {err.args[0]}")
        sys.exit(1)

    except SAXParseException as err:
        logging.error(f"Invalid RDF-XML provided: {str(err)}")
        sys.exit(1)

    except FileNotFoundError as err:
        logging.error(f"{err.strerror}: {err.filename}")
        sys.exit(1)


if __name__ == "__main__":
    main()
