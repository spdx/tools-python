# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from unittest import mock

import pytest

from spdx_tools.spdx3.model.ai import AIPackage
from spdx_tools.spdx3.model.ai.ai_package import SafetyRiskAssessmentType
from spdx_tools.spdx3.model.software import SoftwarePurpose


@mock.patch("spdx_tools.spdx3.model.CreationInfo", autospec=True)
def test_correct_initialization(creation_info):
    ai_package = AIPackage(
        "some_spdx_id",
        "AI Package name",
        ["https://namespace.test#supplier"],
        "https://download.test",
        "1.2:rc2",
        [SoftwarePurpose.SOURCE],
        datetime(12, 5, 23, 11),
        creation_info=creation_info,
        energy_consumption="energy consumption",
        standard_compliance=["some standard"],
        limitation="limitation",
        type_of_model=["model type"],
        information_about_training="training info",
        information_about_application="app info",
        hyperparameter={"param": "value"},
        model_data_preprocessing=["preprocessing steps"],
        model_explainability=["mechanism"],
        sensitive_personal_information=True,
        metric_decision_threshold={"metric1": "threshold", "metric2": None},
        metric={"metric1": "value1", "metric2": None},
        domain=["domain"],
        autonomy_type=True,
        safety_risk_assessment=SafetyRiskAssessmentType.HIGH,
    )

    assert ai_package.supplied_by == ["https://namespace.test#supplier"]
    assert ai_package.download_location == "https://download.test"
    assert ai_package.package_version == "1.2:rc2"
    assert ai_package.purpose == [SoftwarePurpose.SOURCE]
    assert ai_package.release_time == datetime(12, 5, 23, 11)
    assert ai_package.energy_consumption == "energy consumption"
    assert ai_package.standard_compliance == ["some standard"]
    assert ai_package.limitation == "limitation"
    assert ai_package.type_of_model == ["model type"]
    assert ai_package.information_about_training == "training info"
    assert ai_package.information_about_application == "app info"
    assert ai_package.hyperparameter == {"param": "value"}
    assert ai_package.model_data_preprocessing == ["preprocessing steps"]
    assert ai_package.model_explainability == ["mechanism"]
    assert ai_package.sensitive_personal_information
    assert ai_package.metric_decision_threshold == {"metric1": "threshold", "metric2": None}
    assert ai_package.metric == {"metric1": "value1", "metric2": None}
    assert ai_package.domain == ["domain"]
    assert ai_package.autonomy_type
    assert ai_package.safety_risk_assessment == SafetyRiskAssessmentType.HIGH


@mock.patch("spdx_tools.spdx3.model.CreationInfo", autospec=True)
def test_invalid_initialization(creation_info):
    with pytest.raises(TypeError) as err:
        AIPackage(
            "some_spdx_id",
            "AI Package name",
            ["https://namespace.test#supplier"],
            "https://download.test",
            "1.2:rc2",
            [SoftwarePurpose.SOURCE],
            datetime(12, 5, 23, 11),
            creation_info,
            metric={"metric1": "value", "metric2": 250},
        )

    assert len(err.value.args[0]) == 1
    for error in err.value.args[0]:
        assert error.startswith("SetterError AIPackage:")
