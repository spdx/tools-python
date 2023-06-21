# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from abc import ABC, abstractmethod

from beartype.typing import Any, Dict, Generic, Type, TypeVar

from spdx_tools.spdx.casing_tools import snake_case_to_camel_case
from spdx_tools.spdx.jsonschema.json_property import JsonProperty
from spdx_tools.spdx.model import Document

MISSING_IMPLEMENTATION_MESSAGE = "Must be implemented"

T = TypeVar("T")


class TypedConverter(ABC, Generic[T]):
    """
    Base class for all converters between an instance of the tools-python data model and the corresponding dictionary
    representation, following the json schema. The generic type T is the type according to the data model.
    Each converter has several methods:
    - get_json_type and get_data_model_type: return the data model type and the corresponding JsonProperty subclass.
    These methods are abstract in the base class and need to be implemented in subclasses.
    - json_property_name: converts an enum value of a JsonProperty subclass to the corresponding property name in the
    json schema. The default implementation simply converts from snake case to camel case. Can be overridden in case
    of exceptions like "SPDXID".
    - convert: converts an instance of type T (one of the data model types) to a dictionary representation. In some
    cases, the full document is required (see below). The logic should be generic for all types.
    - requires_full_document: indicates whether the full document is required for conversion. Returns False by
    default, can be overridden as needed for specific types.
    - _get_property_value: Retrieves the value of a specific json property from the data model instance. In some
    cases, the full document is required.
    """

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
                f"{self.get_data_model_type()}. Received {type(instance)} instead."
            )
        if self.requires_full_document() and not document:
            raise ValueError(f"Converter of type {self.__class__} requires the full document")

        result = {}
        for property_name in self.get_json_type():
            property_value = self._get_property_value(instance, property_name, document)
            if property_value is None:
                continue
            result[self.json_property_name(property_name)] = property_value
        return result
