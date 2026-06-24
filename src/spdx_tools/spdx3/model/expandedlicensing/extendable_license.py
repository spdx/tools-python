from abc import abstractmethod

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.spdx3.model.simplelicensing.any_license_info import AnyLicenseInfo


@dataclass_with_properties
class ExtendableLicense(AnyLicenseInfo):
    @abstractmethod
    def __init__(self):
        pass
