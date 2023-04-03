# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest.mock import NonCallableMagicMock


def assert_mock_method_called_with_arguments(mock_object: NonCallableMagicMock, method_name: str, *args):
    assert len(mock_object.method_calls) == len(args)
    for running_index in range(len(args)):
        call = mock_object.method_calls[running_index]
        assert call[0] == method_name
        assert call[1][0] == args[running_index]


def assert_no_mock_methods_called(mock_object: NonCallableMagicMock):
    assert len(mock_object.method_calls) == 0
