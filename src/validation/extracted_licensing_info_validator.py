from typing import List

from src.model.extracted_licensing_info import ExtractedLicensingInfo
from src.validation.validation_message import ValidationMessage


class ExtractedLicensingInfoValidator:
    spdx_version: str

    def __init__(self, spdx_version):
        self.spdx_version = spdx_version

    def validate_extracted_licensing_infos(self, extracted_licensing_infos: List[ExtractedLicensingInfo]) -> List[ValidationMessage]:
        error_messages = []
        for extracted_licensing_info in extracted_licensing_infos:
            error_messages.extend(self.validate_extracted_licensing_info(extracted_licensing_info))

        return error_messages

    def validate_extracted_licensing_info(self, extracted_licensing_infos: ExtractedLicensingInfo) -> List[ValidationMessage]:
        pass
