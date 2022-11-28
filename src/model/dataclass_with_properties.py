from dataclasses import dataclass

from typeguard import typechecked


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

    @typechecked
    def set_field(self, value: field_type):
        setattr(self, f"_{field_name}", value)

    return set_field


def make_getter(field_name, field_type):
    """helper method to avoid late binding when generating functions in a for loop"""

    @typechecked
    def get_field(self) -> field_type:
        return getattr(self, f"_{field_name}")

    return get_field
