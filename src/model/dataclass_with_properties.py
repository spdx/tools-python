from typing import Type, Any


def dataclass_with_properties(cls):
    """decorator to generate properties out of the dataclass value:type list.
    Their getters and setters will be subjected to the @typechecked decorator"""
    for field_name, field_type in cls.__annotations__.items():

        set_field = make_setter(field_name, field_type)
        get_field = make_getter(field_name, field_type)

        setattr(cls, f"set_{field_name}", set_field)
        setattr(cls, f"get_{field_name}", get_field)

        setattr(cls, field_name, property(getattr(cls, f"get_{field_name}"), getattr(cls, f'set_{field_name}')))

    return cls


def make_setter(field_name, field_type):
    """helper method to avoid late binding when generating functions in a for loop"""
    def set_field(self, value: field_type):
        setattr(self, f"_{field_name}", value)

    return set_field


def make_getter(field_name, field_type):
    """helper method to avoid late binding when generating functions in a for loop"""
    def get_field(self) -> field_type:
        return getattr(self, f"_{field_name}")

    return get_field


def get_value_error_message(field_name: str, expected_type: Type, value: Any):
    return f"{field_name} must be {expected_type} but is {type(value)} instead: {value}"
