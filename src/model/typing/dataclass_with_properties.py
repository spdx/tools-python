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

    def set_field_with_better_error_message(self, value: field_type):
        try:
            set_field(self, value)
        except TypeError as err:
            error_message: str = f"SetterError {self.__class__.__name__}: {err.args[0]}"
            # As setters are created dynamically, their argument name is always "value". We replace it by the
            # actual name so the error message is more helpful.
            raise TypeError(error_message.replace("value", field_name, 1) + f": {value}")

    return set_field_with_better_error_message


def make_getter(field_name, field_type):
    """helper method to avoid late binding when generating functions in a for loop"""

    @typechecked
    def get_field(self) -> field_type:
        return getattr(self, f"_{field_name}")

    def get_field_with_better_error_message(self) -> field_type:
        try:
            return get_field(self)
        except TypeError as err:
            error_message: str = f"GetterError {self.__class__.__name__}: {err.args[0]}"
            # As getters are created dynamically, their argument name is always "the return value". We replace it by the
            # actual name so the error message is more helpful.
            raise TypeError(
                error_message.replace("the return value", field_name, 1) + f': {getattr(self, f"_{field_name}")}')

    return get_field_with_better_error_message
