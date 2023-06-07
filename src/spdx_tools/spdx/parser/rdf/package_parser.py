# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Optional, Union
from rdflib import DOAP, RDFS, Graph, URIRef
from rdflib.term import BNode

from spdx_tools.spdx.datetime_conversions import datetime_from_str
from spdx_tools.spdx.model import (
    ExternalPackageRef,
    ExternalPackageRefCategory,
    Package,
    PackagePurpose,
    PackageVerificationCode,
)
from spdx_tools.spdx.parser.actor_parser import ActorParser
from spdx_tools.spdx.parser.logger import Logger
from spdx_tools.spdx.parser.parsing_functions import (
    construct_or_raise_parsing_error,
    raise_parsing_error_if_logger_has_messages,
)
from spdx_tools.spdx.parser.rdf.checksum_parser import parse_checksum
from spdx_tools.spdx.parser.rdf.graph_parsing_functions import (
    get_correctly_typed_triples,
    get_correctly_typed_value,
    get_value_from_graph,
    parse_enum_value,
    parse_literal,
    parse_literal_or_no_assertion_or_none,
    parse_spdx_id,
)
from spdx_tools.spdx.parser.rdf.license_expression_parser import parse_license_expression
from spdx_tools.spdx.rdfschema.namespace import REFERENCE_NAMESPACE, SPDX_NAMESPACE


def parse_package(package_node: Union[URIRef, BNode], graph: Graph, doc_namespace: str) -> Package:
    logger = Logger()
    spdx_id = parse_spdx_id(package_node, doc_namespace, graph)
    name = parse_literal(logger, graph, package_node, SPDX_NAMESPACE.name)
    download_location = parse_literal_or_no_assertion_or_none(
        logger, graph, package_node, SPDX_NAMESPACE.downloadLocation
    )
    checksums = []
    for _, _, checksum_node in get_correctly_typed_triples(logger, graph, package_node, SPDX_NAMESPACE.checksum):
        checksums.append(parse_checksum(checksum_node, graph))

    version_info = parse_literal(logger, graph, package_node, SPDX_NAMESPACE.versionInfo)
    package_file_name = parse_literal(logger, graph, package_node, SPDX_NAMESPACE.packageFileName)

    supplier = parse_literal_or_no_assertion_or_none(
        logger, graph, package_node, SPDX_NAMESPACE.supplier, parsing_method=ActorParser.parse_actor
    )
    originator = parse_literal_or_no_assertion_or_none(
        logger, graph, package_node, SPDX_NAMESPACE.originator, parsing_method=ActorParser.parse_actor
    )
    verification_code = parse_literal(
        logger,
        graph,
        package_node,
        SPDX_NAMESPACE.packageVerificationCode,
        parsing_method=lambda x: parse_package_verification_code(x, graph),
    )

    external_package_refs = []
    for _, _, external_package_ref_node in get_correctly_typed_triples(
        logger, graph, package_node, SPDX_NAMESPACE.externalRef
    ):
        external_package_refs.append(parse_external_package_ref(external_package_ref_node, graph, doc_namespace))
    files_analyzed = bool(
        get_value_from_graph(logger, graph, package_node, SPDX_NAMESPACE.filesAnalyzed, default=True)
    )
    license_concluded = parse_literal_or_no_assertion_or_none(
        logger,
        graph,
        package_node,
        SPDX_NAMESPACE.licenseConcluded,
        parsing_method=lambda x: parse_license_expression(x, graph, doc_namespace, logger),
    )
    license_declared = parse_literal_or_no_assertion_or_none(
        logger,
        graph,
        package_node,
        SPDX_NAMESPACE.licenseDeclared,
        parsing_method=lambda x: parse_license_expression(x, graph, doc_namespace, logger),
    )
    license_info_from_files = []
    for _, _, license_info_from_files_node in graph.triples((package_node, SPDX_NAMESPACE.licenseInfoFromFiles, None)):
        license_info_from_files.append(
            get_correctly_typed_value(
                logger,
                license_info_from_files_node,
                lambda x: parse_license_expression(x, graph, doc_namespace, logger),
            )
        )
    license_comment = parse_literal(logger, graph, package_node, SPDX_NAMESPACE.licenseComments)
    comment = parse_literal(logger, graph, package_node, RDFS.comment)
    summary = parse_literal(logger, graph, package_node, SPDX_NAMESPACE.summary)
    description = parse_literal(logger, graph, package_node, SPDX_NAMESPACE.description)
    copyright_text = parse_literal_or_no_assertion_or_none(logger, graph, package_node, SPDX_NAMESPACE.copyrightText)
    source_info = parse_literal(logger, graph, package_node, SPDX_NAMESPACE.sourceInfo)
    primary_package_purpose = parse_literal(
        logger,
        graph,
        package_node,
        SPDX_NAMESPACE.primaryPackagePurpose,
        parsing_method=lambda x: parse_enum_value(x, PackagePurpose, SPDX_NAMESPACE.purpose_),
    )
    homepage = parse_literal(logger, graph, package_node, DOAP.homepage)
    attribution_texts = []
    for _, _, attribution_text_literal in get_correctly_typed_triples(
        logger, graph, package_node, SPDX_NAMESPACE.attributionText, None
    ):
        attribution_texts.append(attribution_text_literal.toPython())

    release_date = parse_literal(
        logger, graph, package_node, SPDX_NAMESPACE.releaseDate, parsing_method=datetime_from_str
    )
    built_date = parse_literal(logger, graph, package_node, SPDX_NAMESPACE.builtDate, parsing_method=datetime_from_str)
    valid_until_date = parse_literal(
        logger, graph, package_node, SPDX_NAMESPACE.validUntilDate, parsing_method=datetime_from_str
    )
    raise_parsing_error_if_logger_has_messages(logger, "Package")
    package = construct_or_raise_parsing_error(
        Package,
        dict(
            name=name,
            spdx_id=spdx_id,
            download_location=download_location,
            version=version_info,
            file_name=package_file_name,
            supplier=supplier,
            originator=originator,
            files_analyzed=files_analyzed,
            verification_code=verification_code,
            checksums=checksums,
            homepage=homepage,
            source_info=source_info,
            license_concluded=license_concluded,
            license_info_from_files=license_info_from_files,
            license_declared=license_declared,
            license_comment=license_comment,
            copyright_text=copyright_text,
            summary=summary,
            description=description,
            comment=comment,
            external_references=external_package_refs,
            attribution_texts=attribution_texts,
            primary_package_purpose=primary_package_purpose,
            release_date=release_date,
            built_date=built_date,
            valid_until_date=valid_until_date,
        ),
    )

    return package


def parse_package_verification_code(
    package_verification_code_node: URIRef, graph: Graph
) -> Optional[PackageVerificationCode]:
    logger = Logger()
    value = parse_literal(logger, graph, package_verification_code_node, SPDX_NAMESPACE.packageVerificationCodeValue)
    excluded_files = []
    for _, _, excluded_file_literal in graph.triples(
        (package_verification_code_node, SPDX_NAMESPACE.packageVerificationCodeExcludedFile, None)
    ):
        excluded_files.append(excluded_file_literal.toPython())

    raise_parsing_error_if_logger_has_messages(logger, "PackageVerificationCode")
    package_verification_code = construct_or_raise_parsing_error(
        PackageVerificationCode, dict(value=value, excluded_files=excluded_files)
    )
    return package_verification_code


def parse_external_package_ref(external_package_ref_node: BNode, graph: Graph, doc_namespace) -> ExternalPackageRef:
    logger = Logger()
    ref_locator = parse_literal(logger, graph, external_package_ref_node, SPDX_NAMESPACE.referenceLocator)
    ref_category = parse_literal(
        logger,
        graph,
        external_package_ref_node,
        SPDX_NAMESPACE.referenceCategory,
        parsing_method=lambda x: parse_enum_value(x, ExternalPackageRefCategory, SPDX_NAMESPACE.referenceCategory_),
    )
    ref_type = parse_literal(
        logger,
        graph,
        external_package_ref_node,
        SPDX_NAMESPACE.referenceType,
        parsing_method=lambda x: parse_external_package_ref_type(x, doc_namespace),
    )
    comment = parse_literal(logger, graph, external_package_ref_node, RDFS.comment)

    raise_parsing_error_if_logger_has_messages(logger, "ExternalPackageRef")
    external_package_ref = construct_or_raise_parsing_error(
        ExternalPackageRef, dict(category=ref_category, reference_type=ref_type, locator=ref_locator, comment=comment)
    )
    return external_package_ref


def parse_external_package_ref_type(external_package_ref_type_resource: URIRef, doc_namespace: str) -> str:
    if external_package_ref_type_resource.startswith(doc_namespace):
        return external_package_ref_type_resource.fragment
    if external_package_ref_type_resource.startswith(REFERENCE_NAMESPACE):
        return external_package_ref_type_resource.replace(REFERENCE_NAMESPACE, "")
    return external_package_ref_type_resource.toPython()
