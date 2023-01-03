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
from typing import Dict, Optional

from src.model.checksum import Checksum, ChecksumAlgorithm
from src.parser.jsonlikedict.dict_parsing_functions import raise_parsing_error_if_logger_has_messages, json_str_to_enum_name, \
    construct_or_raise_parsing_error
from src.parser.logger import Logger


class ChecksumParser:
    logger: Logger

    def __init__(self):
        self.logger = Logger()

    @staticmethod
    def parse_checksum(checksum_dict: Dict) -> Checksum:
        logger = Logger()
        algorithm: str = json_str_to_enum_name(checksum_dict.get("algorithm", ""))
        try:
            checksum_algorithm = ChecksumAlgorithm[algorithm]
        except KeyError:
            logger.append(f"Invalid ChecksumAlgorithm: {algorithm}")
            checksum_algorithm = None
        checksum_value: Optional[str] = checksum_dict.get("checksumValue")
        raise_parsing_error_if_logger_has_messages(logger, "Checksum")
        checksum = construct_or_raise_parsing_error(Checksum, dict(algorithm=checksum_algorithm, value=checksum_value))
        return checksum
