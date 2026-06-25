from dataclasses import field
from typing import List

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties
from spdx_tools.common.typing.type_checks import check_types_and_set_values
from spdx_tools.spdx3.model.hash import HashAlgorithm
from spdx_tools.spdx3.model.integrity_method import IntegrityMethod


@dataclass_with_properties
class PackageVerificationCode(IntegrityMethod):
    algorithm: HashAlgorithm = None
    hash_value: str = None
    package_verification_code_excluded_file: List[str] = field(default_factory=list)

    def __init__(
        self,
        algorithm: HashAlgorithm,
        hash_value: str,
        package_verification_code_excluded_file: List[str] | None = None,
        comment: str | None = None,
    ):
        package_verification_code_excluded_file = (
            [] if package_verification_code_excluded_file is None else package_verification_code_excluded_file
        )
        check_types_and_set_values(self, locals())
