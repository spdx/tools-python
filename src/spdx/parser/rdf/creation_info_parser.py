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
import logging
import sys
from typing import Tuple
from urllib.parse import urldefrag

from rdflib import Graph, RDFS, RDF, Namespace
from rdflib.exceptions import UniquenessError
from rdflib.term import URIRef

from spdx.parser.error import SPDXParsingError
from spdx.parser.logger import Logger
from spdx.parser.parsing_functions import construct_or_raise_parsing_error, raise_parsing_error_if_logger_has_messages
from spdx.parser.rdf.checksum_parser import parse_checksum
from spdx.parser.rdf.graph_parsing_functions import parse_literal, parse_spdx_id, remove_prefix
from spdx.rdfschema.namespace import SPDX_NAMESPACE, LICENSE_NAMESPACE

from spdx.datetime_conversions import datetime_from_str
from spdx.model.document import CreationInfo
from spdx.model.external_document_ref import ExternalDocumentRef
from spdx.model.version import Version
from spdx.parser.actor_parser import ActorParser


def parse_creation_info(graph: Graph) -> Tuple[CreationInfo, URIRef]:
    logger = Logger()
    namespace, spdx_id, doc_node = parse_namespace_and_spdx_id(graph)
    spec_version = parse_literal(logger, graph, doc_node, SPDX_NAMESPACE.specVersion)
    data_license = parse_literal(logger, graph, doc_node, SPDX_NAMESPACE.dataLicense,
                                 parsing_method=lambda x: remove_prefix(x, LICENSE_NAMESPACE))
    comment = parse_literal(logger, graph, doc_node, RDFS.comment)
    name = parse_literal(logger, graph, doc_node, SPDX_NAMESPACE.name)

    creation_info_node = graph.value(predicate=RDF.type, object=SPDX_NAMESPACE.CreationInfo)
    if not creation_info_node:
        logger.append("CreationInfo does not exist.")
        raise SPDXParsingError([f"Error while parsing document {name}: {logger.get_messages()}"])

    created = parse_literal(logger, graph, creation_info_node, SPDX_NAMESPACE.created,
                            parsing_method=datetime_from_str)
    license_list_version = parse_literal(logger, graph, creation_info_node, SPDX_NAMESPACE.licenseListVersion,
                                         parsing_method=Version.from_string)
    creator_comment = parse_literal(logger, graph, creation_info_node, RDFS.comment)
    creators = []
    for (_, _, creator_literal) in graph.triples((creation_info_node, SPDX_NAMESPACE.creator, None)):
        creators.append(ActorParser.parse_actor(creator_literal))
    external_document_refs = []
    for (_, _, external_document_node) in graph.triples((doc_node, SPDX_NAMESPACE.externalDocumentRef, None)):
        external_document_refs.append(parse_external_document_refs(external_document_node, graph, namespace))

    raise_parsing_error_if_logger_has_messages(logger, "CreationInfo")
    creation_info = construct_or_raise_parsing_error(CreationInfo, dict(spdx_id=spdx_id, document_namespace=namespace,
                                                                        spdx_version=spec_version, name=name,
                                                                        data_license=data_license,
                                                                        document_comment=comment, created=created,
                                                                        license_list_version=license_list_version,
                                                                        creator_comment=creator_comment,
                                                                        creators=creators,
                                                                        external_document_refs=external_document_refs))
    return creation_info, doc_node


def parse_namespace_and_spdx_id(graph: Graph) -> (str, str):
    try:
        subject = graph.value(predicate=RDF.type, object=SPDX_NAMESPACE.SpdxDocument, any=False)
    except UniquenessError:
        logging.error("Multiple SpdxDocuments found, can't parse rdf file.")
        sys.exit(1)

    if not subject:
        logging.error("No SpdxDocument found, can't parse rdf file.")
        sys.exit(1)
    if not "#" in subject:
        logging.error("No '#' found in the URI of SpdxDocument, "
                      "the URI for the SpdxDocument should be the namespace appended by '#SPDXRef-DOCUMENT.")
        sys.exit(1)

    namespace, spdx_id = urldefrag(subject)

    if not namespace:
        logging.error(
            "No namespace found, the URI for the SpdxDocument should be the namespace appended by '#SPDXRef-DOCUMENT.")
        sys.exit(1)

    if not spdx_id:
        spdx_id = None

    return namespace, spdx_id, subject


def parse_external_document_refs(external_document_node: URIRef, graph: Graph,
                                 doc_namespace: str) -> ExternalDocumentRef:
    logger = Logger()
    document_ref_id = parse_spdx_id(external_document_node, doc_namespace, graph)
    document_uri = parse_literal(logger, graph, external_document_node, SPDX_NAMESPACE.spdxDocument)
    checksum = parse_literal(logger, graph, external_document_node, SPDX_NAMESPACE.checksum,
                             parsing_method=lambda x: parse_checksum(x, graph))
    external_document_ref = construct_or_raise_parsing_error(ExternalDocumentRef, dict(document_ref_id=document_ref_id,
                                                                                       document_uri=document_uri,
                                                                                       checksum=checksum))

    # To replace the external doc namespaces by the ref id in spdx ids later (e.g. in a relationship), we need to bind
    # the namespace to the graph.
    graph.bind(external_document_ref.document_ref_id, Namespace(external_document_ref.document_uri + "#"))

    return external_document_ref
