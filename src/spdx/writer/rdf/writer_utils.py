# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Union, Any

from rdflib import Namespace, Graph, Literal
from rdflib.term import Node



def add_literal_value_if_exists(graph: Graph, parent: Node, predicate: Node, value: Union[Any, list]):
    if not value:
        return
    if not isinstance(value, list):
        graph.add((parent, predicate, Literal(str(value))))
        return

    for element in value:
        element_triple = (parent, predicate, Literal(str(element)))
        graph.add(element_triple)
