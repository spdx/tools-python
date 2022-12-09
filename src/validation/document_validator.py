from typing import List

from src.model.document import Document
from src.model.relationship import RelationshipType
from src.validation.annotation_validator import AnnotationValidator
from src.validation.creation_info_validator import CreationInfoValidator
from src.validation.external_document_ref_validator import ExternalDocumentRefValidator
from src.validation.extracted_licensing_info_validator import ExtractedLicensingInfoValidator
from src.validation.file_validator import FileValidator
from src.validation.package_validator import PackageValidator
from src.validation.relationship_validator import RelationshipValidator
from src.validation.snippet_validator import SnippetValidator
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


class DocumentValidator:
    spdx_version: str
    creation_info_validator: CreationInfoValidator
    package_validator: PackageValidator
    file_validator: FileValidator
    snippet_validator: SnippetValidator
    annotation_validator: AnnotationValidator
    relationship_validator: RelationshipValidator
    external_document_ref_validator: ExternalDocumentRefValidator
    extracted_licensing_info_validator: ExtractedLicensingInfoValidator

    def __init__(self, spdx_version: str):
        self.spdx_version = spdx_version
        self.creation_info_validator = CreationInfoValidator(spdx_version)
        self.package_validator = PackageValidator(spdx_version)
        self.file_validator = FileValidator(spdx_version)
        self.snippet_validator = SnippetValidator(spdx_version)
        self.annotation_validator = AnnotationValidator(spdx_version)
        self.relationship_validator = RelationshipValidator(spdx_version)
        self.external_document_ref_validator = ExternalDocumentRefValidator(spdx_version)
        self.extracted_licensing_info_validator = ExtractedLicensingInfoValidator(spdx_version)

    def validate_full_spdx_document(self, document: Document) -> List[ValidationMessage]:
        error_messages: List[ValidationMessage] = []

        error_messages.extend(self.creation_info_validator.validate_creation_info(document.creation_info))
        error_messages.extend(self.package_validator.validate_packages(document.packages))
        error_messages.extend(self.file_validator.validate_files(document.files))
        error_messages.extend(self.snippet_validator.validate_snippets(document.snippets))
        error_messages.extend(self.annotation_validator.validate_annotations(document.annotations))
        error_messages.extend(self.relationship_validator.validate_relationships(document.relationships))
        error_messages.extend(
            self.external_document_ref_validator.validate_external_document_ref(document.external_document_refs))
        error_messages.extend(self.extracted_licensing_info_validator.validate_extracted_licensing_infos(
            document.extracted_licensing_info))

        # TODO: is this correct here?
        all_document_relationship_types = [relationship.relationship_type for relationship in document.relationships if
                                           relationship.spdx_element_id == document.creation_info.spdx_id]

        if RelationshipType.DESCRIBES not in all_document_relationship_types:
            error_messages.append(
                ValidationMessage(
                    f'there must be at least one relationship "{document.creation_info.spdx_id} DESCRIBES ..."',
                    ValidationContext(spdx_id=document.creation_info.spdx_id,
                                      element_type=SpdxElementType.DOCUMENT)))

        return error_messages
