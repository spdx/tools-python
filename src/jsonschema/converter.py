#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from abc import ABC, abstractmethod
from typing import Any, Type, Dict, TypeVar, Generic

from src.jsonschema.json_property import JsonProperty
from src.model.document import Document
from src.writer.casing_tools import snake_case_to_camel_case

MISSING_IMPLEMENTATION_MESSAGE = "Must be implemented"

T = TypeVar("T")


class TypedConverter(ABC, Generic[T]):

    @abstractmethod
    def _get_property_value(self, instance: T, json_property: JsonProperty, document: Document = None) -> Any:
        raise NotImplementedError(MISSING_IMPLEMENTATION_MESSAGE)

    @abstractmethod
    def get_json_type(self) -> Type[JsonProperty]:
        raise NotImplementedError(MISSING_IMPLEMENTATION_MESSAGE)

    @abstractmethod
    def get_data_model_type(self) -> Type[T]:
        raise NotImplementedError(MISSING_IMPLEMENTATION_MESSAGE)

    def json_property_name(self, json_property: JsonProperty) -> str:
        return snake_case_to_camel_case(json_property.name)

    def requires_full_document(self) -> bool:
        return False

    def convert(self, instance: T, document: Document = None) -> Dict:
        if not isinstance(instance, self.get_data_model_type()):
            raise TypeError(
                f"Converter of type {self.__class__} can only convert objects of type "
                f"{self.get_data_model_type()}. Received {type(instance)} instead.")
        if self.requires_full_document() and not document:
            raise ValueError(f"Converter of type {self.__class__} requires the full document")

        result = {}
        for property_name in self.get_json_type():
            property_value = self._get_property_value(instance, property_name, document)
            if property_value is None:
                continue
            result[self.json_property_name(property_name)] = property_value
        return result
