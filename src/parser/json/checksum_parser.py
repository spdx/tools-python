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
from typing import Dict, List

from src.model.checksum import Checksum, ChecksumAlgorithm
from src.parser.error import SPDXParsingError
from src.parser.json.dict_parsing_functions import append_list_if_object_could_be_parsed_append_logger_if_not, \
    raise_parsing_error_if_logger_has_messages, \
    raise_parsing_error_without_additional_text_if_logger_has_messages, \
    transform_json_str_to_enum_name, try_construction_raise_parsing_error
from src.parser.logger import Logger


class ChecksumParser:
    auxiliary_logger: Logger

    def __init__(self):
        self.auxiliary_logger = Logger()

    def parse_checksums(self, checksum_dicts_list: List[Dict]) -> List[Checksum]:
        if not checksum_dicts_list:
            raise SPDXParsingError([f"No checksums provided, checksums are mandatory for files."])

        checksum_list = []
        for checksum_dict in checksum_dicts_list:
            checksum_list = append_list_if_object_could_be_parsed_append_logger_if_not(logger=self.auxiliary_logger,
                                                                                       list_to_append=checksum_list,
                                                                                       field=checksum_dict,
                                                                                       method_to_parse=self.parse_checksum)

        raise_parsing_error_without_additional_text_if_logger_has_messages(self.auxiliary_logger)
        return checksum_list

    @staticmethod
    def parse_checksum(checksum_dict: Dict) -> Checksum:
        logger = Logger()
        algorithm = transform_json_str_to_enum_name(checksum_dict.get("algorithm"))
        try:
            checksum_algorithm = ChecksumAlgorithm[algorithm]
        except KeyError:
            logger.append(f"Algorithm {algorithm} not valid for checksum.")
            checksum_algorithm = None
        checksum_value = checksum_dict.get("checksumValue")
        raise_parsing_error_if_logger_has_messages(logger, "Checksum")
        checksum = try_construction_raise_parsing_error(Checksum,
                                                        dict(algorithm=checksum_algorithm, value=checksum_value))
        return checksum
