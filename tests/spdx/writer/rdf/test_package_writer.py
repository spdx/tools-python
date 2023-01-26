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
from datetime import datetime

from rdflib import Graph, URIRef, RDF, Literal, XSD, RDFS, DOAP

from spdx.datetime_conversions import datetime_to_iso_string
from spdx.writer.rdf.package_writer import add_package_information_to_graph, add_external_package_ref_to_graph, \
    add_package_verification_code_to_graph
from spdx.writer.rdf.writer_utils import spdx_namespace
from tests.spdx.fixtures import package_fixture, external_package_ref_fixture, package_verification_code_fixture


def test_add_package_information_to_graph():
    graph = Graph()
    package = package_fixture()

    add_package_information_to_graph(package, graph, "anyURI", {})

    assert (URIRef("anyURI#SPDXRef-Package"), RDF.type, spdx_namespace.Package) in graph
    assert (None, spdx_namespace.name, Literal("packageName")) in graph
    assert (None, spdx_namespace.versionInfo, Literal("12.2")) in graph
    assert (None, spdx_namespace.packageFileName, Literal("./packageFileName")) in graph
    assert (None, spdx_namespace.supplier, Literal("Person: supplierName (some@mail.com)")) in graph
    assert (None, spdx_namespace.originator, Literal("Person: originatorName (some@mail.com)")) in graph
    assert (None, spdx_namespace.downloadLocation, Literal("https://download.com")) in graph
    assert (None, spdx_namespace.filesAnalyzed, Literal("true", datatype=XSD.boolean)) in graph
    assert (URIRef("anyURI#SPDXRef-Package"), spdx_namespace.packageVerificationCode, None) in graph
    assert (URIRef("anyURI#SPDXRef-Package"), spdx_namespace.checksum, None) in graph
    assert (None, DOAP.homepage, Literal("https://homepage.com")) in graph
    assert (None, spdx_namespace.sourceInfo, Literal("sourceInfo")) in graph
    assert (None, spdx_namespace.licenseConcluded, Literal("packageLicenseConcluded")) in graph
    assert (None, spdx_namespace.licenseInfoFromFiles, Literal("licenseInfoFromFile")) in graph
    assert (None, spdx_namespace.licenseDeclared, Literal("packageLicenseDeclared")) in graph
    assert (None, spdx_namespace.licenseComments, Literal("packageLicenseComment")) in graph
    assert (None, spdx_namespace.copyrightText, Literal("packageCopyrightText")) in graph
    assert (None, spdx_namespace.summary, Literal("packageSummary")) in graph
    assert (None, spdx_namespace.description, Literal("packageDescription")) in graph
    assert (None, RDFS.comment, Literal("packageComment")) in graph
    assert (URIRef("anyURI#SPDXRef-Package"), spdx_namespace.externalRef, None) in graph
    assert (None, spdx_namespace.attributionText, Literal("packageAttributionText"))
    assert (None, spdx_namespace.primaryPackagePurpose, spdx_namespace.primaryPackagePurpose_source)
    assert (None, spdx_namespace.releaseDate, Literal(datetime_to_iso_string(datetime(2022, 12, 1)))) in graph
    assert (None, spdx_namespace.builtDate, Literal(datetime_to_iso_string(datetime(2022, 12, 2)))) in graph
    assert (None, spdx_namespace.validUntilDate, Literal(datetime_to_iso_string(datetime(2022, 12, 3)))) in graph


def test_add_package_verification_code_to_graph():
    graph = Graph()
    verification_code = package_verification_code_fixture()

    add_package_verification_code_to_graph(verification_code, graph, URIRef("anyURI"))

    assert (None, None, spdx_namespace.PackageVerificationCode) in graph
    assert (None, spdx_namespace.packageVerificationCodeValue,
            Literal("85ed0817af83a24ad8da68c2b5094de69833983c")) in graph
    assert (None, spdx_namespace.packageVerificationCodeExcludedFile, Literal("./exclude.py")) in graph


def test_external_package_ref_to_graph():
    graph = Graph()
    external_reference = external_package_ref_fixture()

    add_external_package_ref_to_graph(graph, external_reference, URIRef("anyURI"))

    assert (None, None, spdx_namespace.ExternalRef) in graph
    assert (None, spdx_namespace.referenceCategory, spdx_namespace.referenceCategory_packageManager) in graph
    assert (None, spdx_namespace.referenceType, Literal("maven-central")) in graph
    assert (None, spdx_namespace.referenceLocator, Literal("org.apache.tomcat:tomcat:9.0.0.M4")) in graph
    assert (None, RDFS.comment, Literal("externalPackageRefComment")) in graph
