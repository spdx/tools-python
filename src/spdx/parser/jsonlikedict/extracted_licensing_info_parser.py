# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Dict, List, Optional, Union

from spdx.model.extracted_licensing_info import ExtractedLicensingInfo
from spdx.model.spdx_no_assertion import SpdxNoAssertion
from spdx.parser.jsonlikedict.dict_parsing_functions import parse_field_or_no_assertion
from spdx.parser.parsing_functions import construct_or_raise_parsing_error
from spdx.parser.logger import Logger


class ExtractedLicensingInfoParser:
    logger: Logger

    def __init__(self):
        self.logger = Logger()

    @staticmethod
    def parse_extracted_licensing_info(extracted_licensing_info_dict: Dict) -> ExtractedLicensingInfo:
        license_id: Optional[str] = extracted_licensing_info_dict.get("licenseId")
        extracted_text: Optional[str] = extracted_licensing_info_dict.get("extractedText")
        license_name: Optional[Union[str, SpdxNoAssertion]] = parse_field_or_no_assertion(
            extracted_licensing_info_dict.get("name"))
        cross_references: List[str] = extracted_licensing_info_dict.get("seeAlsos", [])
        comment: Optional[str] = extracted_licensing_info_dict.get("comment")
        extracted_licensing_info = construct_or_raise_parsing_error(ExtractedLicensingInfo,
                                                                    dict(license_id=license_id,
                                                                         extracted_text=extracted_text,
                                                                         comment=comment,
                                                                         license_name=license_name,
                                                                         cross_references=cross_references))
        return extracted_licensing_info
