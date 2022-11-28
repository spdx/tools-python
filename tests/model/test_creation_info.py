from datetime import datetime
from unittest import mock

import pytest

from src.model.document import CreationInfo
from src.model.version import Version


@mock.patch('src.model.actor.Actor', autospec=True)
def test_correct_initialization(actor):
    creation_info = CreationInfo([actor, actor], datetime(2022, 1, 1), "comment", Version(6, 3))
    assert creation_info.creators == [actor, actor]
    assert creation_info.created == datetime(2022, 1, 1)
    assert creation_info.comment == "comment"
    assert creation_info.license_list_version == Version(6, 3)


def test_wrong_type_in_creators():
    with pytest.raises(TypeError):
        CreationInfo(["person"], datetime(2022, 1, 1))


@mock.patch('src.model.actor.Actor', autospec=True)
def test_wrong_type_in_created(actor):
    with pytest.raises(TypeError):
        CreationInfo([actor, actor], "2022-01-01")


@mock.patch('src.model.actor.Actor', autospec=True)
def test_wrong_type_in_comment(actor):
    with pytest.raises(TypeError):
        CreationInfo([actor, actor], datetime(2022, 1, 1), comment=["string"])


@mock.patch('src.model.actor.Actor', autospec=True)
def test_wrong_type_in_license_list_version(actor):
    with pytest.raises(TypeError):
        CreationInfo([actor, actor], datetime(2022, 1, 1), license_list_version="6.4")
