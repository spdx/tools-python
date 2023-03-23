# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from spdx.model.package import Package as Spdx2_Package
from spdx3.bump_from_spdx2.actor import bump_actor
from spdx3.bump_from_spdx2.bump_utils import handle_no_assertion_or_none
from spdx3.bump_from_spdx2.checksum import bump_checksum
from spdx3.bump_from_spdx2.message import print_missing_conversion
from spdx3.model.creation_information import CreationInformation
from spdx3.model.software.package import Package
from spdx3.model.software.software_purpose import SoftwarePurpose
from spdx3.payload import Payload


def bump_package(spdx2_package: Spdx2_Package, payload: Payload, creation_information: CreationInformation):
    spdx_id = spdx2_package.spdx_id
    name = spdx2_package.name
    download_location = handle_no_assertion_or_none(spdx2_package.download_location, "package.download_location")
    # package2.version -> ?
    print_missing_conversion("package2.version", 0)
    # package.file_name -> ?
    print_missing_conversion("package2.file_name", 0)
    # package.supplier -> Relationship, suppliedBy?
    print_missing_conversion("package2.supplier", 1, "of relationships")
    originated_by_spdx_id = bump_actor(spdx2_package.originator, payload, creation_information)
    # package.files_analyzed  -> ?
    print_missing_conversion("package2.files_analyzed", 0)
    # package.verification_code -> package.verified_using
    print_missing_conversion("package2.verification_code", 1, "of IntegrityMethod")
    # package.checksums -> package.verified_using
    integrity_methods = [bump_checksum(checksum) for checksum in spdx2_package.checksums]
    homepage = spdx2_package.homepage
    print_missing_conversion("package2.source_info", 0)
    print_missing_conversion("package2.license_concluded, package2.license_info_from_files, package2.license_declared, "
                             "package2.license_comment, package2.copyright_text", 0,
                             "and missing definition of license profile")
    summary = spdx2_package.summary
    description = spdx2_package.description
    comment = spdx2_package.comment
    print_missing_conversion("package2.external_references", 1, "of ExternalReferences / ExternalIdentifiers")
    print_missing_conversion("package2.attribution_texts", 0)
    package_purpose = [SoftwarePurpose[
                           spdx2_package.primary_package_purpose.name]] if spdx2_package.primary_package_purpose else []
    print_missing_conversion("package2.release_date, package2.built_date, package2.valid_until_date", 0)

    payload.add_element(Package(spdx_id, creation_information, name, verified_using=integrity_methods,
                                download_location=download_location, homepage=homepage, summary=summary,
                                description=description, comment=comment, originated_by=originated_by_spdx_id,
                                package_purpose=package_purpose))
