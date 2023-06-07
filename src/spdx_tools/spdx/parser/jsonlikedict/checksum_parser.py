# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Dict, Optional

from spdx_tools.spdx.model import Checksum, ChecksumAlgorithm
from spdx_tools.spdx.parser.jsonlikedict.dict_parsing_functions import json_str_to_enum_name
from spdx_tools.spdx.parser.logger import Logger
from spdx_tools.spdx.parser.parsing_functions import (
    construct_or_raise_parsing_error,
    raise_parsing_error_if_logger_has_messages,
)


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
