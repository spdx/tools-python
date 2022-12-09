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

from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.spdx_none import SpdxNone


@click.command()
@click.option("--file", prompt="File name", help="The file to be parsed")
@click.option("--force", is_flag=True, help="print information even if there are some parsing errors")
def main(file, force):
    """
    COMMAND-LINE TOOL for parsing file of RDF, XML, JSON, YAML and XML format.

    To use : run `pyspdxtools_parser` using terminal or run `pyspdxtools_parser --file <file name>`

    """
    raise NotImplementedError("Currently, no parsers are implemented")

    # Parse document
    # First one to implement is the Json parser: https://github.com/spdx/tools-python/issues/305

    # Print all document properties - or possibly a selection of them. Should be human-readable, so using indentation
    # for nested properties is probably a good idea.


if __name__ == "__main__":
    main()
