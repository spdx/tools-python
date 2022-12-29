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
from typing import TextIO

from src.datetime_conversions import datetime_to_iso_string
from src.model.package import Package, PackageVerificationCode
from src.writer.tagvalue.tagvalue_writer_helper_functions import write_value, write_text_value, \
    write_field_or_none_or_no_assertion, transform_enum_name_to_tv, write_actor_or_no_assertion
from src.writer.tagvalue.checksum_writer import write_checksum_to_tag_value


def write_package(package: Package, text_output: TextIO):
    """
    Write all package information to text_output.
    """
    text_output.write("## Package Information\n")

    write_value("PackageName", package.name, text_output, True)
    write_value("SPDXID", package.spdx_id, text_output, True)
    write_value("PackageVersion", package.version, text_output, True)
    write_value("PackageDownloadLocation", package.download_location, text_output)
    write_value("FilesAnalyzed", package.files_analyzed, text_output, True)
    write_text_value("PackageSummary", package.summary, text_output, True)
    for attribution_text in package.attribution_texts:
        write_text_value("PackageAttributionText", attribution_text, text_output)

    write_text_value("PackageSourceInfo", package.source_info, text_output, True)
    write_value("PackageFileName", package.file_name, text_output, True)
    write_actor_or_no_assertion("PackageSupplier", package.supplier, text_output, True)
    write_actor_or_no_assertion("PackageOriginator", package.originator, text_output, True)

    for package_checksum in package.checksums:
        write_value("PackageChecksum", write_checksum_to_tag_value(package_checksum), text_output, True)

    if package.verification_code:
        package_verification_code = write_package_verification_code(package.verification_code)
        write_value("PackageVerificationCode", package_verification_code, text_output, True)

    write_text_value("PackageDescription", package.description, text_output, True)
    write_text_value("PackageComment", package.comment, text_output, True)

    write_field_or_none_or_no_assertion("PackageLicenseDeclared", package.license_declared, text_output, True)
    write_field_or_none_or_no_assertion("PackageLicenseConcluded", package.license_concluded, text_output, True)
    write_field_or_none_or_no_assertion("PackageLicenseInfoFromFiles", package.license_info_from_files, text_output,
                                        True)

    write_text_value("PackageLicenseComments", package.license_comment, text_output, True)
    write_field_or_none_or_no_assertion("PackageCopyrightText", package.copyright_text, text_output, True)

    write_value("PackageHomePage", package.homepage, text_output, True)

    for external_reference in package.external_references:
        external_reference_str = " ".join(
            [transform_enum_name_to_tv(external_reference.category.name), external_reference.reference_type,
             external_reference.locator]
        )
        write_value("ExternalRef", external_reference_str, text_output, True)
        if external_reference.comment:
            write_text_value("ExternalRefComment", external_reference.comment, text_output)

    if package.primary_package_purpose:
        write_value("PrimaryPackagePurpose", transform_enum_name_to_tv(package.primary_package_purpose.name),
                    text_output)

    if package.built_date:
        write_value("BuiltDate", datetime_to_iso_string(package.built_date), text_output)
    if package.release_date:
        write_value("ReleaseDate", datetime_to_iso_string(package.release_date), text_output)
    if package.valid_until_date:
        write_value("ValidUntilDate", datetime_to_iso_string(package.valid_until_date), text_output)


def write_package_verification_code(verification_code: PackageVerificationCode):
    if not verification_code.excluded_files:
        return verification_code.value

    excluded_files_str = " (excludes: " + " ".join(verification_code.excluded_files) + ")"
    return verification_code.value + excluded_files_str
