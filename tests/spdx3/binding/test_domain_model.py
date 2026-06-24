import enum
import importlib
import pkgutil

from spdx_python_model import v3_0_1 as spdx_3_0

import spdx_tools.spdx3.model as model_package
from spdx_tools.spdx3.binding import helpers
from tests.spdx3.helpers import domain_enum_to_binding_name


def test_that_all_binding_properties_and_classes_have_a_domain_mapping():
    """
    This test ensures that (almost) all properties in the binding classes
    have a corresponding property in the domain classes.
    It does this by iterating over all binding classes and their properties,
    converting the property names to their domain equivalents, and checking
    that the domain class has an attribute with that name.
    It does not do type checking of the attributes, just that they exist.
    """
    # get all binding classes with a URI
    for binding_uri, binding_class in filter(
        lambda item: item[0].startswith("https"), spdx_3_0.SHACLObject.CLASSES.items()
    ):
        domain_class = helpers.convert_binding_iri_to_domain_class(binding_uri)

        # Skip classes that are abstract, since we don't need to worry about instances of them
        if domain_class is None:
            continue

        # DictionaryEntry is a special case that does not have a corresponding domain class because the
        # domain handles it as an item in a dict[str, str] instead of a list of DictionaryEntry objects,
        # so skip this one
        if binding_class.__name__ == "DictionaryEntry":
            continue

        # Check that all binding attributes have a corresponding domain attribute
        binding_attributes = helpers.get_binding_attribute_names(binding_class)
        for binding_attribute in binding_attributes:
            # skip spdx_id if the domain class is not Element or a subclass of Element because
            # only Element and its subclasses have spdx_id
            if binding_attribute == "_id" and binding_class.NODE_KIND == spdx_3_0.NodeKind.BlankNodeOrIRI:
                continue

            domain_attribute = helpers.get_domain_property_name_from_binding_property_name(binding_attribute)
            assert hasattr(domain_class, domain_attribute), (
                f"SPDX property '{binding_attribute}' in class '{binding_class.__name__}'"
                f"maps to domain '{domain_class.__name__}::{domain_attribute}', which does not exist"
            )


def get_all_domain_classes() -> list:
    domain_classes = []
    for _, modname, _ in pkgutil.walk_packages(model_package.__path__, model_package.__name__ + "."):
        try:
            module = importlib.import_module(modname)
            for name in dir(module):
                obj = getattr(module, name)
                if isinstance(obj, type) and obj.__module__ == modname:
                    domain_classes.append(obj)
        except ImportError:
            continue

    return domain_classes


def test_that_all_domain_properties_and_classes_have_a_binding_mapping():
    # Test each domain class
    for domain_class in get_all_domain_classes():
        print(f"Testing domain class: {domain_class.__name__}")
        # Skip private classes and imports
        if domain_class.__name__.startswith("_"):
            continue
        # skip ignored cases and individual values
        if domain_class.__name__ in helpers.INDIVIDUAL_ELEMENT_CLASSES:
            print(f"Skipping {domain_class.__name__}")
            continue

        attributes = [attr for attr in dir(domain_class) if not attr.startswith("_")]

        spdx_iri = helpers.get_binding_iri_from_profile_and_domain_class_name(
            helpers.get_spdx_profile_prefix(domain_class), domain_class.__name__
        )

        if issubclass(domain_class, enum.Enum):
            # check if the values match the enum values in the binding
            shacl_class = spdx_3_0.SHACLObject.CLASSES.get(spdx_iri)
            if shacl_class is None:
                raise ValueError(f"Could not find SPDX class for IRI: {spdx_iri}")

            for attribute in attributes:
                print(f"  Checking enum value: {attribute}")
                converted_enum_value = domain_enum_to_binding_name(attribute)
                assert converted_enum_value in shacl_class.NAMED_INDIVIDUALS, (
                    f"Domain enum value '{attribute}' in domain enum '{domain_class.__name__}'"
                    f"does not have a corresponding enum value in binding class '{shacl_class.__name__}'"
                )

        else:
            # check if the IRI exists in the binding and get the class associated with it
            shacl_class = spdx_3_0.SHACLObject.CLASSES.get(spdx_iri)
            if shacl_class is None:
                raise ValueError(f"Could not find SPDX class for IRI: {spdx_iri}")

            # get all properties in the domain class and check that each property maps to
            # a property in the binding class

            # We have to get the properties via the _OBJ_PY_PROPS because we can't use property_keys()
            # as we are not instanciating objects
            binding_properties = shacl_class._OBJ_PY_PROPS.keys()  # pyright: ignore[reportAttributeAccessIssue]
            renamed_properties = {
                helpers.get_domain_property_name_from_binding_property_name(prop) for prop in binding_properties
            }

            if shacl_class.IS_ABSTRACT:
                print(
                    (
                        f"Skipping properties comparison for {spdx_iri} as it"
                        "is abstract and we cannot extract its fields for comparison"
                    )
                )
                continue

            for attribute in attributes:
                if attribute == "spdx_id" and shacl_class.NODE_KIND == spdx_3_0.NodeKind.BlankNodeOrIRI:
                    print(f"skipping spdx_id as {spdx_iri} is a BlankNodeOrIRI and does not have an _id")
                    continue

                assert attribute in renamed_properties, (
                    f"Domain property '{attribute}' in domain class '{domain_class.__name__}'"
                    f"does not have a corresponding property in binding class '{spdx_iri}'"
                )
                print(
                    (
                        f"    Property '{attribute}' in class '{domain_class.__name__}'"
                        f"maps to binding property in class '{shacl_class.__name__}'"
                    )
                )
