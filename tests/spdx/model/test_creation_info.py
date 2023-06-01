# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime
from unittest import mock

import pytest

from spdx_tools.spdx.model import CreationInfo, Version


@mock.patch("spdx_tools.spdx.model.ExternalDocumentRef", autospec=True)
@mock.patch("spdx_tools.spdx.model.Actor", autospec=True)
def test_correct_initialization(actor, ext_ref):
    creation_info = CreationInfo(
        "version",
        "id",
        "name",
        "namespace",
        [actor, actor],
        datetime(2022, 1, 1),
        "creator_comment",
        "CC0-1.1",
        [ext_ref, ext_ref],
        Version(6, 3),
        "doc_comment",
    )
    assert creation_info.spdx_version == "version"
    assert creation_info.spdx_id == "id"
    assert creation_info.name == "name"
    assert creation_info.document_namespace == "namespace"
    assert creation_info.creators == [actor, actor]
    assert creation_info.created == datetime(2022, 1, 1)
    assert creation_info.creator_comment == "creator_comment"
    assert creation_info.data_license == "CC0-1.1"
    assert creation_info.external_document_refs == [ext_ref, ext_ref]
    assert creation_info.license_list_version == Version(6, 3)
    assert creation_info.document_comment == "doc_comment"


@mock.patch("spdx_tools.spdx.model.Actor", autospec=True)
def test_wrong_type_in_spdx_version(actor):
    with pytest.raises(TypeError):
        CreationInfo(42, "id", "name", "namespace", [actor, actor], datetime(2022, 1, 1))


@mock.patch("spdx_tools.spdx.model.Actor", autospec=True)
def test_wrong_type_in_spdx_id(actor):
    with pytest.raises(TypeError):
        CreationInfo("version", 42, "name", "namespace", [actor, actor], datetime(2022, 1, 1))


@mock.patch("spdx_tools.spdx.model.Actor", autospec=True)
def test_wrong_type_in_name(actor):
    with pytest.raises(TypeError):
        CreationInfo("version", "id", 42, "namespace", [actor, actor], datetime(2022, 1, 1))


@mock.patch("spdx_tools.spdx.model.Actor", autospec=True)
def test_wrong_type_in_document_namespace(actor):
    with pytest.raises(TypeError):
        CreationInfo("version", "id", "name", 42, [actor, actor], datetime(2022, 1, 1))


def test_wrong_type_in_creators():
    with pytest.raises(TypeError):
        CreationInfo("version", "id", "name", "namespace", ["person"], datetime(2022, 1, 1))


@mock.patch("spdx_tools.spdx.model.Actor", autospec=True)
def test_wrong_type_in_created(actor):
    with pytest.raises(TypeError):
        CreationInfo("version", "id", "name", "namespace", [actor, actor], "2022-01-01")


@mock.patch("spdx_tools.spdx.model.Actor", autospec=True)
def test_wrong_type_in_creator_comment(actor):
    with pytest.raises(TypeError):
        CreationInfo(
            "version", "id", "name", "namespace", [actor, actor], datetime(2022, 1, 1), creator_comment=["string"]
        )


@mock.patch("spdx_tools.spdx.model.Actor", autospec=True)
def test_wrong_type_in_data_license(actor):
    with pytest.raises(TypeError):
        CreationInfo("version", "id", "name", "namespace", [actor, actor], datetime(2022, 1, 1), data_license=42)


@mock.patch("spdx_tools.spdx.model.Actor", autospec=True)
def test_wrong_type_in_external_document_refs(actor):
    with pytest.raises(TypeError):
        CreationInfo(
            "version", "id", "name", "namespace", [actor, actor], datetime(2022, 1, 1), external_document_refs=()
        )


@mock.patch("spdx_tools.spdx.model.Actor", autospec=True)
def test_wrong_type_in_license_list_version(actor):
    with pytest.raises(TypeError):
        CreationInfo(
            "version", "id", "name", "namespace", [actor, actor], datetime(2022, 1, 1), license_list_version="6.4"
        )


@mock.patch("spdx_tools.spdx.model.Actor", autospec=True)
def test_wrong_type_in_document_comment(actor):
    with pytest.raises(TypeError):
        CreationInfo(
            "version", "id", "name", "namespace", [actor, actor], datetime(2022, 1, 1), document_comment=["1"]
        )
