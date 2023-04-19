# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import mock
from unittest.mock import MagicMock

import pytest

from spdx_tools.spdx.jsonschema.external_document_ref_converter import ExternalDocumentRefConverter
from spdx_tools.spdx.jsonschema.external_document_ref_properties import ExternalDocumentRefProperty
from spdx_tools.spdx.model import Checksum, ChecksumAlgorithm, ExternalDocumentRef


@pytest.fixture
@mock.patch("spdx_tools.spdx.jsonschema.checksum_converter.ChecksumConverter", autospec=True)
def converter(checksum_converter_magic_mock: MagicMock) -> ExternalDocumentRefConverter:
    mocked_checksum_converter = checksum_converter_magic_mock()
    converter = ExternalDocumentRefConverter()
    converter.checksum_converter = mocked_checksum_converter
    return converter


@pytest.mark.parametrize(
    "external_document_ref_property,expected",
    [
        (ExternalDocumentRefProperty.EXTERNAL_DOCUMENT_ID, "externalDocumentId"),
        (ExternalDocumentRefProperty.SPDX_DOCUMENT, "spdxDocument"),
        (ExternalDocumentRefProperty.CHECKSUM, "checksum"),
    ],
)
def test_json_property_names(
    converter: ExternalDocumentRefConverter, external_document_ref_property: ExternalDocumentRefProperty, expected: str
):
    assert converter.json_property_name(external_document_ref_property) == expected


def test_successful_conversion(converter: ExternalDocumentRefConverter):
    converter.checksum_converter.convert.return_value = "mock_converted_checksum"
    checksum = Checksum(ChecksumAlgorithm.SHA1, "123")
    external_document_ref = ExternalDocumentRef("document_ref_id", "document_uri", checksum)

    converted_dict = converter.convert(external_document_ref)

    assert converted_dict == {
        converter.json_property_name(ExternalDocumentRefProperty.EXTERNAL_DOCUMENT_ID): "document_ref_id",
        converter.json_property_name(ExternalDocumentRefProperty.SPDX_DOCUMENT): "document_uri",
        converter.json_property_name(ExternalDocumentRefProperty.CHECKSUM): "mock_converted_checksum",
    }


def test_json_type(converter: ExternalDocumentRefConverter):
    assert converter.get_json_type() == ExternalDocumentRefProperty


def test_data_model_type(converter: ExternalDocumentRefConverter):
    assert converter.get_data_model_type() == ExternalDocumentRef
