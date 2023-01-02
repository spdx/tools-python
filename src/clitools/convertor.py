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

import click

from src.model.document import Document
from src.parser.parse_anything import parse_file
from src.writer.write_anything import write_file


@click.command()
@click.option("--infile", "-i", help="The file containing the document to be converted")
@click.option("--outfile", "-o", help="The file to write the converted document to")
def main(infile, outfile):
    """
    CLI-tool for converting SPDX documents between RDF, TAG-VALUE, JSON, YAML and XML formats.
    Formats are determined by the file endings.
    To use, run: 'pyspdxtools_convertor --infile <input file name> --outfile <output file name> '
    """
    try:
        document: Document = parse_file(infile)

        write_file(document, outfile)
    except NotImplementedError as err:
        print(err.args[0])
        print("Please note that this project is currently undergoing a major refactoring and therefore missing "
              "a few features which will be added in time.\n"
              "In the meanwhile, please use the current PyPI release version 0.7.0.")
        return


if __name__ == "__main__":
    main()
