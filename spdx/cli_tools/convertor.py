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
from examples.rdf_to_json import RDF_to_JSON
from examples.rdf_to_tv import RDF_to_TAG
from examples.rdf_to_xml import RDF_to_XML
from examples.rdf_to_yaml import RDF_to_YAML
from examples.tv_to_json import TAG_to_JSON
from examples.tv_to_rdf import TAG_to_RDF
from examples.tv_to_xml import TAG_to_XML
from examples.tv_to_yaml import TAG_to_YAML
from spdx.parsers.builderexceptions import FileTypeError

import click


@click.command()
@click.argument("src", nargs=-1)
@click.option("--infile", "-i", help="The file to be converted ", default="undefined")
@click.option("--outfile", "-o", help="The file after converting", default="undefined")
@click.option(
    "--to",
    "-t",
    type=click.Choice(["json", "rdf", "yaml", "xml", "tag"], case_sensitive=False),
    default="undefined",
)
@click.option(
    "--from",
    "-f",
    "from_",
    type=click.Choice(["tag", "rdf"], case_sensitive=False),
    default="undefined",
)
def main(infile, outfile, src, from_, to):
    """
    CLI-TOOL for converting a RDF or TAG file to RDF, JSON, YAML, TAG or XML format.

    To use : run 'convertor -f <from_TYPE> <input file> -t <to_TYPE> <output_file>' command on terminal or use ' convertor --infile <input file name> --outfile <output file name> '

    """
    if infile is None and outfile is None:
        """
        when the CLI is of given format:
        ' convertor -f/--from <type> <input_file> -t/--to <type> <output_file>.
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

    elif infile is None and outfile is not None:
        """
        ' convertor -f/--from <type> <input_file> --outfile <output_file> '
        """
        infile = src[0]
        if from_ is not None:
            infile_path = os.path.splitext(infile)[0]
            infile = infile_path + "." + from_

    elif infile is not None and outfile is None:
        """
        ' convertor --infile <input_file> -t/--to <type> <output_file>'
        """
        outfile = src[0]
        if to is not None:
            outfile_path = os.path.splitext(outfile)[0]
            outfile = outfile_path + "." + to

    if infile.endswith(".rdf"):
        infile_format = "rdf"
    elif infile.endswith(".tag"):
        infile_format = "tag"
    else:
        raise FileTypeError(
            "INPUT FILETYPE NOT SUPPORTED. (only RDF and TAG format supported)"
        )

    if outfile.endswith(".rdf"):
        outfile_format = "rdf"
    elif outfile.endswith(".tag"):
        outfile_format = "tag"
    elif outfile.endswith(".json"):
        outfile_format = "json"
    elif outfile.endswith(".xml"):
        outfile_format = "xml"
    elif outfile.endswith(".yaml"):
        outfile_format = "yaml"
    elif outfile.endswith(".spdx"):
        outfile_format = "tag"
    elif outfile.endswith(".rdf.xml"):
        outfile_format = "rdf"
    else:
        raise FileTypeError("OUTFILE FILETYPE NOT SUPPORTED")

    try:
        func_to_call = infile_format + "_to_" + outfile_format
        result = globals()[func_to_call](infile, outfile)
        click.echo(result)
    except EnvironmentError as e:
        print(os.strerror(e.errno))


def rdf_to_json(infile, outfile):
    infile = str(infile)
    outfile = str(outfile)
    try:
        return RDF_to_JSON(os.path.join(infile), os.path.join(outfile))
    except EnvironmentError as e:
        print(os.strerror(e.errno))


def rdf_to_tag(infile, outfile):
    infile = str(infile)
    outfile = str(outfile)
    try:
        return RDF_to_TAG(os.path.join(infile), os.path.join(outfile))
    except EnvironmentError as e:
        print(os.strerror(e.errno))


def rdf_to_yaml(infile, outfile):
    infile = str(infile)
    outfile = str(outfile)
    try:
        return RDF_to_YAML(os.path.join(infile), os.path.join(outfile))
    except EnvironmentError as e:
        # OSError or IOError...
        print(os.strerror(e.errno))


def rdf_to_xml(infile, outfile):
    infile = str(infile)
    outfile = str(outfile)
    try:
        return RDF_to_XML(os.path.join(infile), os.path.join(outfile))
    except EnvironmentError as e:
        print(os.strerror(e.errno))


def tag_to_json(infile, outfile):
    infile = str(infile)
    outfile = str(outfile)
    try:
        return TAG_to_JSON(os.path.join(infile), os.path.join(outfile))
    except EnvironmentError as e:
        print(os.strerror(e.errno))


def tag_to_rdf(infile, outfile):
    infile = str(infile)
    outfile = str(outfile)
    try:
        return TAG_to_RDF(os.path.join(infile), os.path.join(outfile))
    except EnvironmentError as e:
        print(os.strerror(e.errno))


def tag_to_yaml(infile, outfile):
    infile = str(infile)
    outfile = str(outfile)
    try:
        return TAG_to_YAML(os.path.join(infile), os.path.join(outfile))
    except EnvironmentError as e:
        print(os.strerror(e.errno))


def tag_to_xml(infile, outfile):
    infile = str(infile)
    outfile = str(outfile)
    try:
        return TAG_to_XML(os.path.join(infile), os.path.join(outfile))
    except EnvironmentError as e:
        print(os.strerror(e.errno))


if __name__ == "__main__":
    main()
