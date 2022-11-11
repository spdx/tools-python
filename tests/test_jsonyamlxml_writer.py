import glob
import os
from datetime import datetime
from typing import List

import pytest

from spdx.document import Document
from spdx.package import Package, ExternalPackageRef, PackagePurpose
from spdx.parsers.parse_anything import parse_file
from spdx.snippet import Snippet
from spdx.writers import json, write_anything
from tests.test_rdf_writer import minimal_document

tested_formats: List[str] = ['yaml', 'xml', 'json']


@pytest.fixture
def temporary_file_path() -> str:
    temporary_file_path = "temp_test_writer_output"
    yield temporary_file_path
    file_with_ending = glob.glob(temporary_file_path + "*")
    for file in file_with_ending:
        os.remove(file)


@pytest.mark.parametrize("out_format", tested_formats)
def test_external_package_references(temporary_file_path: str, out_format: str) -> None:
    document: Document = minimal_document()
    package: Package = document.packages[0]
    first_ref = ExternalPackageRef(category="PACKAGE-MANAGER")
    second_ref = ExternalPackageRef(category="SECURITY")
    package.add_pkg_ext_refs(first_ref)
    package.add_pkg_ext_refs(second_ref)

    file_path_with_ending = temporary_file_path + "." + out_format
    write_anything.write_file(document, file_path_with_ending, validate=False)

    parsed_document = parse_file(file_path_with_ending)[0]

    parsed_package: Package = parsed_document.packages[0]
    assert len(parsed_package.pkg_ext_refs) is 2
    written_reference_categories = list(map(lambda x: x.category, parsed_package.pkg_ext_refs))
    assert first_ref.category in written_reference_categories
    assert second_ref.category in written_reference_categories


@pytest.mark.parametrize("out_format", tested_formats)
def test_primary_package_purpose(temporary_file_path: str, out_format: str):
    document: Document = minimal_document()
    package: Package = document.packages[0]
    package.primary_package_purpose = PackagePurpose.OPERATING_SYSTEM

    file_path_with_ending = temporary_file_path + "." + out_format
    write_anything.write_file(document, file_path_with_ending, validate=False)

    parsed_document: Document = parse_file(file_path_with_ending)[0]
    parsed_package: Package = parsed_document.packages[0]

    assert parsed_package.primary_package_purpose == PackagePurpose.OPERATING_SYSTEM


@pytest.mark.parametrize("out_format", tested_formats)
def test_release_built_valid_until_date(temporary_file_path: str, out_format: str):
    document: Document = minimal_document()
    package: Package = document.packages[0]
    package.release_date = datetime(2021, 1, 1, 12, 0, 0)
    package.built_date = datetime(2021, 1, 1, 12, 0, 0)
    package.valid_until_date = datetime(2022, 1, 1, 12, 0, 0)

    file_path_with_ending = temporary_file_path + "." + out_format
    write_anything.write_file(document, file_path_with_ending, validate=False)

    parsed_document: Document = parse_file(file_path_with_ending)[0]
    parsed_package: Package = parsed_document.packages[0]

    assert parsed_package.release_date == package.release_date
    assert parsed_package.built_date == package.built_date
    assert parsed_package.valid_until_date == package.valid_until_date


@pytest.mark.parametrize("out_format", ['yaml', 'xml', 'json'])
def test_snippet_byte_range(temporary_file_path, out_format):
    snippet = minimal_snippet()
    parsed_snippet = write_and_parse_snippet(out_format, snippet, temporary_file_path)

    assert parsed_snippet.byte_range == (310, 420)
    assert parsed_snippet.line_range is None


@pytest.mark.parametrize("out_format", ['yaml', 'xml', 'json'])
def test_snippet_ranges(temporary_file_path, out_format):
    snippet = minimal_snippet()
    snippet.line_range = (5, 23)
    parsed_snippet = write_and_parse_snippet(out_format, snippet, temporary_file_path)

    assert parsed_snippet.byte_range == (310, 420)
    assert parsed_snippet.line_range == (5, 23)


def minimal_snippet():
    snippet = Snippet()
    snippet.spdx_id = "SPDXRef-Snippet"
    snippet.snip_from_file_spdxid = "SPDXRef-File"
    snippet.byte_range = (310, 420)
    return snippet


def write_and_parse_snippet(out_format, snippet, temporary_file_path):
    document: Document = minimal_document()
    document.add_snippet(snippet)
    file_path_with_ending = temporary_file_path + "." + out_format
    write_anything.write_file(document, file_path_with_ending, validate=False)
    parsed_document: Document = parse_file(file_path_with_ending)[0]
    parsed_snippet: Snippet = parsed_document.snippet[0]

    return parsed_snippet

