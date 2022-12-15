from datetime import datetime
from typing import List

import pytest

from src.model.license_expression import LicenseExpression
from src.model.package import Package, PackagePurpose
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.spdx_none import SpdxNone
from src.validation.package_validator import PackageValidator
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType
from tests.valid_defaults import get_checksum, get_external_package_ref, get_actor, get_package_verification_code, \
    get_package, get_document


def test_correct_package():
    package_validator = PackageValidator("2.3", get_document())

    package = Package("SPDXRef-Package", "package name", "www.download.com", "version", "file_name", SpdxNoAssertion(),
                      get_actor(), True,
                      get_package_verification_code(), [get_checksum()], "https://homepage.com", "source_info", None,
                      [LicenseExpression("expression")],
                      SpdxNone(), "comment on license", "copyright", "summary", "description", "comment",
                      [get_external_package_ref()], ["text"], PackagePurpose.OTHER, datetime(2022, 1, 1), None, None)
    validation_messages: List[ValidationMessage] = package_validator.validate_package(package)

    assert validation_messages == []


# TODO: is verification_code required if files_analyzed=True?
@pytest.mark.parametrize("package_input, expected_message",
                         [(get_package(spdx_id="SPDXRef-some_package"),
                           'spdx_id must only contain letters, numbers, "." and "-" and must begin with "SPDXRef-", but is: SPDXRef-some_package'),
                          (get_package(files_analyzed=False, verification_code=get_package_verification_code()),
                           f'verification_code must be None if files_analyzed is False, but is: {get_package_verification_code()}'),
                          (get_package(download_location="bad_download_location"),
                           "download_location must be a valid download location, but is: bad_download_location"),
                          (get_package(homepage="bad_url"),
                           'homepage must be a valid URL, but is: bad_url'),
                          (get_package(files_analyzed=False, license_info_from_files=SpdxNone()),
                           'license_info_from_files must be None if files_analyzed is False, but is: NONE'),
                          (get_package(files_analyzed=False, license_info_from_files=SpdxNoAssertion()),
                           'license_info_from_files must be None if files_analyzed is False, but is: NOASSERTION'),
                          (get_package(files_analyzed=False,
                                       license_info_from_files=[LicenseExpression("some_license")]),
                           'license_info_from_files must be None if files_analyzed is False, but is: [LicenseExpression(expression_string=\'some_license\')]')
                          ])
def test_wrong_package(package_input, expected_message):
    parent_id = "SPDXRef-DOCUMENT"
    package_validator = PackageValidator("2.3", get_document())
    package = package_input
    validation_messages: List[ValidationMessage] = package_validator.validate_package(package)

    expected = ValidationMessage(expected_message,
                                 ValidationContext(spdx_id=package.spdx_id, parent_id=parent_id,
                                                   element_type=SpdxElementType.PACKAGE,
                                                   full_element=package))

    assert validation_messages == [expected]
