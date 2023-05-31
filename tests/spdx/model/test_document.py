# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from unittest import mock

from spdx_tools.spdx.model import Document


@mock.patch("spdx_tools.spdx.model.ExtractedLicensingInfo", autospec=True)
@mock.patch("spdx_tools.spdx.model.Relationship", autospec=True)
@mock.patch("spdx_tools.spdx.model.Annotation", autospec=True)
@mock.patch("spdx_tools.spdx.model.Snippet", autospec=True)
@mock.patch("spdx_tools.spdx.model.File", autospec=True)
@mock.patch("spdx_tools.spdx.model.Package", autospec=True)
@mock.patch("spdx_tools.spdx.model.CreationInfo", autospec=True)
def test_correct_initialization(creation_info, package, file, snippet, annotation, relationship, extracted_lic):
    document = Document(
        creation_info,
        [package, package],
        [file, file],
        [snippet, snippet],
        [annotation, annotation],
        [relationship, relationship],
        [extracted_lic, extracted_lic],
    )
    assert document.creation_info == creation_info
    assert document.packages == [package, package]
    assert document.files == [file, file]
    assert document.snippets == [snippet, snippet]
    assert document.annotations == [annotation, annotation]
    assert document.relationships == [relationship, relationship]
    assert document.extracted_licensing_info == [extracted_lic, extracted_lic]


@mock.patch("spdx_tools.spdx.model.CreationInfo", autospec=True)
def test_correct_initialization_with_default_values(creation_info):
    document = Document(creation_info)
    assert document.creation_info == creation_info
    assert document.packages == []
    assert document.files == []
    assert document.snippets == []
    assert document.annotations == []
    assert document.relationships == []
    assert document.extracted_licensing_info == []
