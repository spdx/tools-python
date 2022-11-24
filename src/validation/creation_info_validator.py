from typing import List

from src.model.document import CreationInfo
from src.validation.actor_validator import ActorValidator
from src.validation.validation_message import ValidationMessage


class CreationInfoValidator:
    spdx_version: str
    actor_validator: ActorValidator

    def __init__(self, spdx_version):
        self.spdx_version = spdx_version
        self.actor_validator = ActorValidator(spdx_version)

    def validate_creation_info(self, creation_info: CreationInfo) -> List[ValidationMessage]:
        pass
