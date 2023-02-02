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
from typing import Optional, Union

from rdflib import URIRef, Graph, RDFS, DOAP
from rdflib.exceptions import UniquenessError

from spdx.datetime_conversions import datetime_from_str
from spdx.model.actor import Actor
from spdx.model.package import Package, PackagePurpose
from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.parser.error import SPDXParsingError
from spdx.parser.jsonlikedict.actor_parser import ActorParser
from spdx.parser.logger import Logger
from spdx.parser.parsing_functions import raise_parsing_error_if_logger_has_messages, construct_or_raise_parsing_error
from spdx.parser.rdf.checksum_parser import parse_checksum
from spdx.parser.rdf.graph_parsing_functions import parse_spdx_id, parse_literal, str_to_no_assertion_or_none
from spdx.rdfschema.namespace import SPDX_NAMESPACE


def parse_package(package_node: URIRef, graph: Graph, doc_namespace: str) -> Package:
    logger = Logger()
    spdx_id = parse_spdx_id(package_node, doc_namespace)
    name = parse_literal(logger, graph, package_node, SPDX_NAMESPACE.name)
    download_location = parse_literal(logger, graph, package_node, SPDX_NAMESPACE.downloadLocation)
    checksums = []
    for (_, _, checksum_node) in graph.triples((package_node, SPDX_NAMESPACE.checksum, None)):
        checksums.append(parse_checksum(checksum_node, graph))

    version_info = parse_literal(logger, graph, package_node, SPDX_NAMESPACE.versionInfo)
    package_file_name = parse_literal(logger, graph, package_node, SPDX_NAMESPACE.packageFileName)
    try:
        supplier = parse_actor_or_no_assertion(logger, graph, package_node, SPDX_NAMESPACE.supplier)
    except SPDXParsingError as err:
        logger.extend(err.get_messages())
        supplier = None
    try:
        originator = parse_actor_or_no_assertion(logger, graph, package_node, SPDX_NAMESPACE.originator)
    except SPDXParsingError as err:
        logger.extend(err.get_messages())
        originator = None

    files_analyzed = bool(graph.value(package_node, SPDX_NAMESPACE.filesAnalyzed, default=True))
    license_comment = parse_literal(logger, graph, package_node, SPDX_NAMESPACE.licenseComments)
    comment = parse_literal(logger, graph, package_node, RDFS.comment)
    summary = parse_literal(logger, graph, package_node, SPDX_NAMESPACE.summary)
    description = parse_literal(logger, graph, package_node, SPDX_NAMESPACE.description)
    copyright_text = parse_literal(logger, graph, package_node, SPDX_NAMESPACE.copyrightText,
                                   method_to_apply=str_to_no_assertion_or_none)
    source_info = parse_literal(logger, graph, package_node, SPDX_NAMESPACE.sourceInfo)
    try:
        primary_package_purpose = parse_primary_package_purpose(package_node, graph)
    except KeyError:
        logger.append(f"Invalid PackagePurpose: {graph.value(package_node, SPDX_NAMESPACE.primaryPackagePurpose)}")
        primary_package_purpose = None
    homepage = parse_literal(logger, graph, package_node, DOAP.homepage)
    attribution_texts = []
    for (_, _, attribution_text_literal) in graph.triples((package_node, SPDX_NAMESPACE.attributionText, None)):
        attribution_texts.append(attribution_text_literal.toPython())

    release_date = parse_literal(logger, graph, package_node, SPDX_NAMESPACE.releaseDate,
                                 method_to_apply=datetime_from_str)
    built_date = parse_literal(logger, graph, package_node, SPDX_NAMESPACE.builtDate,
                               method_to_apply=datetime_from_str)
    valid_until_date = parse_literal(logger, graph, package_node, SPDX_NAMESPACE.validUntilDate,
                                     method_to_apply=datetime_from_str)

    raise_parsing_error_if_logger_has_messages(logger, "Package")
    package = construct_or_raise_parsing_error(Package,
                                               dict(name=name, spdx_id=spdx_id, download_location=download_location,
                                                    version=version_info, file_name=package_file_name,
                                                    supplier=supplier, originator=originator,
                                                    files_analyzed=files_analyzed,
                                                    verification_code=None,
                                                    checksums=checksums, homepage=homepage,
                                                    source_info=source_info,
                                                    license_concluded=None,
                                                    license_info_from_files=None,
                                                    license_declared=None,
                                                    license_comment=license_comment,
                                                    copyright_text=copyright_text, summary=summary,
                                                    description=description, comment=comment,
                                                    external_references=None,
                                                    attribution_texts=attribution_texts,
                                                    primary_package_purpose=primary_package_purpose,
                                                    release_date=release_date, built_date=built_date,
                                                    valid_until_date=valid_until_date))

    return package


def parse_actor_or_no_assertion(logger, graph, parent_node, predicate) -> Optional[Union[SpdxNoAssertion, Actor]]:
    try:
        value = graph.value(parent_node, predicate, any=False)
    except UniquenessError:
        logger.append(f"Multiple values for unique value {predicate} found.")
        return
    if not value:
        return None
    if value == "NOASSERTION":
        return SpdxNoAssertion()
    return ActorParser.parse_actor(value)


def parse_primary_package_purpose(package_node: URIRef, graph: Graph) -> Optional[PackagePurpose]:
    primary_package_purpose_ref = graph.value(package_node, SPDX_NAMESPACE.primaryPackagePurpose)
    if not primary_package_purpose_ref:
        return None
    return PackagePurpose[primary_package_purpose_ref.fragment.replace("purpose_", "").upper()]
