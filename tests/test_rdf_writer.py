import os

import pytest
from rdflib import URIRef

from spdx.document import Document
from spdx.package import Package
from spdx.parsers.loggers import StandardLogger
from spdx.parsers.rdf import Parser
from spdx.parsers.rdfbuilders import Builder
from spdx.utils import NoAssert
from spdx.writers.rdf import Writer


@pytest.fixture
def temporary_file_path():
    temporary_file_path = "temp_accept_provided_doc_node.rdf.xml"
    yield temporary_file_path
    os.remove(temporary_file_path)


# This test is really clunky since it's hard to isolate features of the rdf writer to test. Should be improved when
# that part is refactored.
def test_accept_provided_doc_node(temporary_file_path) -> None:
    doc_node = URIRef("http://www.spdx.org/tools#SPDXRef-DOCUMENT")
    document: Document = minimal_document()

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


def minimal_document() -> Document:
    document = Document()
    document.creation_info.set_created_now()
    package: Package = minimal_package()
    document.add_package(package)
    return document


def minimal_package() -> Package:
    package = Package()
    package.conc_lics = NoAssert()
    package.license_declared = NoAssert()
    package.add_lics_from_file(NoAssert())
    return package
