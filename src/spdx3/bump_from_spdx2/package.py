# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import Union

from spdx3.bump_from_spdx2.actor import bump_actor
from spdx3.bump_from_spdx2.bump_utils import handle_no_assertion_or_none
from spdx3.bump_from_spdx2.checksum import bump_checksum
from spdx3.bump_from_spdx2.message import print_missing_conversion
from spdx3.model.creation_information import CreationInformation
from spdx3.model.external_identifier import ExternalIdentifier, ExternalIdentifierType
from spdx3.model.external_reference import ExternalReference, ExternalReferenceType
from spdx3.model.software.package import Package
from spdx3.model.software.software_purpose import SoftwarePurpose
from spdx3.payload import Payload
from spdx.model.package import ExternalPackageRef
from spdx.model.package import Package as Spdx2_Package


def bump_package(
    spdx2_package: Spdx2_Package, payload: Payload, creation_information: CreationInformation, document_namespace: str
):
    spdx_id = "#".join([document_namespace, spdx2_package.spdx_id])
    name = spdx2_package.name
    download_location = handle_no_assertion_or_none(spdx2_package.download_location, "package.download_location")
    package_version = spdx2_package.version
    # package.file_name -> ?
    print_missing_conversion("package2.file_name", 0)
    # package.supplier -> Relationship, suppliedBy?
    print_missing_conversion("package2.supplier", 1, "of relationships")
    originated_by_spdx_id = bump_actor(spdx2_package.originator, payload, creation_information, document_namespace)
    # package.files_analyzed  -> ?
    print_missing_conversion("package2.files_analyzed", 0)
    # package.verification_code -> package.verified_using
    print_missing_conversion("package2.verification_code", 1, "of IntegrityMethod")
    # package.checksums -> package.verified_using
    integrity_methods = [bump_checksum(checksum) for checksum in spdx2_package.checksums]
    homepage = spdx2_package.homepage
    print_missing_conversion("package2.source_info", 0)
    print_missing_conversion(
        "package2.license_concluded, package2.license_info_from_files, package2.license_declared, "
        "package2.license_comment, package2.copyright_text",
        0,
        "and missing definition of license profile",
    )
    summary = spdx2_package.summary
    description = spdx2_package.description
    comment = spdx2_package.comment

    external_references = []
    external_identifiers = []
    purl_refs = [
        external_ref for external_ref in spdx2_package.external_references if external_ref.reference_type == "purl"
    ]
    exactly_one_purl = len(purl_refs) == 1
    package_url = None
    if exactly_one_purl:
        package_url = purl_refs[0].locator
    for spdx2_external_ref in spdx2_package.external_references:
        if exactly_one_purl and spdx2_external_ref.reference_type == "purl":
            continue
        id_or_ref = bump_external_package_ref(spdx2_external_ref)
        if isinstance(id_or_ref, ExternalReference):
            external_references.append(id_or_ref)
        elif isinstance(id_or_ref, ExternalIdentifier):
            external_identifiers.append(id_or_ref)

    print_missing_conversion("package2.attribution_texts", 0)
    package_purpose = (
        [SoftwarePurpose[spdx2_package.primary_package_purpose.name]] if spdx2_package.primary_package_purpose else []
    )
    print_missing_conversion("package2.release_date, package2.built_date, package2.valid_until_date", 0)

    payload.add_element(
        Package(
            spdx_id,
            creation_information,
            name,
            summary=summary,
            description=description,
            comment=comment,
            verified_using=integrity_methods,
            external_references=external_references,
            external_identifier=external_identifiers,
            originated_by=originated_by_spdx_id,
            package_purpose=package_purpose,
            package_version=package_version,
            download_location=download_location,
            package_url=package_url,
            homepage=homepage,
        )
    )


external_ref_type_map = {
    "cpe22Type": ExternalIdentifierType.CPE22,
    "cpe23Type": ExternalIdentifierType.CPE23,
    "advisory": ExternalReferenceType.SECURITY_ADVISORY,
    "fix": ExternalReferenceType.SECURITY_FIX,
    "url": None,
    "swid": ExternalIdentifierType.SWID,
    "maven-central": None,
    "npm": None,
    "nuget": None,
    "bower": None,
    "purl": ExternalIdentifierType.PURL,
    "swh": ExternalIdentifierType.SWHID,
    "gitoid": ExternalIdentifierType.GITOID,
}


def bump_external_package_ref(spdx2_external_ref: ExternalPackageRef) -> Union[ExternalReference, ExternalIdentifier]:
    reference_type = spdx2_external_ref.reference_type
    locator = spdx2_external_ref.locator
    comment = spdx2_external_ref.comment

    if reference_type not in external_ref_type_map:
        raise NotImplementedError(
            f"Conversion of ExternalPackageRef of type {reference_type} is currently not supported."
        )

    id_or_ref_type = external_ref_type_map[reference_type]

    if isinstance(id_or_ref_type, ExternalReferenceType):
        return ExternalReference(id_or_ref_type, [locator], None, comment)
    elif isinstance(id_or_ref_type, ExternalIdentifierType):
        return ExternalIdentifier(id_or_ref_type, locator, comment)
