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
from typing import Dict

from rdflib import Graph, URIRef, RDF, Literal, XSD, BNode, DOAP, RDFS
from spdx.writer.rdf.license_expression_writer import add_license_expression_or_none_or_no_assertion

from spdx.writer.casing_tools import snake_case_to_camel_case
from spdx.writer.rdf.checksum_writer import add_checksum_information_to_graph

from spdx.model.package import Package, PackageVerificationCode, ExternalPackageRef, \
    CATEGORY_TO_EXTERNAL_PACKAGE_REF_TYPES
from spdx.writer.rdf.writer_utils import SPDX_NAMESPACE, add_optional_literal, add_literal_or_no_assertion_or_none, \
    add_datetime_to_graph, add_namespace_to_spdx_id


def add_package_information_to_graph(package: Package, graph: Graph, doc_namespace: str,
                                     external_doc_ref_to_namespace: Dict[str, str]):
    package_resource = URIRef(add_namespace_to_spdx_id(package.spdx_id, doc_namespace, external_doc_ref_to_namespace))
    graph.add((package_resource, RDF.type, SPDX_NAMESPACE.Package))

    graph.add((package_resource, SPDX_NAMESPACE.name, Literal(package.name)))
    add_optional_literal(graph, package_resource, SPDX_NAMESPACE.versionInfo, package.version)
    add_optional_literal(graph, package_resource, SPDX_NAMESPACE.packageFileName, package.file_name)
    add_optional_literal(graph, package_resource, SPDX_NAMESPACE.supplier, package.supplier)
    add_optional_literal(graph, package_resource, SPDX_NAMESPACE.originator, package.originator)
    add_literal_or_no_assertion_or_none(graph, package_resource, SPDX_NAMESPACE.downloadLocation,
                                        package.download_location)
    graph.add((package_resource, SPDX_NAMESPACE.filesAnalyzed, Literal(package.files_analyzed, datatype=XSD.boolean)))
    add_package_verification_code_to_graph(package.verification_code, graph, package_resource)
    for checksum in package.checksums:
        add_checksum_information_to_graph(checksum, graph, package_resource)

    add_optional_literal(graph, package_resource, DOAP.homepage, package.homepage)
    add_optional_literal(graph, package_resource, SPDX_NAMESPACE.sourceInfo, package.source_info)
    add_license_expression_or_none_or_no_assertion(graph, package_resource, SPDX_NAMESPACE.licenseConcluded,
                                                   package.license_concluded,
                                                   doc_namespace)
    add_license_expression_or_none_or_no_assertion(graph, package_resource, SPDX_NAMESPACE.licenseInfoFromFiles,
                                                   package.license_info_from_files, doc_namespace)
    add_license_expression_or_none_or_no_assertion(graph, package_resource, SPDX_NAMESPACE.licenseDeclared,
                                                   package.license_declared, doc_namespace)
    add_optional_literal(graph, package_resource, SPDX_NAMESPACE.licenseComments, package.license_comment)
    add_optional_literal(graph, package_resource, SPDX_NAMESPACE.copyrightText, package.copyright_text)
    add_optional_literal(graph, package_resource, SPDX_NAMESPACE.summary, package.summary)
    add_optional_literal(graph, package_resource, SPDX_NAMESPACE.description, package.description)
    add_optional_literal(graph, package_resource, RDFS.comment, package.comment)
    for external_reference in package.external_references:
        add_external_package_ref_to_graph(graph, external_reference, package_resource)
    for attribution_text in package.attribution_texts:
        add_optional_literal(graph, package_resource, SPDX_NAMESPACE.attributionText, attribution_text)
    if package.primary_package_purpose:
        graph.add((package_resource, SPDX_NAMESPACE.primaryPackagePurpose,
                   SPDX_NAMESPACE[f"purpose_{snake_case_to_camel_case(package.primary_package_purpose.name)}"]))

    add_datetime_to_graph(graph, package_resource, SPDX_NAMESPACE.releaseDate, package.release_date)
    add_datetime_to_graph(graph, package_resource, SPDX_NAMESPACE.builtDate, package.built_date)
    add_datetime_to_graph(graph, package_resource, SPDX_NAMESPACE.validUntilDate, package.valid_until_date)


def add_package_verification_code_to_graph(package_verification_code: PackageVerificationCode, graph: Graph,
                                           package_resource: URIRef):
    if not package_verification_code:
        return
    package_verification_code_node = BNode()
    graph.add((package_verification_code_node, RDF.type, SPDX_NAMESPACE.PackageVerificationCode))
    graph.add((package_verification_code_node, SPDX_NAMESPACE.packageVerificationCodeValue,
               Literal(package_verification_code.value)))
    for excluded_file in package_verification_code.excluded_files:
        graph.add((package_verification_code_node, SPDX_NAMESPACE.packageVerificationCodeExcludedFile,
                   Literal(excluded_file)))

    graph.add((package_resource, SPDX_NAMESPACE.packageVerificationCode, package_verification_code_node))


def add_external_package_ref_to_graph(graph: Graph, external_package_ref: ExternalPackageRef,
                                      package_resource: URIRef):
    external_package_ref_node = BNode()
    graph.add((external_package_ref_node, RDF.type, SPDX_NAMESPACE.ExternalRef))
    graph.add((external_package_ref_node, SPDX_NAMESPACE.referenceCategory,
               SPDX_NAMESPACE[f"referenceCategory_{snake_case_to_camel_case(external_package_ref.category.name)}"]))

    if external_package_ref.reference_type in CATEGORY_TO_EXTERNAL_PACKAGE_REF_TYPES[external_package_ref.category]:
        graph.add((external_package_ref_node, SPDX_NAMESPACE.referenceType,
                   URIRef(f"http://spdx.org/rdf/references/{external_package_ref.reference_type}")))
    else:
        graph.add((external_package_ref_node, SPDX_NAMESPACE.referenceType,
                   URIRef(external_package_ref.reference_type)))
    graph.add((external_package_ref_node, SPDX_NAMESPACE.referenceLocator, Literal(external_package_ref.locator)))
    if external_package_ref.comment:
        graph.add((external_package_ref_node, RDFS.comment, Literal(external_package_ref.comment)))

    graph.add((package_resource, SPDX_NAMESPACE.externalRef, external_package_ref_node))
