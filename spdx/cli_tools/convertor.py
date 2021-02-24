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

import os
from spdx.parsers.builderexceptions import FileTypeError
from spdx.parsers.parse_anything import parse_file
from spdx.writers.write_anything import write_file

import click

def print_help_msg(command):
    with click.Context(command) as ctx:
        click.echo(command.get_help(ctx))

def determine_infile_and_outfile(infile, outfile, src, from_, to):
    if infile is not None and outfile is not None:
        """
        when the CLI is of given format:
        ' pyspdxtools_convertor ---infile <input_file> ---outfile <output_file>.
        """
        return infile, outfile

    elif infile is None and outfile is None and len(src) == 2:
        """
        ' pyspdxtools_convertor -f/--from <type> <input_file> -t/--to <type> <output_file>.
        """
        infile = src[0]
        outfile = src[1]
        # infile = os.path.splitext(infile)[0]
        if from_ is not None:
            infile_path = os.path.splitext(infile)[0]
            infile = infile_path + "." + from_
        if to is not None:
            outfile_path = os.path.splitext(outfile)[0]
            outfile = outfile_path + "." + to
        return infile, outfile

    elif infile is None and outfile is not None:
        """
        ' pyspdxtools_convertor -f/--from <type> <input_file> --outfile <output_file> '
        """
        infile = src[0]
        if from_ is not None:
            infile_path = os.path.splitext(infile)[0]
            infile = infile_path + "." + from_
        return infile, outfile

    elif infile is not None and outfile is None:
        """
        ' pyspdxtools_convertor --infile <input_file> -t/--to <type> <output_file>'
        """
        outfile = src[0]
        if to is not None:
            outfile_path = os.path.splitext(outfile)[0]
            outfile = outfile_path + "." + to
        return infile, outfile

    else:
        raise ValueError("Given arguments for convertor are invalid.")


@click.command()
@click.argument("src", nargs=-1)
@click.option("--infile", "-i", help="The file to be converted ")
@click.option("--outfile", "-o", help="The file after converting")
@click.option(
    "--to",
    "-t",
    type=click.Choice(["json", "rdf", "yaml", "xml", "tag"], case_sensitive=False)
)
@click.option(
    "--from",
    "-f",
    "from_",
    type=click.Choice(["tag", "rdf"], case_sensitive=False))
@click.option("--force", is_flag=True, help="convert even if there are some parsing errors or inconsistencies")
def main(infile, outfile, src, from_, to, force):
    """
    CLI-TOOL for converting a RDF or TAG file to RDF, JSON, YAML, TAG or XML format.

    To use : run 'pyspdxtools_convertor -f <from_TYPE> <input file> -t <to_TYPE> <output_file>' command on terminal or use ' pyspdxtools_convertor --infile <input file name> --outfile <output file name> '

    """
    try:
        infile, outfile = determine_infile_and_outfile(infile, outfile, src, from_, to)
    except ValueError as err:
        print(err)
        print_help_msg(main)
        return

    doc, errors = parse_file(infile)
    if errors:
        print("Errors while parsing: ", errors)
        if not force:
            return 1

    write_file(doc, outfile)


if __name__ == "__main__":
    main()
