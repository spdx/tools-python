# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from unittest import mock

import pytest

from spdx_tools.spdx3.model.ai import AIPackage
from spdx_tools.spdx3.model.ai.ai_package import SafetyRiskAssessmentType


@mock.patch("spdx_tools.spdx3.model.CreationInformation", autospec=True)
def test_correct_initialization(creation_information):
    ai_package = AIPackage(
        "some_spdx_id",
        creation_information,
        "AI Package name",
        energy_consumption="energy consumption",
        standard_compliance=["some standard"],
        limitation="limitation",
        type_of_model=["model type"],
        information_about_training="training info",
        information_about_application="app info",
        hyperparameter={"param": "value"},
        model_data_preprocessing="preprocessing steps",
        model_explainability="mechanism",
        sensitive_personal_information=True,
        metric_decision_threshold={"metric1": "threshold", "metric2": None},
        metric={"metric1": "value1", "metric2": None},
        domain=["domain"],
        autonomy_type=True,
        safety_risk_assessment=SafetyRiskAssessmentType.HIGH,
    )

    assert ai_package.energy_consumption == "energy consumption"
    assert ai_package.standard_compliance == ["some standard"]
    assert ai_package.limitation == "limitation"
    assert ai_package.type_of_model == ["model type"]
    assert ai_package.information_about_training == "training info"
    assert ai_package.information_about_application == "app info"
    assert ai_package.hyperparameter == {"param": "value"}
    assert ai_package.model_data_preprocessing == "preprocessing steps"
    assert ai_package.model_explainability == "mechanism"
    assert ai_package.sensitive_personal_information
    assert ai_package.metric_decision_threshold == {"metric1": "threshold", "metric2": None}
    assert ai_package.metric == {"metric1": "value1", "metric2": None}
    assert ai_package.domain == ["domain"]
    assert ai_package.autonomy_type
    assert ai_package.safety_risk_assessment == SafetyRiskAssessmentType.HIGH


@mock.patch("spdx_tools.spdx3.model.CreationInformation", autospec=True)
def test_invalid_initialization(creation_information):
    with pytest.raises(TypeError) as err:
        AIPackage(
            "some_spdx_id",
            creation_information,
            "AI Package name",
            metric={"metric1": "value", "metric2": 250},
        )

    assert err.value.args[0] == [
        (
            "SetterError AIPackage: type of argument \"metric\"['metric2'] must be one of "
            "(str, NoneType); got int instead: {'metric1': 'value', 'metric2': 250}"
        )
    ]
