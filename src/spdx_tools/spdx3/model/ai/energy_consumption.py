from dataclasses import field

from beartype.typing import List

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model.ai.energy_consumption_description import EnergyConsumptionDescription


@dataclass_with_properties
class EnergyConsumption:
    finetuning_energy_consumption: List[EnergyConsumptionDescription] = field(default_factory=list)
    inference_energy_consumption: List[EnergyConsumptionDescription] = field(default_factory=list)
    training_energy_consumption: List[EnergyConsumptionDescription] = field(default_factory=list)

    def __init__(
        self,
        finetuning_energy_consumption: List[EnergyConsumptionDescription] | None = None,
        inference_energy_consumption: List[EnergyConsumptionDescription] | None = None,
        training_energy_consumption: List[EnergyConsumptionDescription] | None = None,
    ):
        finetuning_energy_consumption = [] if finetuning_energy_consumption is None else finetuning_energy_consumption
        inference_energy_consumption = [] if inference_energy_consumption is None else inference_energy_consumption
        training_energy_consumption = [] if training_energy_consumption is None else training_energy_consumption
        check_types_and_set_values(self, locals())
