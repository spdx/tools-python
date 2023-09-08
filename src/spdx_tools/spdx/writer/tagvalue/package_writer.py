# SPDX-License-Identifier: Apache-2.0
#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from beartype.typing import TextIO

from spdx_tools.spdx.datetime_conversions import datetime_to_iso_string
from spdx_tools.spdx.model import Package, PackageVerificationCode
from spdx_tools.spdx.writer.tagvalue.checksum_writer import write_checksum_to_tag_value
from spdx_tools.spdx.writer.tagvalue.tagvalue_writer_helper_functions import (
    transform_enum_name_to_tv,
    write_actor,
    write_text_value,
    write_value,
)


def write_package(package: Package, text_output: TextIO):
    text_output.write("## Package Information\n")

    write_value("PackageName", package.name, text_output)
    write_value("SPDXID", package.spdx_id, text_output)
    write_value("PackageVersion", package.version, text_output)
    write_value("PackageFileName", package.file_name, text_output)
    write_actor("PackageSupplier", package.supplier, text_output)
    write_actor("PackageOriginator", package.originator, text_output)
    write_value("PackageDownloadLocation", package.download_location, text_output)

    write_value("FilesAnalyzed", str(package.files_analyzed).lower(), text_output)
    if package.verification_code:
        package_verification_code = get_package_verification_code_string(package.verification_code)
        write_value("PackageVerificationCode", package_verification_code, text_output)

    for package_checksum in package.checksums:
        write_value("PackageChecksum", write_checksum_to_tag_value(package_checksum), text_output)

    write_value("PackageHomePage", package.homepage, text_output)
    write_text_value("PackageSourceInfo", package.source_info, text_output)

    write_value("PackageLicenseConcluded", package.license_concluded, text_output)
    for license_info in package.license_info_from_files:
        write_value("PackageLicenseInfoFromFiles", license_info, text_output)
    write_value("PackageLicenseDeclared", package.license_declared, text_output)
    write_text_value("PackageLicenseComments", package.license_comment, text_output)
    write_text_value("PackageCopyrightText", package.copyright_text, text_output)

    write_text_value("PackageSummary", package.summary, text_output)
    write_text_value("PackageDescription", package.description, text_output)
    write_text_value("PackageComment", package.comment, text_output)

    for external_reference in package.external_references:
        external_reference_str = " ".join(
            [
                transform_enum_name_to_tv(external_reference.category.name),
                external_reference.reference_type,
                external_reference.locator,
            ]
        )
        write_value("ExternalRef", external_reference_str, text_output)
        if external_reference.comment:
            write_text_value("ExternalRefComment", external_reference.comment, text_output)

    for attribution_text in package.attribution_texts:
        write_text_value("PackageAttributionText", attribution_text, text_output)

    if package.primary_package_purpose:
        write_value(
            "PrimaryPackagePurpose", transform_enum_name_to_tv(package.primary_package_purpose.name), text_output
        )

    if package.release_date:
        write_value("ReleaseDate", datetime_to_iso_string(package.release_date), text_output)
    if package.built_date:
        write_value("BuiltDate", datetime_to_iso_string(package.built_date), text_output)
    if package.valid_until_date:
        write_value("ValidUntilDate", datetime_to_iso_string(package.valid_until_date), text_output)


def get_package_verification_code_string(verification_code: PackageVerificationCode) -> str:
    if not verification_code.excluded_files:
        return verification_code.value

    excluded_files_str = " (excludes: " + " ".join(verification_code.excluded_files) + ")"
    return verification_code.value + excluded_files_str
