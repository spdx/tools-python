# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx.jsonschema.extracted_licensing_info_converter import ExtractedLicensingInfoConverter
from spdx_tools.spdx.jsonschema.extracted_licensing_info_properties import ExtractedLicensingInfoProperty
from spdx_tools.spdx.model import ExtractedLicensingInfo, SpdxNoAssertion
from spdx_tools.spdx.model.spdx_no_assertion import SPDX_NO_ASSERTION_STRING
from tests.spdx.fixtures import extracted_licensing_info_fixture


@pytest.fixture
def converter() -> ExtractedLicensingInfoConverter:
    return ExtractedLicensingInfoConverter()


@pytest.mark.parametrize(
    "extracted_licensing_info_property,expected",
    [
        (ExtractedLicensingInfoProperty.LICENSE_ID, "licenseId"),
        (ExtractedLicensingInfoProperty.EXTRACTED_TEXT, "extractedText"),
        (ExtractedLicensingInfoProperty.NAME, "name"),
        (ExtractedLicensingInfoProperty.COMMENT, "comment"),
        (ExtractedLicensingInfoProperty.SEE_ALSOS, "seeAlsos"),
    ],
)
def test_json_property_names(
    converter: ExtractedLicensingInfoConverter,
    extracted_licensing_info_property: ExtractedLicensingInfoProperty,
    expected: str,
):
    assert converter.json_property_name(extracted_licensing_info_property) == expected


def test_json_type(converter: ExtractedLicensingInfoConverter):
    assert converter.get_json_type() == ExtractedLicensingInfoProperty


def test_data_model_type(converter: ExtractedLicensingInfoConverter):
    assert converter.get_data_model_type() == ExtractedLicensingInfo


def test_successful_conversion(converter: ExtractedLicensingInfoConverter):
    extracted_licensing_info = ExtractedLicensingInfo(
        license_id="licenseId",
        extracted_text="Extracted text",
        license_name="license name",
        cross_references=["reference1", "reference2"],
        comment="comment",
    )

    converted_dict = converter.convert(extracted_licensing_info)

    assert converted_dict == {
        converter.json_property_name(ExtractedLicensingInfoProperty.LICENSE_ID): "licenseId",
        converter.json_property_name(ExtractedLicensingInfoProperty.EXTRACTED_TEXT): "Extracted text",
        converter.json_property_name(ExtractedLicensingInfoProperty.NAME): "license name",
        converter.json_property_name(ExtractedLicensingInfoProperty.SEE_ALSOS): ["reference1", "reference2"],
        converter.json_property_name(ExtractedLicensingInfoProperty.COMMENT): "comment",
    }


def test_null_values(converter: ExtractedLicensingInfoConverter):
    extracted_licensing_info = ExtractedLicensingInfo(cross_references=[])

    converted_dict = converter.convert(extracted_licensing_info)

    assert converter.json_property_name(ExtractedLicensingInfoProperty.LICENSE_ID) not in converted_dict
    assert converter.json_property_name(ExtractedLicensingInfoProperty.EXTRACTED_TEXT) not in converted_dict
    assert converter.json_property_name(ExtractedLicensingInfoProperty.NAME) not in converted_dict
    assert converter.json_property_name(ExtractedLicensingInfoProperty.SEE_ALSOS) not in converted_dict
    assert converter.json_property_name(ExtractedLicensingInfoProperty.COMMENT) not in converted_dict


def test_spdx_no_assertion(converter: ExtractedLicensingInfoConverter):
    extracted_licensing_info = extracted_licensing_info_fixture(license_name=SpdxNoAssertion())

    converted_dict = converter.convert(extracted_licensing_info)

    assert (
        converted_dict[converter.json_property_name(ExtractedLicensingInfoProperty.NAME)] == SPDX_NO_ASSERTION_STRING
    )
