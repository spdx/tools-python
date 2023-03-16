# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys
from typing import List

import click

from spdx.model.document import Document
from spdx.parser.parse_anything import parse_file
from spdx.validation.document_validator import validate_full_spdx_document
from spdx.validation.validation_message import ValidationMessage
from spdx3.bump_from_spdx2.spdx_document import bump_spdx_document
from spdx3.payload import Payload
from spdx3.writer.console.payload_writer import write_payload


@click.command()
@click.option("--infile", "-i", prompt="input file path",
              help="The file containing the document to be validated or converted.")
@click.option("--outfile", "-o",
              help="The file to write the converted document to (write a dash for output to stdout or omit for no conversion).")
@click.option("--version", help='The SPDX version to be used during parsing and validation (format "SPDX-2.3").',
              default="SPDX-2.3")
@click.option("--novalidation", is_flag=True, help="Don't validate the provided document.")
def main(infile: str, outfile: str, version: str, novalidation: bool):
    """
    CLI-tool to parse and validate a SPDX 2.x document and migrate it into the prototype of SPDX 3.0. As there is no
    definition for a serialization yet output can only be written to stdout.
    To use, run: 'pyspdxtools3 --infile <input file name> -o -'
    """
    try:
        document: Document = parse_file(infile)

        if not novalidation:
            validation_messages: List[ValidationMessage] = validate_full_spdx_document(document, version)
            if validation_messages:
                print("The document is invalid. The following issues have been found:", file=sys.stderr)
                for message in validation_messages:
                    print(message.validation_message, file=sys.stderr)
                sys.exit(1)
            else:
                print("The document is valid.", file=sys.stderr)

        if outfile == "-":
            payload: Payload = bump_spdx_document(document)
            write_payload(payload, sys.stdout)

    except NotImplementedError as err:
        print(err.args[0])
        sys.exit(1)


if __name__ == "__main__":
    main()
