import os
from typing import Optional
from unittest import TestCase

import pytest
from rdflib import URIRef

from spdx.document import Document
from spdx.license import License
from spdx.package import Package, ExternalPackageRef
from spdx.parsers.loggers import StandardLogger
from spdx.parsers.parse_anything import parse_file
from spdx.parsers.rdf import Parser
from spdx.parsers.rdfbuilders import Builder
from spdx.utils import NoAssert
from spdx.writers.rdf import Writer


@pytest.fixture
def temporary_file_path() -> str:
    temporary_file_path = "temp_accept_provided_doc_node.rdf.xml"
    yield temporary_file_path
    os.remove(temporary_file_path)


# This test is really clunky since it's hard to isolate features of the rdf writer to test. Should be improved when
# that part is refactored.
def test_accept_provided_doc_node(temporary_file_path) -> None:
    doc_node = URIRef("http://www.spdx.org/tools#SPDXRef-DOCUMENT")
    document: Document = minimal_document_with_package()

    with open(temporary_file_path, "wb") as out:
        writer = Writer(document, out)
        writer.write(doc_node)
    parser = Parser(Builder(), StandardLogger())
    with open(temporary_file_path, "r") as file:
        parsed_document: Document = parser.parse(file)[0]

    # These properties are set automatically if no doc_node is provided. Instead, we provided an empty one
    assert parsed_document.data_license is None
    assert parsed_document.namespace is None
    assert parsed_document.spdx_id is None


def test_external_package_references(temporary_file_path) -> None:
    document: Document = minimal_document_with_package()
    package: Package = document.packages[0]
    first_ref = ExternalPackageRef(category="PACKAGE-MANAGER")
    second_ref = ExternalPackageRef(category="SECURITY")
    package.add_pkg_ext_refs(first_ref)
    package.add_pkg_ext_refs(second_ref)

    # Not using write_anything here because we don't want to deal with validation
    with open(temporary_file_path, "wb") as out:
        writer = Writer(document, out)
        writer.write()

    parsed_document = parse_file(temporary_file_path)[0]
    parsed_package: Package = parsed_document.packages[0]

    assert len(parsed_package.pkg_ext_refs) is 2
    parsed_reference_categories = list(map(lambda x: x.category, parsed_package.pkg_ext_refs))
    assert first_ref.category in parsed_reference_categories
    assert second_ref.category in parsed_reference_categories


# This test is really clunky since it's hard to isolate features of the rdf writer to test. Should be improved when
# that part is refactored.
def test_multiple_packages_in_one_document(temporary_file_path) -> None:
    doc_node = URIRef("http://www.spdx.org/tools#SPDXRef-DOCUMENT")
    document = Document()
    document.creation_info.set_created_now()
    package = Package()
    package.spdx_id = "SPDXRef-Package"
    package.version = "2.1"
    document.add_package(package)
    package2 = Package()
    package2.spdx_id = "SPDXRef-Another-Package"
    package2.version = "2.3"
    document.add_package(package2)

    with open(temporary_file_path, "wb") as out:
        writer = Writer(document, out)
        writer.write(doc_node)
    parser = Parser(Builder(), StandardLogger())
    with open(temporary_file_path, "r") as file:
        parsed_document: Document = parser.parse(file)[0]

    assert len(parsed_document.packages) == 2
    first_package = get_package_by_spdx_id("SPDXRef-Package", document)
    assert first_package.version == "2.1"
    second_package = get_package_by_spdx_id("SPDXRef-Another-Package", document)
    assert second_package.version == "2.3"


def minimal_document_with_package() -> Document:
    document = Document(data_license=License.from_identifier('CC0-1.0'))
    document.creation_info.set_created_now()
    package: Package = minimal_package()
    document.add_package(package)
    return document


def minimal_package() -> Package:
    package = Package()
    package.spdx_id = "SPDXRef-Package"
    package.conc_lics = NoAssert()
    package.license_declared = NoAssert()
    package.add_lics_from_file(NoAssert())
    return package


def get_package_by_spdx_id(package_spdx_id: str, document: Document) -> Optional[Package]:
    for package in document.packages:
        if package.spdx_id == package_spdx_id:
            return package
    return None
