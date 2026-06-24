from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model.ai.energy_unit_type import EnergyUnitType


@dataclass_with_properties
class EnergyConsumptionDescription:
    energy_quantity: float | int = None  # Decimal value
    energy_unit: EnergyUnitType = None

    def __init__(self, energy_quantity: float | int, energy_unit: EnergyUnitType):
        check_types_and_set_values(self, locals())
