# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

import pytest
from rdflib import Graph, RDF
from spdx.model.checksum import Checksum, ChecksumAlgorithm

from spdx.model.file import FileType
from spdx.parser.rdf.file_parser import convert_uri_ref_to_file_type, parse_file
from spdx.rdfschema.namespace import SPDX_NAMESPACE


def test_parse_file():
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/file_to_test_rdf_parser.rdf.xml"))
    file_node = graph.value(predicate=RDF.type, object=SPDX_NAMESPACE.File)
    doc_namespace = "https://some.namespace"

    file = parse_file(file_node, graph, doc_namespace)

    assert file.name == "./fileName.py"
    assert file.spdx_id == "SPDXRef-File"
    assert file.checksums == [Checksum(ChecksumAlgorithm.SHA1, "71c4025dd9897b364f3ebbb42c484ff43d00791c")]
    assert file.file_type == [FileType.TEXT]
    assert file.comment == "fileComment"
    assert file.copyright_text == "copyrightText"
    assert file.contributors == ["fileContributor"]
    assert file.license_comment == "licenseComment"
    assert file.notice == "fileNotice"
    assert file.attribution_texts == ["fileAttributionText"]

@pytest.mark.parametrize("uri_ref,expected", [(SPDX_NAMESPACE.fileType_source, FileType.SOURCE),
                                              (SPDX_NAMESPACE.fileType_binary, FileType.BINARY),
                                              (SPDX_NAMESPACE.fileType_archive, FileType.ARCHIVE),
                                              (SPDX_NAMESPACE.fileType_application, FileType.APPLICATION),
                                              (SPDX_NAMESPACE.fileType_audio, FileType.AUDIO),
                                              (SPDX_NAMESPACE.fileType_image, FileType.IMAGE),
                                              (SPDX_NAMESPACE.fileType_text, FileType.TEXT),
                                              (SPDX_NAMESPACE.fileType_video, FileType.VIDEO),
                                              (SPDX_NAMESPACE.fileType_documentation, FileType.DOCUMENTATION),
                                              (SPDX_NAMESPACE.fileType_spdx, FileType.SPDX),
                                              (SPDX_NAMESPACE.fileType_other, FileType.OTHER)])
def test_convert_uri_ref_to_file_type(uri_ref, expected):
    file_type = convert_uri_ref_to_file_type(uri_ref)

    assert file_type == expected

def test_convert_uri_ref_to_file_type_error():
    with pytest.raises(KeyError):
        convert_uri_ref_to_file_type(SPDX_NAMESPACE.filetype_SPDX)
