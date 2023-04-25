# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import os
from datetime import datetime
from typing import List, Tuple

import pytest
from rdflib import RDF, Graph, URIRef
from rdflib.term import Node

from spdx_tools.spdx.constants import DOCUMENT_SPDX_ID
from spdx_tools.spdx.model import Actor, ActorType, Checksum, ChecksumAlgorithm, Version
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.rdf.creation_info_parser import (
    parse_creation_info,
    parse_external_document_refs,
    parse_namespace_and_spdx_id,
)
from spdx_tools.spdx.parser.rdf.rdf_parser import parse_from_file
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE


def test_parse_creation_info():
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/file_to_test_rdf_parser.rdf.xml"))

    creation_info, _ = parse_creation_info(graph)
    assert creation_info.spdx_id == DOCUMENT_SPDX_ID
    assert creation_info.spdx_version == "SPDX-2.3"
    assert creation_info.name == "documentName"
    assert creation_info.document_namespace == "https://some.namespace"
    assert creation_info.creators == [Actor(ActorType.PERSON, "creatorName", "some@mail.com")]
    assert creation_info.created == datetime(2022, 12, 1, 0, 0)
    assert creation_info.creator_comment == "creatorComment"
    assert creation_info.data_license == "CC0-1.0"
    assert creation_info.license_list_version == Version(3, 19)
    assert creation_info.document_comment == "documentComment"


def test_parse_namespace_and_spdx_id():
    graph = Graph().add((URIRef("docNamespace#spdxID"), RDF.type, SPDX_NAMESPACE.SpdxDocument))

    namespace, spdx_id, _ = parse_namespace_and_spdx_id(graph)

    assert namespace == "docNamespace"
    assert spdx_id == "spdxID"


@pytest.mark.parametrize(
    "triples,error_message",
    [
        (
            [(URIRef("docNamespace"), RDF.type, SPDX_NAMESPACE.SpdxDocument)],
            r"No '#' found in the URI of SpdxDocument",
        ),
        ([(URIRef(""), RDF.type, URIRef(""))], r"No SpdxDocument found, can't parse rdf file."),
        ([(URIRef(f"#{DOCUMENT_SPDX_ID}"), RDF.type, SPDX_NAMESPACE.SpdxDocument)], "No namespace found"),
        (
            [
                (URIRef("docNamespace1"), RDF.type, SPDX_NAMESPACE.SpdxDocument),
                (URIRef("docNamespace2"), RDF.type, SPDX_NAMESPACE.SpdxDocument),
            ],
            "Multiple SpdxDocuments found",
        ),
    ],
)
def test_parse_namespace_and_spdx_id_with_system_exit(
    triples: List[Tuple[Node, Node, Node]], error_message: str, caplog
):
    graph = Graph()
    for triple in triples:
        graph = graph.add(triple)

    with pytest.raises(SystemExit):
        parse_namespace_and_spdx_id(graph)

    assert error_message in caplog.text


def test_parse_external_document_refs():
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/file_to_test_rdf_parser.rdf.xml"))
    doc_namespace = "https://some.namespace"
    external_doc_ref_node = graph.value(
        subject=URIRef(f"{doc_namespace}#{DOCUMENT_SPDX_ID}"), predicate=SPDX_NAMESPACE.externalDocumentRef
    )
    assert isinstance(external_doc_ref_node, URIRef)

    external_document_ref = parse_external_document_refs(external_doc_ref_node, graph, doc_namespace)

    assert external_document_ref.document_ref_id == "DocumentRef-external"
    assert external_document_ref.checksum == Checksum(
        ChecksumAlgorithm.SHA1, "71c4025dd9897b364f3ebbb42c484ff43d00791c"
    )
    assert external_document_ref.document_uri == "https://namespace.com"


@pytest.mark.parametrize(
    "file, error_message",
    [
        (
            "invalid_creation_info.rdf.xml",
            "Error while parsing CreationInfo: ['No creators provided.']",
        ),
        ("invalid_creation_info_with_snippet.rdf.xml", "Error while parsing CreationInfo: ['No creators provided.']"),
    ],
)
def test_parse_invalid_creation_info(file, error_message):
    with pytest.raises(SPDXParsingError) as err:
        parse_from_file(os.path.join(os.path.dirname(__file__), f"data/invalid_documents/{file}"))

    assert err.value.get_messages() == [error_message]
