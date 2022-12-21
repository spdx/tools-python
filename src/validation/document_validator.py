from typing import List

from src.model.document import Document
from src.model.relationship import RelationshipType
from src.validation.annotation_validator import validate_annotations
from src.validation.creation_info_validator import validate_creation_info
from src.validation.extracted_licensing_info_validator import validate_extracted_licensing_infos
from src.validation.file_validator import validate_files
from src.validation.package_validator import validate_packages
from src.validation.relationship_validator import validate_relationships
from src.validation.snippet_validator import validate_snippets
from src.validation.validation_message import ValidationMessage, ValidationContext, SpdxElementType


def validate_full_spdx_document(document: Document, spdx_version: str) -> List[ValidationMessage]:
    validation_messages: List[ValidationMessage] = []

    validation_messages.extend(validate_creation_info(document.creation_info))
    validation_messages.extend(validate_packages(document.packages, document))
    validation_messages.extend(validate_files(document.files, document))
    validation_messages.extend(validate_snippets(document.snippets, document))
    validation_messages.extend(validate_annotations(document.annotations, document))
    validation_messages.extend(validate_relationships(document.relationships, document, spdx_version))
    validation_messages.extend(validate_extracted_licensing_infos(document.extracted_licensing_info))

    document_id = document.creation_info.spdx_id
    document_describes_relationships = [relationship for relationship in document.relationships if
                                        relationship.relationship_type == RelationshipType.DESCRIBES and relationship.spdx_element_id == document_id]
    described_by_document_relationships = [relationship for relationship in document.relationships if
                                           relationship.relationship_type == RelationshipType.DESCRIBED_BY and relationship.related_spdx_element_id == document_id]

    if not document_describes_relationships + described_by_document_relationships:
        validation_messages.append(
            ValidationMessage(
                f'there must be at least one relationship "{document_id} DESCRIBES ..." or "... DESCRIBED_BY {document_id}"',
                ValidationContext(spdx_id=document_id,
                                  element_type=SpdxElementType.DOCUMENT)))

    return validation_messages
