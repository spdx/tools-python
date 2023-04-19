# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from rdflib import RDFS, Graph, URIRef

from spdx_tools.spdx.model import ExtractedLicensingInfo
from spdx_tools.spdx.parser.logger import Logger
from spdx_tools.spdx.parser.parsing_functions import (
    construct_or_raise_parsing_error,
    raise_parsing_error_if_logger_has_messages,
)
from spdx_tools.spdx.parser.rdf.graph_parsing_functions import (
    get_correctly_typed_triples,
    parse_literal,
    parse_literal_or_no_assertion_or_none,
)
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE


def parse_extracted_licensing_info(
    extracted_licensing_info_node: URIRef, graph: Graph, doc_namespace: str
) -> ExtractedLicensingInfo:
    logger = Logger()
    license_id = parse_literal(logger, graph, extracted_licensing_info_node, SPDX_NAMESPACE.licenseId)
    if not license_id:
        license_id = (
            extracted_licensing_info_node.fragment
            if extracted_licensing_info_node.startswith(f"{doc_namespace}#")
            else extracted_licensing_info_node.toPython()
        )

    extracted_text = parse_literal(logger, graph, extracted_licensing_info_node, SPDX_NAMESPACE.extractedText)
    comment = parse_literal(logger, graph, extracted_licensing_info_node, RDFS.comment)
    license_name = parse_literal_or_no_assertion_or_none(
        logger, graph, extracted_licensing_info_node, SPDX_NAMESPACE.name
    )
    cross_references = []
    for _, _, cross_reference_node in get_correctly_typed_triples(
        logger, graph, extracted_licensing_info_node, RDFS.seeAlso
    ):
        cross_references.append(cross_reference_node.toPython())
    raise_parsing_error_if_logger_has_messages(logger, "ExtractedLicensingInfo")
    extracted_licensing_info = construct_or_raise_parsing_error(
        ExtractedLicensingInfo,
        dict(
            license_id=license_id,
            extracted_text=extracted_text,
            comment=comment,
            license_name=license_name,
            cross_references=cross_references,
        ),
    )

    return extracted_licensing_info
