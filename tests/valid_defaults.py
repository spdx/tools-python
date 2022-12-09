from datetime import datetime

from src.model.actor import Actor, ActorType
from src.model.annotation import AnnotationType, Annotation
from src.model.checksum import Checksum, ChecksumAlgorithm
from src.model.document import CreationInfo, Document
from src.model.external_document_ref import ExternalDocumentRef
from src.model.extracted_licensing_info import ExtractedLicensingInfo
from src.model.file import File
from src.model.package import Package, PackageVerificationCode, ExternalPackageRef, ExternalPackageRefCategory
from src.model.relationship import Relationship, RelationshipType
from src.model.snippet import Snippet
from src.model.spdx_none import SpdxNone


def get_actor(actor_type=ActorType.PERSON, name="person name", mail=None) -> Actor:
    return Actor(actor_type, name, mail)


def get_annotation(spdx_id="SPDXRef-DOCUMENT", annotation_type=AnnotationType.OTHER, annotator=get_actor(),
                   annotation_date=datetime(2022, 1, 1), annotation_comment="annotation comment") -> Annotation:
    return Annotation(spdx_id, annotation_type, annotator, annotation_date, annotation_comment)


def get_checksum(algorithm=ChecksumAlgorithm.SHA1, value="85ed0817af83a24ad8da68c2b5094de69833983c") -> Checksum:
    return Checksum(algorithm, value)


def get_creation_info(spdx_version="SPDX-2.3", spdx_id="SPDXRef-DOCUMENT", name="document_name",
                      document_namespace="https://some.uri",
                      creators=None, created=datetime(2022, 1, 1), creator_comment=None, data_license="CC0-1.0",
                      external_document_refs=None, license_list_version=None, document_comment=None) -> CreationInfo:
    if creators is None:
        creators = [get_actor()]

    if external_document_refs is None:
        external_document_refs = []

    return CreationInfo(spdx_version, spdx_id, name, document_namespace, creators, created, creator_comment,
                        data_license, external_document_refs, license_list_version, document_comment)


def get_document(creation_info=get_creation_info(), packages=None, files=None, snippets=None, annotations=None,
                 relationships=None, extracted_licensing_info=None) -> Document:
    if packages is None:
        packages = []
    if files is None:
        files = []
    if snippets is None:
        snippets = []
    if annotations is None:
        annotations = []
    if relationships is None:
        relationships = []
    if extracted_licensing_info is None:
        extracted_licensing_info = []

    return Document(creation_info, packages, files, snippets, annotations, relationships, extracted_licensing_info)


def get_external_document_ref(document_ref_id="DocumentRef-idstring", document_uri="https://some.uri",
                              checksum=get_checksum()) -> ExternalDocumentRef:
    return ExternalDocumentRef(document_ref_id, document_uri, checksum)


def get_extracted_licensing_info(license_id="LicenseRef-1", extracted_text="extracted text",
                                 license_name="license name", comment=None,
                                 cross_references=None) -> ExtractedLicensingInfo:
    if cross_references is None:
        cross_references = ["http://some.url"]
    return ExtractedLicensingInfo(license_id, extracted_text, license_name, comment, cross_references)


def get_file(name="./file/name.py", spdx_id="SPDXRef-File", checksums=None, file_type=None, concluded_license=None,
             license_info_in_file=None, license_comment=None, copyright_text=None, comment=None, notice=None,
             contributors=None, attribution_texts=None):
    if checksums is None:
        checksums = [get_checksum()]
    if contributors is None:
        contributors = []
    if attribution_texts is None:
        attribution_texts = []

    return File(name, spdx_id, checksums, file_type, concluded_license, license_info_in_file, license_comment,
                copyright_text, comment, notice, contributors, attribution_texts)


def get_package_verification_code(value="85ed0817af83a24ad8da68c2b5094de69833983c",
                                  excluded_files=None) -> PackageVerificationCode:
    if excluded_files is None:
        excluded_files = []

    return PackageVerificationCode(value, excluded_files)


def get_external_package_ref(category=ExternalPackageRefCategory.SECURITY, reference_type="cpe22Type",
                             locator="cpe:/o:canonical:ubuntu_linux:10.04:-:lts",
                             comment="external package ref comment") -> ExternalPackageRef:
    return ExternalPackageRef(category, reference_type, locator, comment)


def get_package(spdx_id="SPDXRef-Package", name="package name", download_location=SpdxNone(), version=None,
                file_name=None, supplier=None, originator=None, files_analyzed=False, verification_code=None,
                checksums=None, homepage=None, source_info=None, license_concluded=None, license_info_from_files=None,
                license_declared=None, license_comment=None, copyright_text=None, summary=None, description=None,
                comment=None, external_references=None, attribution_texts=None, primary_package_purpose=None,
                release_date=None, built_date=None, valid_until_date=None) -> Package:
    if checksums is None:
        checksums = []
    if external_references is None:
        external_references = []
    if attribution_texts is None:
        attribution_texts = []

    return Package(spdx_id, name, download_location, version, file_name, supplier, originator, files_analyzed,
                   verification_code, checksums, homepage, source_info, license_concluded, license_info_from_files,
                   license_declared, license_comment, copyright_text, summary, description, comment,
                   external_references, attribution_texts, primary_package_purpose, release_date, built_date,
                   valid_until_date)


def get_relationship(spdx_element_id="SPDXRef-DOCUMENT", relationship_type=RelationshipType.DESCRIBES,
                     related_spdx_element_id="SPDXRef-File", comment=None) -> Relationship:
    return Relationship(spdx_element_id, relationship_type, related_spdx_element_id, comment)


def get_snippet(spdx_id="SPDXRef-Snippet", file_spdx_id="SPDXRef-File", byte_range=(200, 400), line_range=None,
                concluded_license=None, license_info_in_snippet=None, license_comment=None, copyright_text=None,
                comment=None, name=None, attribution_texts=None) -> Snippet:
    if attribution_texts is None:
        attribution_texts = []

    return Snippet(spdx_id, file_spdx_id, byte_range, line_range, concluded_license, license_info_in_snippet,
                   license_comment, copyright_text, comment, name, attribution_texts)
