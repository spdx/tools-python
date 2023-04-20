# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import TextIO

from spdx_tools.spdx3.model.ai import AIPackage
from spdx_tools.spdx3.writer.console.console import write_dict, write_value
from spdx_tools.spdx3.writer.console.software.package_writer import write_package


def write_ai_package(ai_package: AIPackage, text_output: TextIO):
    text_output.write("## AI Package\n")
    write_package(ai_package, text_output, False)

    write_value("energy_consumption", ai_package.energy_consumption, text_output)
    write_value("standards_compliance", ", ".join([entry for entry in ai_package.standards_compliance]), text_output)
    write_value("limitations", ai_package.limitations, text_output)
    write_value("type_of_model", ", ".join([entry for entry in ai_package.type_of_model]), text_output)
    write_value("information_about_training", ai_package.information_about_training, text_output)
    write_value("information_about_application", ai_package.information_about_application, text_output)
    write_dict("hyperparameters", ai_package.hyperparameters, text_output)
    write_value("data_preprocessing_steps", ai_package.data_preprocessing_steps, text_output)
    write_value("model_explainability_mechanisms", ai_package.model_explainability_mechanisms, text_output)
    write_value("sensitive_personal_information", ai_package.sensitive_personal_information, text_output)
    write_dict("metrics_decision_thresholds", ai_package.metrics_decision_thresholds, text_output)
    write_dict("metrics", ai_package.metrics, text_output)
    write_value("domain", ", ".join([entry for entry in ai_package.domain]), text_output)
    write_value("autonomy_type", ai_package.autonomy_type, text_output)
    write_value("safety_risk_assessment", ai_package.safety_risk_assessment, text_output)
