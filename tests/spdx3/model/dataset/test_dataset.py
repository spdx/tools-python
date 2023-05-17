# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from unittest import mock

import pytest

from spdx_tools.spdx3.model.dataset import ConfidentialityLevelType, Dataset, DatasetAvailabilityType
from spdx_tools.spdx3.model.software import SoftwarePurpose


@mock.patch("spdx_tools.spdx3.model.CreationInfo", autospec=True)
def test_correct_initialization(creation_info):
    dataset = Dataset(
        "some_spdx_id",
        "Dataset name",
        ["https://namespace.test#originator"],
        "https://download.test",
        [SoftwarePurpose.DATA],
        datetime(10, 5, 23, 11),
        datetime(11, 5, 24, 12),
        "training data",
        creation_info=creation_info,
        data_collection_process="data collection process",
        intended_use="intended use",
        dataset_size=420000,
        dataset_noise="dataset noise",
        data_preprocessing=["data preprocessing steps"],
        sensor={"sensor1": "some value"},
        known_bias=["known biases"],
        sensitive_personal_information=True,
        anonymization_method_used=["anonymization method"],
        confidentiality_level=ConfidentialityLevelType.RED,
        dataset_update_mechanism="update mechanism",
        dataset_availability=DatasetAvailabilityType.QUERY,
    )

    assert dataset.originated_by == ["https://namespace.test#originator"]
    assert dataset.download_location == "https://download.test"
    assert dataset.purpose == [SoftwarePurpose.DATA]
    assert dataset.built_time == datetime(10, 5, 23, 11)
    assert dataset.release_time == datetime(11, 5, 24, 12)
    assert dataset.dataset_type == "training data"
    assert dataset.data_collection_process == "data collection process"
    assert dataset.intended_use == "intended use"
    assert dataset.dataset_size == 420000
    assert dataset.dataset_noise == "dataset noise"
    assert dataset.data_preprocessing == ["data preprocessing steps"]
    assert dataset.sensor == {"sensor1": "some value"}
    assert dataset.known_bias == ["known biases"]
    assert dataset.sensitive_personal_information
    assert dataset.anonymization_method_used == ["anonymization method"]
    assert dataset.confidentiality_level == ConfidentialityLevelType.RED
    assert dataset.dataset_update_mechanism == "update mechanism"
    assert dataset.dataset_availability == DatasetAvailabilityType.QUERY


@mock.patch("spdx_tools.spdx3.model.CreationInfo", autospec=True)
def test_invalid_initialization(creation_info):
    with pytest.raises(TypeError) as err:
        Dataset(
            "some_spdx_id",
            "Dataset name",
            ["https://namespace.test#originator"],
            "https://download.test",
            [SoftwarePurpose.DATA],
            datetime(10, 5, 23, 11),
            datetime(11, 5, 24, 12),
            "training data",
            creation_info=creation_info,
            sensor={"sensor1": "value", "sensor2": 250},
        )

    assert len(err.value.args[0]) == 1
    for error in err.value.args[0]:
        assert error.startswith("SetterError Dataset:")
