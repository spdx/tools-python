# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from dataclasses import dataclass

from beartype import beartype
from beartype.roar import BeartypeCallHintException


def dataclass_with_properties(cls):
    """Decorator to generate a dataclass with properties out of the class' value:type list.
    Their getters and setters will be subjected to the @typechecked decorator to ensure type conformity."""
    data_cls = dataclass(cls)
    for field_name, field_type in data_cls.__annotations__.items():
        set_field = make_setter(field_name, field_type)
        get_field = make_getter(field_name, field_type)

        setattr(data_cls, field_name, property(get_field, set_field))

    return data_cls


def make_setter(field_name, field_type):
    """helper method to avoid late binding when generating functions in a for loop"""

    @beartype
    def set_field(self, value: field_type):
        setattr(self, f"_{field_name}", value)

    def set_field_with_error_conversion(self, value: field_type):
        try:
            set_field(self, value)
        except BeartypeCallHintException as err:
            error_message: str = f"SetterError {self.__class__.__name__}: {err}"

            # As setters are created dynamically, their argument name is always "value". We replace it by the
            # actual name so the error message is more helpful.
            raise TypeError(error_message.replace("value", field_name, 1) + f": {value}")

    return set_field_with_error_conversion


def make_getter(field_name, field_type):
    """helper method to avoid late binding when generating functions in a for loop"""

    def get_field(self) -> field_type:
        return getattr(self, f"_{field_name}")

    return get_field
