from datetime import datetime

from src.model.actor import Actor, ActorType
from src.model.annotation import AnnotationType, Annotation
from src.model.checksum import Checksum, ChecksumAlgorithm
from src.model.document import CreationInfo, Document
from src.model.external_document_ref import ExternalDocumentRef


def get_actor(actor_type=ActorType.PERSON, name="person name", mail="mail@mail.com") -> Actor:
    return Actor(actor_type, name, mail)


def get_annotation(spdx_id="", annotation_type=AnnotationType.OTHER, annotator="person name", annotation_date=datetime(2022, 1, 1), annotation_comment=""):
    return Annotation(spdx_id, annotation_type, annotator, annotation_date, annotation_comment)


def get_creation_info(spdx_version="SPDX-2.3", spdx_id="SPDXRef-DOCUMENT", name="document_name", document_namespace="https://some.uri",
                      creators=None, created=datetime(2022, 1, 1), creator_comment=None, data_license="CC0-1.0",
                      external_document_refs=None, license_list_version=None, document_comment=None):
    if creators is None:
        creators = [get_actor()]

    if external_document_refs is None:
        external_document_refs = []

    return CreationInfo(spdx_version, spdx_id, name, document_namespace, creators, created, creator_comment, data_license, external_document_refs, license_list_version, document_comment)


def get_document(creation_info=get_creation_info(), packages=None, files=None, snippets=None, annotations=None, relationships=None, extracted_licensing_info=None):
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


def get_external_document_ref() -> ExternalDocumentRef:
    return ExternalDocumentRef("https://some.uri", "SPDXRef-1", get_checksum())


def get_checksum(algorithm=ChecksumAlgorithm.SHA1, value="85ed0817af83a24ad8da68c2b5094de69833983c") -> Checksum:
    return Checksum(algorithm, value)

