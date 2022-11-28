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

from src.model.relationship import Relationship
from src.parser.logger import Logger


class RelationshipParser:
    logger: Logger

    def __init__(self, logger):
        self.logger = logger

    def parse_relationship(self, relationship: Dict) -> Relationship:
        relationship = Relationship()
        return relationship

    def parse_relationships(self, relationship_dict_list: List[Dict]) -> List[Relationship]:
        relationships_list = []
        for relationship_dict in relationship_dict_list:
            relationships_list.append(self.parse_relationship(relationship_dict))
        return relationships_list
