#  SPDX-FileCopyrightText: 2023 spdx contributors
#
#  SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx3.model.dataset import ConfidentialityLevelType, Dataset, DatasetAvailabilityType


def test_correct_initialization():
    dataset = Dataset(
        "data collection process",
        "intended use",
        420000,
        "dataset noise",
        "data preprocessing steps",
        {"sensor1": "some value"},
        "known biases",
        True,
        ["anonymization method"],
        ConfidentialityLevelType.RED,
        "update mechanism",
        DatasetAvailabilityType.QUERY,
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


def test_invalid_initialization():
    with pytest.raises(TypeError) as err:
        Dataset(sensors={"sensor1": "value", "sensor2": 250})

    assert err.value.args[0] == [
        (
            "SetterError Dataset: type of argument \"sensors\"['sensor2'] must be one of "
            "(str, NoneType); got int instead: {'sensor1': 'value', 'sensor2': 250}"
        )
    ]
