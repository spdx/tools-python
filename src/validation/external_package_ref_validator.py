from typing import List

from src.model.package import ExternalPackageRef
from src.validation.validation_message import ValidationMessage


def validate_external_package_refs(external_package_refs: List[ExternalPackageRef], parent_id: str) -> List[
    ValidationMessage]:
    validation_messages = []
    for external_package_ref in external_package_refs:
        validation_messages.extend(validate_external_package_ref(external_package_ref, parent_id))

    return validation_messages


def validate_external_package_ref(external_package_ref: ExternalPackageRef, parent_id: str) -> List[ValidationMessage]:
    # TODO: https://github.com/spdx/tools-python/issues/373
    return []
