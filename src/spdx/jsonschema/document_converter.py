# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Type, Any

from spdx.document_utils import get_contained_spdx_element_ids
from spdx.jsonschema.annotation_converter import AnnotationConverter
from spdx.jsonschema.converter import TypedConverter
from spdx.jsonschema.creation_info_converter import CreationInfoConverter
from spdx.jsonschema.document_properties import DocumentProperty
from spdx.jsonschema.external_document_ref_converter import ExternalDocumentRefConverter
from spdx.jsonschema.extracted_licensing_info_converter import ExtractedLicensingInfoConverter
from spdx.jsonschema.file_converter import FileConverter
from spdx.jsonschema.json_property import JsonProperty
from spdx.jsonschema.package_converter import PackageConverter
from spdx.jsonschema.relationship_converter import RelationshipConverter
from spdx.jsonschema.snippet_converter import SnippetConverter
from spdx.model.document import Document
from spdx.model.relationship import RelationshipType
from spdx.model.relationship_filters import filter_by_type_and_origin, filter_by_type_and_target, \
    find_package_contains_file_relationships, \
    find_file_contained_by_package_relationships


class DocumentConverter(TypedConverter[Document]):
    creation_info_converter: CreationInfoConverter
    external_document_ref_converter: ExternalDocumentRefConverter
    package_converter: PackageConverter
    file_converter: FileConverter
    snippet_converter: SnippetConverter
    annotation_converter: AnnotationConverter
    relationship_converter: RelationshipConverter
    extracted_licensing_info_converter: ExtractedLicensingInfoConverter

    def __init__(self):
        self.external_document_ref_converter = ExternalDocumentRefConverter()
        self.creation_info_converter = CreationInfoConverter()
        self.package_converter = PackageConverter()
        self.file_converter = FileConverter()
        self.snippet_converter = SnippetConverter()
        self.annotation_converter = AnnotationConverter()
        self.relationship_converter = RelationshipConverter()
        self.extracted_licensing_info_converter = ExtractedLicensingInfoConverter()

    def get_json_type(self) -> Type[JsonProperty]:
        return DocumentProperty

    def get_data_model_type(self) -> Type[Document]:
        return Document

    def json_property_name(self, document_property: DocumentProperty) -> str:
        if document_property == DocumentProperty.SPDX_ID:
            return "SPDXID"
        return super().json_property_name(document_property)

    def _get_property_value(self, document: Document, document_property: DocumentProperty,
                            _document: Document = None) -> Any:
        if document_property == DocumentProperty.SPDX_ID:
            return document.creation_info.spdx_id
        elif document_property == DocumentProperty.ANNOTATIONS:
            # annotations referencing files, packages or snippets will be added to those elements directly
            element_ids = get_contained_spdx_element_ids(document)
            document_annotations = filter(lambda annotation: annotation.spdx_id not in element_ids,
                                          document.annotations)
            return [self.annotation_converter.convert(annotation) for annotation in document_annotations] or None
        elif document_property == DocumentProperty.COMMENT:
            return document.creation_info.document_comment
        elif document_property == DocumentProperty.CREATION_INFO:
            return self.creation_info_converter.convert(document.creation_info)
        elif document_property == DocumentProperty.DATA_LICENSE:
            return document.creation_info.data_license
        elif document_property == DocumentProperty.EXTERNAL_DOCUMENT_REFS:
            return [self.external_document_ref_converter.convert(external_document_ref) for
                    external_document_ref in document.creation_info.external_document_refs] or None
        elif document_property == DocumentProperty.HAS_EXTRACTED_LICENSING_INFOS:
            return [self.extracted_licensing_info_converter.convert(licensing_info) for licensing_info in
                    document.extracted_licensing_info] or None
        elif document_property == DocumentProperty.NAME:
            return document.creation_info.name
        elif document_property == DocumentProperty.SPDX_VERSION:
            return document.creation_info.spdx_version
        elif document_property == DocumentProperty.DOCUMENT_NAMESPACE:
            return document.creation_info.document_namespace
        elif document_property == DocumentProperty.DOCUMENT_DESCRIBES:
            describes_ids = [relationship.related_spdx_element_id for relationship in
                             filter_by_type_and_origin(document.relationships, RelationshipType.DESCRIBES,
                                                       document.creation_info.spdx_id)]
            described_by_ids = [relationship.spdx_element_id for relationship in
                                filter_by_type_and_target(document.relationships, RelationshipType.DESCRIBED_BY,
                                                          document.creation_info.spdx_id)]
            return describes_ids + described_by_ids or None
        elif document_property == DocumentProperty.PACKAGES:
            return [self.package_converter.convert(package, document) for package in document.packages] or None
        elif document_property == DocumentProperty.FILES:
            return [self.file_converter.convert(file, document) for file in document.files] or None
        elif document_property == DocumentProperty.SNIPPETS:
            return [self.snippet_converter.convert(snippet, document) for snippet in document.snippets] or None
        elif document_property == DocumentProperty.RELATIONSHIPS:
            already_covered_relationships = filter_by_type_and_origin(document.relationships,
                                                                      RelationshipType.DESCRIBES,
                                                                      document.creation_info.spdx_id)
            already_covered_relationships.extend(
                filter_by_type_and_target(document.relationships, RelationshipType.DESCRIBED_BY,
                                          document.creation_info.spdx_id))
            for package in document.packages:
                already_covered_relationships.extend(find_package_contains_file_relationships(document, package))
                already_covered_relationships.extend(find_file_contained_by_package_relationships(document, package))
            relationships_to_ignore = [relationship for relationship in already_covered_relationships if
                                       relationship.comment is None]
            return [self.relationship_converter.convert(relationship) for relationship in document.relationships if
                    relationship not in relationships_to_ignore] or None
