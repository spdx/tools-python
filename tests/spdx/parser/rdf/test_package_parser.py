# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import os
from unittest import TestCase

import pytest
from rdflib import RDF, BNode, Graph, Literal, URIRef

from spdx_tools.common.spdx_licensing import spdx_licensing
from spdx_tools.spdx.model import (
    Actor,
    ActorType,
    Checksum,
    ChecksumAlgorithm,
    ExternalPackageRefCategory,
    PackagePurpose,
    PackageVerificationCode,
    SpdxNoAssertion,
)
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.rdf.package_parser import parse_external_package_ref, parse_package
from spdx_tools.spdx.rdfschema.namespace import SPDX_NAMESPACE


def test_package_parser():
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/file_to_test_rdf_parser.rdf.xml"))
    # we have two packages in the test file, graph.value() will return the first package
    package_node = graph.value(predicate=RDF.type, object=SPDX_NAMESPACE.Package)
    doc_namespace = "https://some.namespace"
    assert isinstance(package_node, URIRef)

    package = parse_package(package_node, graph, doc_namespace)

    assert package.spdx_id == "SPDXRef-Package"
    assert package.name == "packageName"
    assert package.download_location == "https://download.com"
    assert package.version == "12.2"
    assert package.file_name == "./packageFileName"
    assert package.homepage == "https://homepage.com"
    assert package.files_analyzed is True
    assert package.checksums == [Checksum(ChecksumAlgorithm.SHA1, "71c4025dd9897b364f3ebbb42c484ff43d00791c")]
    assert package.source_info == "sourceInfo"
    assert package.license_concluded == spdx_licensing.parse("MIT AND GPL-2.0")
    assert package.license_declared == spdx_licensing.parse("MIT AND GPL-2.0")
    TestCase().assertCountEqual(
        package.license_info_from_files,
        [spdx_licensing.parse("MIT"), spdx_licensing.parse("GPL-2.0"), SpdxNoAssertion()],
    )
    assert package.license_comment == "packageLicenseComment"
    assert package.copyright_text == "packageCopyrightText"
    assert package.verification_code == PackageVerificationCode(
        value="85ed0817af83a24ad8da68c2b5094de69833983c", excluded_files=["./exclude.py"]
    )
    assert len(package.external_references) == 1
    assert package.summary == "packageSummary"
    assert package.description == "packageDescription"
    assert package.comment == "packageComment"
    assert package.attribution_texts == ["packageAttributionText"]
    assert package.primary_package_purpose == PackagePurpose.SOURCE
    assert package.supplier == Actor(ActorType.PERSON, "supplierName", "some@mail.com")
    assert package.originator == Actor(ActorType.PERSON, "originatorName", "some@mail.com")


@pytest.mark.parametrize(
    "download_location,category,locator,type,comment",
    [
        (
            "https://download.com",
            ExternalPackageRefCategory.PACKAGE_MANAGER,
            "org.apache.tomcat:tomcat:9.0.0.M4",
            "maven-central",
            "externalPackageRefComment",
        ),
        (
            "http://differentdownload.com",
            ExternalPackageRefCategory.OTHER,
            "acmecorp/acmenator/4.1.3-alpha",
            "LocationRef-acmeforge",
            "This is the external ref for Acme",
        ),
    ],
)
def test_external_package_ref_parser(download_location, category, locator, type, comment):
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/file_to_test_rdf_parser.rdf.xml"))
    doc_namespace = "https://some.namespace"
    # we use the download location to identify the package node
    # in the test file we have two different external package refs depending on the package
    package_node = graph.value(predicate=SPDX_NAMESPACE.downloadLocation, object=Literal(download_location))
    external_package_ref_node = graph.value(package_node, SPDX_NAMESPACE.externalRef)
    assert isinstance(external_package_ref_node, BNode)

    external_package_ref = parse_external_package_ref(external_package_ref_node, graph, doc_namespace)

    assert external_package_ref.category == category
    assert external_package_ref.locator == locator
    assert external_package_ref.reference_type == type
    assert external_package_ref.comment == comment


def test_parse_invalid_package():
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/invalid_documents/file_without_spdx_ids.xml"))
    package_node = graph.value(predicate=RDF.type, object=SPDX_NAMESPACE.Package)
    doc_namespace = "https://some.namespace"

    assert isinstance(package_node, BNode)
    with pytest.raises(SPDXParsingError):
        parse_package(package_node, graph, doc_namespace)
