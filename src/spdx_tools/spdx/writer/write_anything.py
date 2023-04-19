# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from spdx_tools.spdx.formats import FileFormat, file_name_to_format
from spdx_tools.spdx.model import Document
from spdx_tools.spdx.writer.json import json_writer
from spdx_tools.spdx.writer.rdf import rdf_writer
from spdx_tools.spdx.writer.tagvalue import tagvalue_writer
from spdx_tools.spdx.writer.xml import xml_writer
from spdx_tools.spdx.writer.yaml import yaml_writer


def write_file(document: Document, file_name: str, validate: bool = True):
    output_format = file_name_to_format(file_name)
    if output_format == FileFormat.JSON:
        json_writer.write_document_to_file(document, file_name, validate)
    elif output_format == FileFormat.YAML:
        yaml_writer.write_document_to_file(document, file_name, validate)
    elif output_format == FileFormat.XML:
        xml_writer.write_document_to_file(document, file_name, validate)
    elif output_format == FileFormat.TAG_VALUE:
        tagvalue_writer.write_document_to_file(document, file_name, validate)
    elif output_format == FileFormat.RDF_XML:
        rdf_writer.write_document_to_file(document, file_name, validate)
