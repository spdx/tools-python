from datetime import datetime
from typing import List
from unittest import mock

from src.model.license_expression import LicenseExpression
from src.model.package import Package, PackagePurpose
from src.model.spdx_no_assertion import SpdxNoAssertion
from src.model.spdx_none import SpdxNone
from src.validation.package_validator import PackageValidator
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


@mock.patch('src.model.actor.Actor', autospec=True)
@mock.patch('src.model.package.PackageVerificationCode', autospec=True)
@mock.patch('src.model.checksum.Checksum', autospec=True)
@mock.patch('src.model.package.ExternalPackageReference', autospec=True)
def test_correct_package(actor, verif_code, checksum, ext_ref):
    package_validator = PackageValidator("2.3")

    package = Package("id", "name", SpdxNoAssertion(), "version", "file_name", SpdxNoAssertion(), actor, True,
                      verif_code, [checksum], "homepage", "source_info", None, [LicenseExpression("expression")],
                      SpdxNone(), "comment on license", "copyright", "summary", "description", "comment",
                      [ext_ref, ext_ref], ["text"], PackagePurpose.OTHER, datetime(2022, 1, 1), None, None)
    validation_messages: List[ValidationMessage] = package_validator.validate_package(package)

    assert validation_messages == []
