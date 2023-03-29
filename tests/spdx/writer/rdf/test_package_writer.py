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
import pytest
from rdflib import Graph, URIRef, RDF, Literal, XSD, RDFS, DOAP
from spdx.model.package import ExternalPackageRefCategory

from spdx.datetime_conversions import datetime_to_iso_string
from spdx.writer.rdf.package_writer import add_package_to_graph, add_external_package_ref_to_graph, \
    add_package_verification_code_to_graph
from spdx.rdfschema.namespace import SPDX_NAMESPACE, LICENSE_NAMESPACE
from tests.spdx.fixtures import package_fixture, external_package_ref_fixture, package_verification_code_fixture


def test_add_package_to_graph():
    graph = Graph()
    package = package_fixture()

    add_package_to_graph(package, graph, "docNamespace", {})

    assert (URIRef("docNamespace#SPDXRef-Package"), RDF.type, SPDX_NAMESPACE.Package) in graph
    assert (None, SPDX_NAMESPACE.name, Literal(package.name)) in graph
    assert (None, SPDX_NAMESPACE.versionInfo, Literal(package.version)) in graph
    assert (None, SPDX_NAMESPACE.packageFileName, Literal(package.file_name)) in graph
    assert (None, SPDX_NAMESPACE.supplier, Literal(package.supplier.to_serialized_string())) in graph
    assert (None, SPDX_NAMESPACE.originator, Literal(package.originator.to_serialized_string())) in graph
    assert (None, SPDX_NAMESPACE.downloadLocation, Literal(package.download_location)) in graph
    assert (None, SPDX_NAMESPACE.filesAnalyzed, Literal(package.files_analyzed, datatype=XSD.boolean)) in graph
    assert (URIRef("docNamespace#SPDXRef-Package"), SPDX_NAMESPACE.packageVerificationCode, None) in graph
    assert (URIRef("docNamespace#SPDXRef-Package"), SPDX_NAMESPACE.checksum, None) in graph
    assert (None, DOAP.homepage, Literal(package.homepage)) in graph
    assert (None, SPDX_NAMESPACE.sourceInfo, Literal(package.source_info)) in graph
    assert (None, SPDX_NAMESPACE.licenseConcluded, None) in graph
    assert (None, SPDX_NAMESPACE.licenseInfoFromFiles, LICENSE_NAMESPACE.MIT) in graph
    assert (None, SPDX_NAMESPACE.licenseInfoFromFiles, LICENSE_NAMESPACE["GPL-2.0-only"]) in graph
    assert (None, SPDX_NAMESPACE.licenseInfoFromFiles, SPDX_NAMESPACE.noassertion) in graph
    assert (None, SPDX_NAMESPACE.licenseDeclared, None) in graph
    assert (None, SPDX_NAMESPACE.licenseComments, Literal(package.license_comment)) in graph
    assert (None, SPDX_NAMESPACE.copyrightText, Literal(package.copyright_text)) in graph
    assert (None, SPDX_NAMESPACE.summary, Literal(package.summary)) in graph
    assert (None, SPDX_NAMESPACE.description, Literal(package.description)) in graph
    assert (None, RDFS.comment, Literal(package.comment)) in graph
    assert (URIRef("docNamespace#SPDXRef-Package"), SPDX_NAMESPACE.externalRef, None) in graph
    assert (None, SPDX_NAMESPACE.attributionText, Literal(package.attribution_texts[0])) in graph
    assert (None, SPDX_NAMESPACE.primaryPackagePurpose, SPDX_NAMESPACE.purpose_source) in graph
    assert (None, SPDX_NAMESPACE.releaseDate, Literal(datetime_to_iso_string(package.release_date))) in graph
    assert (None, SPDX_NAMESPACE.builtDate, Literal(datetime_to_iso_string(package.built_date))) in graph
    assert (None, SPDX_NAMESPACE.validUntilDate, Literal(datetime_to_iso_string(package.valid_until_date))) in graph


def test_add_package_verification_code_to_graph():
    graph = Graph()
    verification_code = package_verification_code_fixture()

    add_package_verification_code_to_graph(verification_code, graph, URIRef("docNamespace"))

    assert (None, RDF.type, SPDX_NAMESPACE.PackageVerificationCode) in graph
    assert (None, SPDX_NAMESPACE.packageVerificationCodeValue,
            Literal("85ed0817af83a24ad8da68c2b5094de69833983c")) in graph
    assert (None, SPDX_NAMESPACE.packageVerificationCodeExcludedFile, Literal("./exclude.py")) in graph


@pytest.mark.parametrize("external_reference,ref_type,category",
                         [(external_package_ref_fixture(), URIRef("http://spdx.org/rdf/references/maven-central"),
                           SPDX_NAMESPACE.referenceCategory_packageManager),
                          (external_package_ref_fixture(locator="acmecorp/acmenator/4.1.3-alpha",
                                                        category=ExternalPackageRefCategory.OTHER,
                                                        reference_type="LocationRef-acmeforge",
                                                        comment="This is the external ref for Acme"),
                           URIRef("https://some.namespace#LocationRef-acmeforge"),
                           SPDX_NAMESPACE.referenceCategory_other)])
def test_external_package_ref_to_graph(external_reference, ref_type, category):
    graph = Graph()
    doc_namespace = "https://some.namespace"
    add_external_package_ref_to_graph(external_reference, graph, URIRef("docNamespace"), doc_namespace)

    assert (None, RDF.type, SPDX_NAMESPACE.ExternalRef) in graph
    assert (None, SPDX_NAMESPACE.referenceCategory, category) in graph
    assert (None, SPDX_NAMESPACE.referenceType, ref_type) in graph
    assert (None, SPDX_NAMESPACE.referenceLocator, Literal(external_reference.locator)) in graph
    assert (None, RDFS.comment, Literal(external_reference.comment)) in graph
