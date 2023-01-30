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
from spdx.writer.rdf.writer_utils import spdx_namespace, add_literal_value, add_literal_or_no_assertion_or_none, \
    add_datetime_to_graph, add_namespace_to_spdx_id


def add_package_information_to_graph(package: Package, graph: Graph, doc_namespace: str,
                                     external_doc_ref_to_namespace: Dict[str, str]):
    package_resource = URIRef(add_namespace_to_spdx_id(package.spdx_id, doc_namespace, external_doc_ref_to_namespace))
    graph.add((package_resource, RDF.type, spdx_namespace.Package))

    graph.add((package_resource, spdx_namespace.name, Literal(package.name)))
    add_literal_value(graph, package_resource, spdx_namespace.versionInfo, package.version)
    add_literal_value(graph, package_resource, spdx_namespace.packageFileName, package.file_name)
    add_literal_value(graph, package_resource, spdx_namespace.supplier, package.supplier)
    add_literal_value(graph, package_resource, spdx_namespace.originator, package.originator)
    add_literal_or_no_assertion_or_none(graph, package_resource, spdx_namespace.downloadLocation,
                                        package.download_location)
    graph.add((package_resource, spdx_namespace.filesAnalyzed, Literal(package.files_analyzed, datatype=XSD.boolean)))
    add_package_verification_code_to_graph(package.verification_code, graph, package_resource)
    for checksum in package.checksums:
        add_checksum_information_to_graph(checksum, graph, package_resource)

    add_literal_value(graph, package_resource, DOAP.homepage, package.homepage)
    add_literal_value(graph, package_resource, spdx_namespace.sourceInfo, package.source_info)
    add_license_expression_or_none_or_no_assertion(graph, package_resource, spdx_namespace.licenseConcluded,
                                                   package.license_concluded,
                                                   doc_namespace)
    add_license_expression_or_none_or_no_assertion(graph, package_resource, spdx_namespace.licenseInfoFromFiles,
                                                   package.license_info_from_files, doc_namespace)
    add_license_expression_or_none_or_no_assertion(graph, package_resource, spdx_namespace.licenseDeclared,
                                                   package.license_declared, doc_namespace)
    add_literal_value(graph, package_resource, spdx_namespace.licenseComments, package.license_comment)
    add_literal_value(graph, package_resource, spdx_namespace.copyrightText, package.copyright_text)
    add_literal_value(graph, package_resource, spdx_namespace.summary, package.summary)
    add_literal_value(graph, package_resource, spdx_namespace.description, package.description)
    add_literal_value(graph, package_resource, RDFS.comment, package.comment)
    for external_reference in package.external_references:
        add_external_package_ref_to_graph(graph, external_reference, package_resource)
    for attribution_text in package.attribution_texts:
        add_literal_value(graph, package_resource, spdx_namespace.attributionText, attribution_text)
    if package.primary_package_purpose:
        graph.add((package_resource, spdx_namespace.primaryPackagePurpose,
                   spdx_namespace[f"purpose_{snake_case_to_camel_case(package.primary_package_purpose.name)}"]))

    add_datetime_to_graph(graph, package_resource, spdx_namespace.releaseDate, package.release_date)
    add_datetime_to_graph(graph, package_resource, spdx_namespace.builtDate, package.built_date)
    add_datetime_to_graph(graph, package_resource, spdx_namespace.validUntilDate, package.valid_until_date)


def add_package_verification_code_to_graph(package_verification_code: PackageVerificationCode, graph: Graph,
                                           package_resource: URIRef):
    if not package_verification_code:
        return
    package_verification_code_node = BNode()
    graph.add((package_verification_code_node, RDF.type, spdx_namespace.PackageVerificationCode))
    graph.add((package_verification_code_node, spdx_namespace.packageVerificationCodeValue,
               Literal(package_verification_code.value)))
    for excluded_file in package_verification_code.excluded_files:
        graph.add((package_verification_code_node, spdx_namespace.packageVerificationCodeExcludedFile,
                   Literal(excluded_file)))

    graph.add((package_resource, spdx_namespace.packageVerificationCode, package_verification_code_node))


def add_external_package_ref_to_graph(graph: Graph, external_package_ref: ExternalPackageRef,
                                      package_resource: URIRef):
    external_package_ref_node = BNode()
    graph.add((external_package_ref_node, RDF.type, spdx_namespace.ExternalRef))
    graph.add((external_package_ref_node, spdx_namespace.referenceCategory,
               spdx_namespace[f"referenceCategory_{snake_case_to_camel_case(external_package_ref.category.name)}"]))

    if external_package_ref.reference_type in CATEGORY_TO_EXTERNAL_PACKAGE_REF_TYPES[external_package_ref.category]:
        graph.add((external_package_ref_node, spdx_namespace.referenceType,
                   URIRef(f"http://spdx.org/rdf/references/{external_package_ref.reference_type}")))
    else:
        graph.add((external_package_ref_node, spdx_namespace.referenceType,
                   URIRef(external_package_ref.reference_type)))
    graph.add((external_package_ref_node, spdx_namespace.referenceLocator, Literal(external_package_ref.locator)))
    if external_package_ref.comment:
        graph.add((external_package_ref_node, RDFS.comment, Literal(external_package_ref.comment)))

    graph.add((package_resource, spdx_namespace.externalRef, external_package_ref_node))
