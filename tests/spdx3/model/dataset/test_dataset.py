# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import mock

import pytest

from spdx_tools.spdx3.model.dataset import ConfidentialityLevelType, Dataset, DatasetAvailabilityType


@mock.patch("spdx_tools.spdx3.model.CreationInformation", autospec=True)
def test_correct_initialization(creation_information):
    dataset = Dataset(
        "some_spdx_id",
        creation_information,
        data_collection_process="data collection process",
        intended_use="intended use",
        dataset_size=420000,
        dataset_noise="dataset noise",
        data_preprocessing_steps="data preprocessing steps",
        sensors={"sensor1": "some value"},
        known_biases="known biases",
        sensitive_personal_information=True,
        anonymization_method_used=["anonymization method"],
        confidentiality_level=ConfidentialityLevelType.RED,
        dataset_update_mechanism="update mechanism",
        dataset_availability=DatasetAvailabilityType.QUERY,
    )

    assert dataset.data_collection_process == "data collection process"
    assert dataset.intended_use == "intended use"
    assert dataset.dataset_size == 420000
    assert dataset.dataset_noise == "dataset noise"
    assert dataset.data_preprocessing_steps == "data preprocessing steps"
    assert dataset.sensors == {"sensor1": "some value"}
    assert dataset.known_biases == "known biases"
    assert dataset.sensitive_personal_information
    assert dataset.anonymization_method_used == ["anonymization method"]
    assert dataset.confidentiality_level == ConfidentialityLevelType.RED
    assert dataset.dataset_update_mechanism == "update mechanism"
    assert dataset.dataset_availability == DatasetAvailabilityType.QUERY


@mock.patch("spdx_tools.spdx3.model.CreationInformation", autospec=True)
def test_invalid_initialization(creation_information):
    with pytest.raises(TypeError) as err:
        Dataset(
            "some_spdx_id",
            creation_information,
            sensors={"sensor1": "value", "sensor2": 250},
        )

    assert err.value.args[0] == [
        (
            "SetterError Dataset: type of argument \"sensors\"['sensor2'] must be one of "
            "(str, NoneType); got int instead: {'sensor1': 'value', 'sensor2': 250}"
        )
    ]
