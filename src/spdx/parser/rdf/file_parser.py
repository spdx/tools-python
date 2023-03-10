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
from rdflib import URIRef, Graph, RDFS

from spdx.model.file import File, FileType
from spdx.parser.logger import Logger
from spdx.parser.parsing_functions import construct_or_raise_parsing_error, raise_parsing_error_if_logger_has_messages
from spdx.parser.rdf.checksum_parser import parse_checksum
from spdx.parser.rdf.graph_parsing_functions import parse_literal, parse_spdx_id, parse_literal_or_no_assertion_or_none, \
    get_correctly_typed_value, apply_parsing_method_or_log_error, parse_enum_value
from spdx.parser.rdf.license_expression_parser import parse_license_expression
from spdx.rdfschema.namespace import SPDX_NAMESPACE


def parse_file(file_node: URIRef, graph: Graph, doc_namespace: str) -> File:
    logger = Logger()
    spdx_id = parse_spdx_id(file_node, doc_namespace, graph)
    name = parse_literal(logger, graph, file_node, SPDX_NAMESPACE.fileName)
    checksums = []
    for (_, _, checksum_node) in graph.triples((file_node, SPDX_NAMESPACE.checksum, None)):
        checksums.append(parse_checksum(checksum_node, graph))

    file_types = []
    for (_, _, file_type_ref) in graph.triples((file_node, SPDX_NAMESPACE.fileType, None)):
        file_types.append(
            apply_parsing_method_or_log_error(logger, file_type_ref,
                                              parsing_method=lambda x: parse_enum_value(x, FileType,
                                                                                        SPDX_NAMESPACE.fileType_)))
    license_concluded = parse_literal_or_no_assertion_or_none(
        logger, graph, file_node, SPDX_NAMESPACE.licenseConcluded,
        parsing_method=lambda x: parse_license_expression(x, graph, doc_namespace))
    license_info_in_file = []
    for (_, _, license_info_from_files_node) in graph.triples((file_node, SPDX_NAMESPACE.licenseInfoInFile, None)):
        license_info_in_file.append(
            get_correctly_typed_value(logger, license_info_from_files_node,
                                      lambda x: parse_license_expression(x, graph, doc_namespace)))
    license_comment = parse_literal(logger, graph, file_node, SPDX_NAMESPACE.licenseComments)
    copyright_text = parse_literal_or_no_assertion_or_none(logger, graph, file_node, SPDX_NAMESPACE.copyrightText)
    file_contributors = []
    for (_, _, file_contributor) in graph.triples((file_node, SPDX_NAMESPACE.fileContributor, None)):
        file_contributors.append(file_contributor.toPython())

    notice_text = parse_literal(logger, graph, file_node, SPDX_NAMESPACE.noticeText)
    comment = parse_literal(logger, graph, file_node, RDFS.comment)
    attribution_texts = []
    for (_, _, attribution_text_literal) in graph.triples((file_node, SPDX_NAMESPACE.attributionText, None)):
        attribution_texts.append(attribution_text_literal.toPython())
    raise_parsing_error_if_logger_has_messages(logger, "File")
    file = construct_or_raise_parsing_error(File, dict(name=name, spdx_id=spdx_id, checksums=checksums,
                                                       attribution_texts=attribution_texts, comment=comment,
                                                       copyright_text=copyright_text, file_types=file_types,
                                                       contributors=file_contributors,
                                                       license_comment=license_comment,
                                                       license_concluded=license_concluded,
                                                       license_info_in_file=license_info_in_file,
                                                       notice=notice_text))
    return file
