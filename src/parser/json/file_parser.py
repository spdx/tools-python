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
from typing import Dict, List, Optional

from spdx.file import File
from src.parser.logger import Logger


class FileParser:
    logger: Logger

    def __init__(self, logger:  Logger):
        self.logger = logger

    def parse_file(self, file_dict: Dict) -> Optional[File]:
        name = file_dict.get("name")
        spdx_id = file_dict.get("SPDXID")
        try:
            file = File(name, spdx_id)
        except ValueError as error:
            self.logger.append(error.args[0])
            return
        return file

    def parse_files(self, file_dict_list) -> List[File]:
        file_list = []
        for file_dict in file_dict_list:
            file_list.append(self.parse_file(file_dict))

        return file_list

