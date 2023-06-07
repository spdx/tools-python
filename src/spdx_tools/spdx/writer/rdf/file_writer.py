# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Dict
from rdflib import RDF, RDFS, Graph, Literal, URIRef

from spdx_tools.spdx.casing_tools import snake_case_to_camel_case
from spdx_tools.spdx.model import File
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE
from spdx_tools.spdx.writer.rdf.checksum_writer import add_checksum_to_graph
from spdx_tools.spdx.writer.rdf.license_expression_writer import add_license_expression_or_none_or_no_assertion
from spdx_tools.spdx.writer.rdf.writer_utils import add_namespace_to_spdx_id, add_optional_literal


def add_file_to_graph(file: File, graph: Graph, doc_namespace: str, external_doc_ref_to_namespace: Dict[str, str]):
    file_resource = URIRef(add_namespace_to_spdx_id(file.spdx_id, doc_namespace, external_doc_ref_to_namespace))
    graph.add((file_resource, RDF.type, SPDX_NAMESPACE.File))
    graph.add((file_resource, SPDX_NAMESPACE.fileName, Literal(file.name)))
    for file_type in file.file_types:
        graph.add(
            (
                file_resource,
                SPDX_NAMESPACE.fileType,
                SPDX_NAMESPACE[f"fileType_{snake_case_to_camel_case(file_type.name)}"],
            )
        )

    for checksum in file.checksums:
        add_checksum_to_graph(checksum, graph, file_resource)

    add_license_expression_or_none_or_no_assertion(
        file.license_concluded, graph, file_resource, SPDX_NAMESPACE.licenseConcluded, doc_namespace
    )
    add_license_expression_or_none_or_no_assertion(
        file.license_info_in_file, graph, file_resource, SPDX_NAMESPACE.licenseInfoInFile, doc_namespace
    )

    add_optional_literal(file.license_comment, graph, file_resource, SPDX_NAMESPACE.licenseComments)
    add_optional_literal(file.copyright_text, graph, file_resource, SPDX_NAMESPACE.copyrightText)
    add_optional_literal(file.comment, graph, file_resource, RDFS.comment)
    add_optional_literal(file.notice, graph, file_resource, SPDX_NAMESPACE.noticeText)
    for contributor in file.contributors:
        graph.add((file_resource, SPDX_NAMESPACE.fileContributor, Literal(contributor)))
    for attribution_text in file.attribution_texts:
        graph.add((file_resource, SPDX_NAMESPACE.attributionText, Literal(attribution_text)))
