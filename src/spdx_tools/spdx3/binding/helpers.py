import importlib
import inspect
import os
from typing import Dict, List, Optional

from spdx_python_model import v3_0_1 as spdx_3_0

from spdx_tools.spdx3.model.element import Element
from spdx_tools.spdx.casing_tools import camel_case_to_snake_case, snake_case_to_camel_case

FIRST_PART_OF_IRI = "https://spdx.org/rdf"
SPDX_VERSION = "3.0.1"


# These should not be instantiated and will only every be referenced as an URI,
# so we don't want to try to map them to a domain class
INDIVIDUAL_ELEMENT_CLASSES = {
    "IndividualElement",  # concrete class for individuals of Element
    "IndividualLicensingInfo",  # concrete class for individuals of LicensingInfo
    "NoAssertionElement",  # the rest are individuals that should only be represented as URIs
    "NoneElement",
    "SpdxOrganization",
    "NoAssertionLicense",
    "NoneLicense",
}


LOWER_CASE_TO_CORRECT_CASE_PROFILE_NAMES = {
    "core": "Core",
    "software": "Software",
    "security": "Security",
    "simplelicensing": "SimpleLicensing",
    "expandedlicensing": "ExpandedLicensing",
    "dataset": "Dataset",
    "ai": "AI",
    "build": "Build",
    "extension": "Extension",
}


def convert_binding_iri_to_domain_class(iri: str) -> Optional[type]:
    """
    Converts a binding class IRI () to the corresponding domain class type if one exists.
    Returns None if there is no corresponding domain class that would be instantiated,
    such as for Individuals such as NoAssertionElement or NoneLicense, who should only be represented
    as URI strings in the domain model. Or if the type is abstract.
    Raises an exception if the domain class cannot be found and the binding class is not abstract.
    """

    # check if the IRI is valid and if it is for an individual that is abstract
    shacl_class = spdx_3_0.SHACLObject.CLASSES.get(iri)
    if shacl_class is None:
        raise ValueError(f"Could not find SPDX class for IRI: {iri}")

    if shacl_class.IS_ABSTRACT:
        return None

    profile = "Core"
    relevant_path = iri.replace(FIRST_PART_OF_IRI + "/" + SPDX_VERSION + "/terms/", "")
    split_path = relevant_path.split("/")

    if len(split_path) != 2:
        raise ValueError("Failed to convert SPDX IRI. Did the IRI format change?")

    profile = split_path[0].lower()

    class_name = split_path[1]

    if class_name in INDIVIDUAL_ELEMENT_CLASSES:
        return None

    # check special name cases because these names don't match the spdx class names
    if class_name == "ExternalRef":
        class_name = "ExternalReference"
    if class_name == "ExternalRefType":
        class_name = "ExternalReferenceType"

    # this is here because SPDX 3.0.1 DictionaryEntry is represented in
    # Python by tuple[str, str]
    if class_name == "DictionaryEntry":
        return tuple

    # special case for the core profile because it is not in a subdirectory
    module_name = "spdx_tools.spdx3.model"
    if profile != "core":
        module_name += f".{profile}"
    try:
        target_module = importlib.import_module(module_name)
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            f"Could not find module '{module_name}'. It probably hasn't been implemented yet."
        ) from e

    try:
        return getattr(target_module, class_name)
    except AttributeError as e:
        raise AttributeError(
            (
                f"Could not find domain class '{class_name}' in module '{module_name}'."
                "It probably hasn't been implemented yet or was not added to its module's __init__.py file"
            )
        ) from e


def get_binding_type_name_from_domain_object(element: Element) -> str:
    """
    Returns the SPDX type name for an element, including profile prefix if applicable.
    For example: "software_Package" or "CreationInfo"
    """
    profile_prefix = get_spdx_profile_prefix(type(element))
    type_name = element.__class__.__name__
    return get_binding_type_name_from_profile_and_domain_class_name(profile_prefix, type_name)


def get_binding_type_name_from_profile_and_domain_class_name(profile: str, domain_class_name: str) -> str:
    profile_prefix = profile.lower()
    type_name = domain_class_name

    # special case for external reference
    if type_name == "ExternalReference":
        type_name = "ExternalRef"

    return f"{profile_prefix}_{type_name}".strip("_")


def get_binding_iri_from_profile_and_domain_class_name(profile: str, domain_class_name: str) -> str:
    if profile not in LOWER_CASE_TO_CORRECT_CASE_PROFILE_NAMES and profile != "":
        raise ValueError(
            (
                f"Unknown SPDX profile name: '{profile}'. Known profiles are: "
                f"{list(LOWER_CASE_TO_CORRECT_CASE_PROFILE_NAMES.keys())} or empty string for core profile"
            )
        )

    iri_case_profile_name = LOWER_CASE_TO_CORRECT_CASE_PROFILE_NAMES.get(profile.lower(), "Core")

    class_name = domain_class_name
    if class_name == "ExternalReference":
        class_name = "ExternalRef"
    if class_name == "ExternalReferenceType":
        class_name = "ExternalRefType"

    return f"{FIRST_PART_OF_IRI}/{SPDX_VERSION}/terms/{iri_case_profile_name}/{class_name}"


def get_binding_attribute_names(binding_class) -> set[str]:
    return {py_name for py_name, iri, compact in binding_class().property_keys()}


def _get_class_directory_name(obj: object) -> str:
    """
    Returns the directory that the passed in class is defined in.

    This is used for finding the name of the directory that an implementation
    of an Element is in, which is the same as its profile.
    """
    # If we're passed an instance, get its class
    if not isinstance(obj, type):
        obj = obj.__class__

    # Get the module of the class
    module = inspect.getmodule(obj)
    if not module:
        return ""

    # Get the file path of the module
    file_path = module.__file__
    if not file_path:
        return ""

    # Get the directory containing the file
    dir_path = os.path.dirname(file_path)

    # Return just the name of the directory (not the full path)
    return os.path.basename(dir_path)


def get_spdx_profile_prefix(element: type) -> str:
    """
    Returns the profile prefix of a domain element type.
    """
    directory_name = _get_class_directory_name(element)

    # If the class is in the model directory, then it is part of the Core profile and does not have a profile prefix
    if directory_name == "model":
        directory_name = ""

    return directory_name


def get_attributes_by_domain_class_hierarchy(obj: object) -> Dict[type, List[str]]:
    """
    Returns a list of tuples containing each parent class name and the attributes
    defined in that class (including the class itself).

    Args:
        obj: The object to analyze

    Returns:
        List of tuples of (class_name, [attribute_names]) for each class in the inheritance hierarchy
    """
    # Get the class of the object if an instance was provided
    cls = obj if isinstance(obj, type) else obj.__class__

    # Get the Method Resolution Order (MRO) - the inheritance hierarchy
    class_hierarchy = cls.__mro__

    result = {}
    all_attrs = set()  # Track attributes we've already seen

    # Stop at these classes as that is as far down the class hierarchy as we need to go
    stop_classes = {
        "Element",
        "CreationInfo",
        "ExternalIdentifier",
        "ExternalMap",
        "DictionaryEntry",
        "ExternalRef",
        "PositiveIntegerRange",
        "NamespaceMap",
        "IntegrityMethod",
        "Hash",
        "PackageVerificationCode",
    }

    # Iterate through each class in the hierarchy
    for parent_class in class_hierarchy:
        # Get all attributes defined directly in this class (not inherited)
        class_attrs = set()
        for attr_name in parent_class.__dict__.keys():
            # Skip private/special attributes and methods
            if not attr_name.startswith("__") and not attr_name.startswith("_abc_"):
                class_attrs.add(attr_name)

        # Remove attributes already found in child classes
        unique_attrs = class_attrs - all_attrs
        all_attrs.update(unique_attrs)

        # Add to result if there are any attributes
        if unique_attrs:
            result[parent_class] = sorted(unique_attrs)
        if parent_class.__name__ in stop_classes:
            break

    return result


def get_binding_property_name_from_element_field_name_and_prefix(element_field_name: str, profile_prefix: str) -> str:
    # special cases
    # the spdx_id field is always mapped to _id in the binding classes
    if element_field_name == "spdx_id":
        return "_id"

    field_name = element_field_name
    if field_name == "from_element":
        return "from_"

    if field_name == "external_reference":
        return "externalRef"

    if field_name == "external_reference_type":
        return "externalRefType"

    if field_name == "imports":
        return "import_"

    return f"{profile_prefix}_{snake_case_to_camel_case(field_name)}".strip("_")


def get_domain_property_name_from_binding_property_name(binding_property_name: str) -> str:
    # Special cases. These do not follow the naming conventions.
    if binding_property_name == "_id":
        return "spdx_id"
    elif binding_property_name == "from_":
        return "from_element"
    elif binding_property_name == "externalRef":
        return "external_reference"
    elif binding_property_name == "externalRefType":
        return "external_reference_type"
    elif binding_property_name == "import_":
        return "imports"

    # Typical cases
    if "_" in binding_property_name:
        # A profile prefix is present because there is a "_" present.
        # Remove it because the domain model's property names do not have profile prefixes.
        # These binding_property_name(s) are formatted like "software_Package",
        # "simplelicensing_LicenseAddition", or "ElementCollection".
        prefix, _, suffix = binding_property_name.partition("_")
        if len(suffix) == 0:
            # this shouldn't happen, but just in case
            domain_property_name = prefix
        else:
            domain_property_name = suffix
    else:
        # This is a "core" profile property, so it doesn't have a profile prefix
        domain_property_name = binding_property_name

    # The (Python) domain properties are Python properties, so they are snake case
    return camel_case_to_snake_case(domain_property_name)


def is_binding_object_kind_not_iri_and_the_field_is_id(binding_obj, pyname: str) -> bool:
    return (
        isinstance(binding_obj, spdx_3_0.SHACLObject)
        and binding_obj.NODE_KIND != spdx_3_0.NodeKind.IRI
        and pyname == "_id"
    )
