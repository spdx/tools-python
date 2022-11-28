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

from src.model.package import Package
from src.parser.logger import Logger


class PackageParser:
    logger: Logger

    def __init__(self, logger: Logger):
        self.logger = logger

    def parse_package(self, package: Dict) -> Package:
        name = package.get("name")

        package = Package(name)
        return package

    def parse_packages(self, packages_dict_list: List[Dict]) -> List[Package]:
        packages_list = []
        for package_dict in packages_dict_list:
            packages_list.append(self.parse_package(package_dict))
        return packages_list

