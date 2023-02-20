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
from spdx.parser.rdf.graph_parsing_functions import parse_literal, parse_literal_or_no_assertion_or_none

from spdx.parser.parsing_functions import raise_parsing_error_if_logger_has_messages, construct_or_raise_parsing_error

from spdx.model.extracted_licensing_info import ExtractedLicensingInfo
from spdx.parser.logger import Logger
from spdx.rdfschema.namespace import SPDX_NAMESPACE


def parse_extracted_licensing_info(extracted_licensing_info_node: URIRef, graph: Graph) -> ExtractedLicensingInfo:
    logger = Logger()
    license_id = parse_literal(logger, graph, extracted_licensing_info_node, SPDX_NAMESPACE.licenseId)
    extracted_text = parse_literal(logger, graph, extracted_licensing_info_node, SPDX_NAMESPACE.extractedText)
    comment = parse_literal(logger, graph, extracted_licensing_info_node, RDFS.comment)
    license_name = parse_literal_or_no_assertion_or_none(logger, graph, extracted_licensing_info_node, SPDX_NAMESPACE.name)
    cross_references = []
    for (_, _, cross_reference_node) in graph.triples((extracted_licensing_info_node, RDFS.seeAlso, None)):
        cross_references.append(cross_reference_node.toPython())
    raise_parsing_error_if_logger_has_messages(logger, "ExtractedLicensingInfo")
    extracted_licensing_info = construct_or_raise_parsing_error(ExtractedLicensingInfo, dict(license_id=license_id,
                                                                                             extracted_text=extracted_text,
                                                                                             comment=comment,
                                                                                             license_name=license_name,
                                                                                             cross_references=cross_references))

    return extracted_licensing_info
