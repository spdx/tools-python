# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime

from spdx_tools.common.spdx_licensing import spdx_licensing
from spdx_tools.spdx.constants import DOCUMENT_SPDX_ID
from spdx_tools.spdx.model import (
    Actor,
    ActorType,
    Annotation,
    AnnotationType,
    Checksum,
    ChecksumAlgorithm,
    CreationInfo,
    Document,
    ExternalDocumentRef,
    ExternalPackageRef,
    ExternalPackageRefCategory,
    ExtractedLicensingInfo,
    File,
    FileType,
    Package,
    PackagePurpose,
    PackageVerificationCode,
    Relationship,
    RelationshipType,
    Snippet,
    SpdxNoAssertion,
    SpdxNone,
    Version,
)

# Utility methods to create data model instances. All properties have valid defaults, so they don't need to be
# specified unless relevant for the test.


def actor_fixture(actor_type=ActorType.PERSON, name="actorName", email="some@mail.com") -> Actor:
    return Actor(actor_type, name, email)


def checksum_fixture(algorithm=ChecksumAlgorithm.SHA1, value="71c4025dd9897b364f3ebbb42c484ff43d00791c") -> Checksum:
    return Checksum(algorithm, value)


def package_verification_code_fixture(
    value="85ed0817af83a24ad8da68c2b5094de69833983c", excluded_files=None
) -> PackageVerificationCode:
    excluded_files = ["./exclude.py"] if excluded_files is None else excluded_files
    return PackageVerificationCode(value, excluded_files)


def creation_info_fixture(
    spdx_version="SPDX-2.3",
    spdx_id=DOCUMENT_SPDX_ID,
    name="documentName",
    document_namespace="https://some.namespace",
    creators=None,
    created=datetime(2022, 12, 1),
    creator_comment="creatorComment",
    data_license="CC0-1.0",
    external_document_refs=None,
    license_list_version=Version(3, 19),
    document_comment="documentComment",
) -> CreationInfo:
    creators = [actor_fixture(name="creatorName")] if creators is None else creators
    external_document_refs = (
        [external_document_ref_fixture()] if external_document_refs is None else external_document_refs
    )
    return CreationInfo(
        spdx_version,
        spdx_id,
        name,
        document_namespace,
        creators,
        created,
        creator_comment,
        data_license,
        external_document_refs,
        license_list_version,
        document_comment,
    )


def file_fixture(
    name="./fileName.py",
    spdx_id="SPDXRef-File",
    checksums=None,
    file_types=None,
    license_concluded=spdx_licensing.parse("MIT and GPL-2.0"),
    license_info_in_file=None,
    license_comment="licenseComment",
    copyright_text="copyrightText",
    comment="fileComment",
    notice="fileNotice",
    contributors=None,
    attribution_texts=None,
) -> File:
    checksums = [checksum_fixture()] if checksums is None else checksums
    file_types = [FileType.TEXT] if file_types is None else file_types
    license_info_in_file = (
        [spdx_licensing.parse("MIT"), spdx_licensing.parse("GPL-2.0"), SpdxNoAssertion()]
        if license_info_in_file is None
        else license_info_in_file
    )
    contributors = ["fileContributor"] if contributors is None else contributors
    attribution_texts = ["fileAttributionText"] if attribution_texts is None else attribution_texts
    return File(
        name=name,
        spdx_id=spdx_id,
        checksums=checksums,
        file_types=file_types,
        license_concluded=license_concluded,
        license_info_in_file=license_info_in_file,
        license_comment=license_comment,
        copyright_text=copyright_text,
        comment=comment,
        notice=notice,
        contributors=contributors,
        attribution_texts=attribution_texts,
    )


def package_fixture(
    spdx_id="SPDXRef-Package",
    name="packageName",
    download_location="https://download.com",
    version="12.2",
    file_name="./packageFileName",
    supplier=actor_fixture(name="supplierName"),
    originator=actor_fixture(name="originatorName"),
    files_analyzed=True,
    verification_code=package_verification_code_fixture(),
    checksums=None,
    homepage="https://homepage.com",
    source_info="sourceInfo",
    license_concluded=spdx_licensing.parse("MIT and GPL-2.0"),
    license_info_from_files=None,
    license_declared=spdx_licensing.parse("MIT and GPL-2.0"),
    license_comment="packageLicenseComment",
    copyright_text="packageCopyrightText",
    summary="packageSummary",
    description="packageDescription",
    comment="packageComment",
    external_references=None,
    attribution_texts=None,
    primary_package_purpose=PackagePurpose.SOURCE,
    release_date=datetime(2022, 11, 1),
    built_date=datetime(2022, 11, 2),
    valid_until_date=datetime(2022, 11, 3),
) -> Package:
    checksums = [checksum_fixture()] if checksums is None else checksums
    license_info_from_files = (
        [spdx_licensing.parse("MIT"), spdx_licensing.parse("GPL-2.0"), SpdxNoAssertion()]
        if license_info_from_files is None
        else license_info_from_files
    )
    external_references = [external_package_ref_fixture()] if external_references is None else external_references
    attribution_texts = ["packageAttributionText"] if attribution_texts is None else attribution_texts
    return Package(
        spdx_id=spdx_id,
        name=name,
        download_location=download_location,
        version=version,
        file_name=file_name,
        supplier=supplier,
        originator=originator,
        files_analyzed=files_analyzed,
        verification_code=verification_code,
        checksums=checksums,
        homepage=homepage,
        source_info=source_info,
        license_concluded=license_concluded,
        license_info_from_files=license_info_from_files,
        license_declared=license_declared,
        license_comment=license_comment,
        copyright_text=copyright_text,
        summary=summary,
        description=description,
        comment=comment,
        external_references=external_references,
        attribution_texts=attribution_texts,
        primary_package_purpose=primary_package_purpose,
        release_date=release_date,
        built_date=built_date,
        valid_until_date=valid_until_date,
    )


def external_document_ref_fixture(
    document_ref_id="DocumentRef-external", document_uri="https://namespace.com", checksum=checksum_fixture()
) -> ExternalDocumentRef:
    return ExternalDocumentRef(document_ref_id=document_ref_id, document_uri=document_uri, checksum=checksum)


def external_package_ref_fixture(
    category=ExternalPackageRefCategory.PACKAGE_MANAGER,
    reference_type="maven-central",
    locator="org.apache.tomcat:tomcat:9.0.0.M4",
    comment="externalPackageRefComment",
) -> ExternalPackageRef:
    return ExternalPackageRef(category=category, reference_type=reference_type, locator=locator, comment=comment)


def snippet_fixture(
    spdx_id="SPDXRef-Snippet",
    file_spdx_id="SPDXRef-File",
    byte_range=(1, 2),
    line_range=(3, 4),
    license_concluded=spdx_licensing.parse("MIT and GPL-2.0"),
    license_info_in_snippet=None,
    license_comment="snippetLicenseComment",
    copyright_text="licenseCopyrightText",
    comment="snippetComment",
    name="snippetName",
    attribution_texts=None,
) -> Snippet:
    license_info_in_snippet = (
        [spdx_licensing.parse("MIT"), spdx_licensing.parse("GPL-2.0"), SpdxNone()]
        if license_info_in_snippet is None
        else license_info_in_snippet
    )
    attribution_texts = ["snippetAttributionText"] if attribution_texts is None else attribution_texts
    return Snippet(
        spdx_id=spdx_id,
        file_spdx_id=file_spdx_id,
        byte_range=byte_range,
        line_range=line_range,
        license_concluded=license_concluded,
        license_info_in_snippet=license_info_in_snippet,
        license_comment=license_comment,
        copyright_text=copyright_text,
        comment=comment,
        name=name,
        attribution_texts=attribution_texts,
    )


def annotation_fixture(
    spdx_id="SPDXRef-File",
    annotation_type=AnnotationType.REVIEW,
    annotator=actor_fixture(name="annotatorName"),
    annotation_date=datetime(2022, 12, 24),
    annotation_comment="annotationComment",
) -> Annotation:
    return Annotation(
        spdx_id=spdx_id,
        annotation_type=annotation_type,
        annotator=annotator,
        annotation_date=annotation_date,
        annotation_comment=annotation_comment,
    )


def extracted_licensing_info_fixture(
    license_id="LicenseRef-1",
    extracted_text="extractedText",
    license_name="licenseName",
    cross_references=None,
    comment="licenseComment",
) -> ExtractedLicensingInfo:
    cross_references = ["https://see.also"] if cross_references is None else cross_references
    return ExtractedLicensingInfo(
        license_id=license_id,
        extracted_text=extracted_text,
        license_name=license_name,
        cross_references=cross_references,
        comment=comment,
    )


def relationship_fixture(
    spdx_element_id=DOCUMENT_SPDX_ID,
    relationship_type=RelationshipType.DESCRIBES,
    related_spdx_element_id="SPDXRef-File",
    comment="relationshipComment",
) -> Relationship:
    return Relationship(
        spdx_element_id=spdx_element_id,
        relationship_type=relationship_type,
        related_spdx_element_id=related_spdx_element_id,
        comment=comment,
    )


def document_fixture(
    creation_info=None,
    packages=None,
    files=None,
    snippets=None,
    annotations=None,
    relationships=None,
    extracted_licensing_info=None,
) -> Document:
    creation_info = creation_info_fixture() if creation_info is None else creation_info
    packages = [package_fixture()] if packages is None else packages
    files = [file_fixture()] if files is None else files
    snippets = [snippet_fixture()] if snippets is None else snippets
    annotations = [annotation_fixture()] if annotations is None else annotations
    relationships = [relationship_fixture()] if relationships is None else relationships
    extracted_licensing_info = (
        [extracted_licensing_info_fixture()] if extracted_licensing_info is None else extracted_licensing_info
    )
    return Document(
        creation_info=creation_info,
        packages=packages,
        files=files,
        snippets=snippets,
        annotations=annotations,
        relationships=relationships,
        extracted_licensing_info=extracted_licensing_info,
    )
