import os

import pytest

from spdx.document import Document
from spdx.package import Package, ExternalPackageRef
from spdx.parsers.parse_anything import parse_file
from spdx.writers import json
from tests.test_rdf_writer import minimal_document


@pytest.fixture
def temporary_file_path() -> str:
    temporary_file_path = "temp_external_references.json"
    yield temporary_file_path
    os.remove(temporary_file_path)


def test_external_package_references(temporary_file_path) -> None:
    document: Document = minimal_document()
    package: Package = document.packages[0]
    first_ref = ExternalPackageRef(category="PACKAGE-MANAGER")
    second_ref = ExternalPackageRef(category="SECURITY")
    package.add_pkg_ext_refs(first_ref)
    package.add_pkg_ext_refs(second_ref)

    with open(temporary_file_path, "w") as out:
        json.write_document(document, out, validate=False)

    parsed_document = parse_file(temporary_file_path)[0]

    written_package: Package = parsed_document.packages[0]
    assert len(written_package.pkg_ext_refs) is 2
    written_reference_categories = list(map(lambda x: x.category, written_package.pkg_ext_refs))
    assert first_ref.category in written_reference_categories
    assert second_ref.category in written_reference_categories
