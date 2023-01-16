from typing import Any, Dict

from spdx_tools.common.typing.constructor_type_errors import ConstructorTypeErrors


def check_types_and_set_values(instance_under_construction: Any, local_variables: Dict) -> None:
    """
    Helper method to accumulate all type errors encountered during a constructor call and return them in a
    ConstructorTypeErrors instance.
    Background: Our setters are enhanced with runtime typechecks using beartype. However, this means that by
    default, a TypeError is raised on the first type violation that is encountered. We consider it more helpful to
    return all type violations in one go.
    As an aside, defining constructors "manually" using this utility method helps avoid a nasty PyCharm bug:
    https://youtrack.jetbrains.com/issue/PY-34569
    With the additional parameter origin_class we ensure that the attributes from the class that calls this method
    are set. If we use inheritance the instance_under_construction object might be a child object.
    """
    errors = []
    for key in instance_under_construction.__dataclass_fields__.keys():
        value = local_variables.get(key)
        try:
            setattr(instance_under_construction, key, value)
        except TypeError as err:
            error_message: str = err.args[0]
            errors.append(error_message)
    if errors:
        raise ConstructorTypeErrors(errors)
