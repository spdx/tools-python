# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import TextIO

from spdx_tools.spdx3.model.dataset import Dataset
from spdx_tools.spdx3.writer.console.console import write_dict, write_value
from spdx_tools.spdx3.writer.console.software.package_writer import write_package


def write_dataset(dataset: Dataset, text_output: TextIO):
    text_output.write("## AI Package\n")
    write_package(dataset, text_output, False)

    write_value("data_collection_process", dataset.data_collection_process, text_output)
    write_value("intended_use", dataset.intended_use, text_output)
    write_value("dataset_size", dataset.dataset_size, text_output)
    write_value("dataset_noise", dataset.dataset_noise, text_output)
    write_value("data_preprocessing_steps", dataset.data_preprocessing_steps, text_output)
    write_dict("sensors", dataset.sensors, text_output)
    write_value("known_biases", dataset.known_biases, text_output)
    write_value("sensitive_personal_information", dataset.sensitive_personal_information, text_output)
    write_value(
        "anonymization_method_used", ", ".join([entry for entry in dataset.anonymization_method_used]), text_output
    )
    write_value("confidentiality_level", dataset.confidentiality_level, text_output)
    write_value("dataset_update_mechanism", dataset.dataset_update_mechanism, text_output)
    write_value("dataset_availability", dataset.dataset_availability, text_output)
