# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Dict, List, Optional, Union

from spdx_tools.spdx.model import ExtractedLicensingInfo, SpdxNoAssertion
from spdx_tools.spdx.parser.jsonlikedict.dict_parsing_functions import parse_field_or_no_assertion
from spdx_tools.spdx.parser.logger import Logger
from spdx_tools.spdx.parser.parsing_functions import construct_or_raise_parsing_error


class ExtractedLicensingInfoParser:
    logger: Logger

    def __init__(self):
        self.logger = Logger()

    @staticmethod
    def parse_extracted_licensing_info(extracted_licensing_info_dict: Dict) -> ExtractedLicensingInfo:
        license_id: Optional[str] = extracted_licensing_info_dict.get("licenseId")
        extracted_text: Optional[str] = extracted_licensing_info_dict.get("extractedText")
        license_name: Optional[Union[str, SpdxNoAssertion]] = parse_field_or_no_assertion(
            extracted_licensing_info_dict.get("name")
        )
        cross_references: List[str] = extracted_licensing_info_dict.get("seeAlsos", [])
        comment: Optional[str] = extracted_licensing_info_dict.get("comment")
        extracted_licensing_info = construct_or_raise_parsing_error(
            ExtractedLicensingInfo,
            dict(
                license_id=license_id,
                extracted_text=extracted_text,
                comment=comment,
                license_name=license_name,
                cross_references=cross_references,
            ),
        )
        return extracted_licensing_info
