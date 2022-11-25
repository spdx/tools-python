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
from typing import Dict

from src.model.extracted_licensing_info import ExtractedLicensingInfo
from src.parser.logger import Logger


class ExtractedLicensingParser:
    logger: Logger

    def __init__(self, logger: Logger):
        self.logger = logger

    def parse(self, extracted_licensing_info: Dict) -> ExtractedLicensingInfo:
        extracted_licensing_info = ExtractedLicensingInfo()
        return extracted_licensing_info
