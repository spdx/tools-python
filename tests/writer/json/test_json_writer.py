#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import json
import os
from datetime import datetime

import pytest

from src.model.actor import Actor, ActorType
from src.model.annotation import Annotation, AnnotationType
from src.model.checksum import ChecksumAlgorithm, Checksum
from src.model.document import CreationInfo, Document
from src.model.external_document_ref import ExternalDocumentRef
from src.model.extracted_licensing_info import ExtractedLicensingInfo
from src.model.file import File
from src.model.package import Package
from src.model.relationship import RelationshipType, Relationship
from src.model.snippet import Snippet
from src.model.spdx_none import SpdxNone
from src.writer.json.json_writer import JsonWriter


@pytest.fixture
def temporary_file_path() -> str:
    temporary_file_path = "temp_test_json_writer_output.json"
    yield temporary_file_path
    os.remove(temporary_file_path)


def test_write_json(temporary_file_path: str):
    writer = JsonWriter()
    creation_info = CreationInfo("spdxVersion", "documentId", "documentName", "documentNamespace",
                                 [Actor(ActorType.TOOL, "tools-python", "tools-python@github.com")],
                                 datetime(2022, 12, 1), document_comment="comment", data_license="dataLicense",
                                 external_document_refs=[ExternalDocumentRef("docRefId", "externalDocumentUri",
                                                                             Checksum(ChecksumAlgorithm.SHA1,
                                                                                      "externalRefSha1"))])
    package = Package("packageId", "packageName", SpdxNone())
    file = File("fileName", "fileId", [Checksum(ChecksumAlgorithm.SHA1, "fileSha1")])
    snippet = Snippet("snippetId", "snippetFileId", (1, 2))
    relationships = [
        Relationship(creation_info.spdx_id, RelationshipType.DESCRIBES, "packageId"),
        Relationship(creation_info.spdx_id, RelationshipType.DESCRIBES, "fileId", "relationshipComment"),
        Relationship("relationshipOriginId", RelationshipType.AMENDS, "relationShipTargetId")]
    annotations = [
        Annotation("documentId", AnnotationType.REVIEW, Actor(ActorType.PERSON, "reviewerName"),
                   datetime(2022, 12, 2), "reviewComment"),
        Annotation("fileId", AnnotationType.OTHER, Actor(ActorType.TOOL, "toolName"), datetime(2022, 12, 3),
                   "otherComment")]
    extracted_licensing_info = [ExtractedLicensingInfo("licenseId", "licenseText")]
    document = Document(creation_info, annotations=annotations, extracted_licensing_info=extracted_licensing_info,
                        relationships=relationships, packages=[package], files=[file], snippets=[snippet])
    writer.write_document(document, temporary_file_path)

    with open(temporary_file_path) as written_file:
        written_json = json.load(written_file)

    with open(os.path.join(os.path.dirname(__file__), 'expected_results', 'expected.json')) as expected_file:
        expected_json = json.load(expected_file)

    assert written_json == expected_json
