import enum
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple, cast

from semantic_version import Version
from spdx_python_model import v3_0_1 as spdx_3_0

from spdx_tools.spdx3.binding import helpers
from spdx_tools.spdx3.model import CreationInfo, Element
from spdx_tools.spdx3.model.positive_integer_range import PositiveIntegerRange
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.casing_tools import snake_case_to_camel_case

base_creationinfo_id = "_:CreationInfo"


def _does_binding_class_exist(value) -> bool:
    binding_name = helpers.get_binding_type_name_from_domain_object(value)
    return binding_name in spdx_3_0.SHACLObject.CLASSES


def _convert_domain_enum_to_binding_uri(value) -> str:
    binding_name = helpers.get_binding_type_name_from_domain_object(value)

    # special case for ExternalRefType because it is called ExternalReferenceType
    # in the domain model but ExternalRefType in the SHACL model
    if binding_name == "ExternalReferenceType":
        shacl_object = spdx_3_0.SHACLObject.CLASSES["ExternalRefType"]()
        return shacl_object.NAMED_INDIVIDUALS[snake_case_to_camel_case(value.name)]
    else:
        shacl_object = spdx_3_0.SHACLObject.CLASSES[binding_name]()
        return shacl_object.NAMED_INDIVIDUALS[snake_case_to_camel_case(value.name)]


class Spdx3ToSHACLConverter:
    creationinfo_str_to_id: Dict[str, str]

    def __init__(self):
        self.creationinfo_str_to_id = {}

    def _convert_value_to_positive_int_range(self, value: PositiveIntegerRange) -> spdx_3_0.PositiveIntegerRange:
        return spdx_3_0.PositiveIntegerRange(
            beginIntegerRange=value.begin_integer_range,
            endIntegerRange=value.end_integer_range,
        )

    def _convert_field_to_property_or_return_id_of_id_haver(
        self,
        value: Element | CreationInfo | list | dict | None,
        shacl_set: spdx_3_0.SHACLObjectSet,
        binding_obj: spdx_3_0.SHACLObject,
        pyname: str,
    ) -> spdx_3_0.SHACLObject | str | bool | int | float | datetime | list | dict | None:
        """Convert a SPDX domain field value to its SHACL representation.

        SPDX 3 properties either contain the ID of another Element (or CreationInfo),
        or the full body of a non-Element, such as an externalIdentifier,
        or a URI or date. This accepts a field's value and returns whatever
        the correct representation of that value is for that field.
        """
        if value is None:
            return None

        id_havers = (Element, CreationInfo)
        if isinstance(value, id_havers):
            # Special case for CreationInfo, since it uniquely has an ID, but is not an Element
            if type(value) is CreationInfo:
                return self._retrieve_or_create_creation_info(value, shacl_set)
            else:
                return cast(Element, value).spdx_id
        elif isinstance(value, list):
            return [
                self._convert_field_to_property_or_return_id_of_id_haver(v, shacl_set, binding_obj, pyname)
                for v in value
            ]
        elif isinstance(value, dict):
            converted_dict = []  # Yes, this is supposed to be a list because the SHACL representation of a dictionary
            # is a list of DictionaryEntry objects
            for k, v in value.items():
                dict_entry: spdx_3_0.DictionaryEntry = spdx_3_0.DictionaryEntry()
                dict_entry.key = k
                converted_value = self._convert_field_to_property_or_return_id_of_id_haver(
                    v, shacl_set, binding_obj, pyname
                )

                if not type(converted_value) is str:
                    raise Exception("Parsing error. Dictionary entry's value should be a string. Dictionary: {value}")

                dict_entry.value = converted_value
                converted_dict.append(dict_entry)
            return converted_dict
        elif isinstance(value, enum.Enum):
            return _convert_domain_enum_to_binding_uri(value)
        elif isinstance(value, (str, bool, int, float)):
            return value
        elif isinstance(value, datetime):
            return value.astimezone(timezone.utc)
        elif isinstance(value, PositiveIntegerRange):
            return self._convert_value_to_positive_int_range(value)
        elif isinstance(value, Version):
            return str(value)
        elif _does_binding_class_exist(value):
            return self._convert_non_element_with_binding_class_to_shacl(value, shacl_set)
        else:
            raise NotImplementedError(f"converter not implemented for type: '{type(value)} and value: {value}'")

    def _convert_non_element_with_binding_class_to_shacl(
        self, obj, shacl_set: spdx_3_0.SHACLObjectSet
    ) -> spdx_3_0.SHACLObject:
        binding_name = helpers.get_binding_type_name_from_domain_object(obj)
        if not _does_binding_class_exist(obj):
            raise TypeError(f"No corresponding SHACL binding class found for {binding_name}")

        shacl_object = spdx_3_0.SHACLObject.CLASSES[binding_name]()
        class_names_to_fields: dict[type, list[str]] = helpers.get_attributes_by_domain_class_hierarchy(obj)

        for class_type, attribute_list in class_names_to_fields.items():
            profile_prefix = helpers.get_spdx_profile_prefix(class_type)

            for attribute_name in attribute_list:
                full_attribute_name: str = helpers.get_binding_property_name_from_element_field_name_and_prefix(
                    attribute_name, profile_prefix
                )
                if hasattr(obj, attribute_name):
                    value = getattr(obj, attribute_name)
                    converted_value = self._convert_field_to_property_or_return_id_of_id_haver(
                        value, shacl_set, shacl_object, full_attribute_name
                    )
                    if converted_value:
                        setattr(shacl_object, full_attribute_name, converted_value)

        return shacl_object

    def convert(self, obj: Payload) -> spdx_3_0.SHACLObjectSet:
        shacl_set: spdx_3_0.SHACLObjectSet = spdx_3_0.SHACLObjectSet()

        for _, element in obj.get_full_map().items():
            self._convert_element_to_shacl(element, shacl_set)
        return shacl_set

    def _retrieve_or_create_creation_info(self, value, shacl_set: spdx_3_0.SHACLObjectSet) -> str:
        if str(value) in self.creationinfo_str_to_id:
            return self.creationinfo_str_to_id[
                str(value)
            ]  # return the ID of the creationinfo that was made previously
        else:
            new_creation_info_id = base_creationinfo_id + str(len(self.creationinfo_str_to_id))
            self.creationinfo_str_to_id[str(value)] = new_creation_info_id
            shacl_set.add(self._convert_creation_info_to_shacl(value, new_creation_info_id))
        return new_creation_info_id

    def _convert_creation_info_to_shacl(
        self, creation_info: CreationInfo, new_creation_info_id
    ) -> spdx_3_0.SHACLObject:
        shacl_object = spdx_3_0.CreationInfo()
        shacl_object.created = creation_info.created.astimezone(timezone.utc)
        for created_by in creation_info.created_by:
            shacl_object.createdBy.append(created_by)
        shacl_object.specVersion = str(creation_info.spec_version)
        shacl_object["@id"] = new_creation_info_id
        for creating_using in creation_info.created_using:
            shacl_object.createdUsing.append(creating_using)
        if creation_info.comment is not None:
            shacl_object.comment = creation_info.comment
        return shacl_object

    def _convert_element_to_shacl(self, element, shacl_set: spdx_3_0.SHACLObjectSet) -> None:
        spdx_type_name = helpers.get_binding_type_name_from_domain_object(element)

        # Dynamically create an instance of the corresponding SHACL class
        binding_obj = spdx_3_0.SHACLObject.CLASSES[spdx_type_name]()

        binding_class_properties: list[Tuple[Optional[str], str, Optional[str]]] = list(binding_obj.property_keys())
        for prop in binding_class_properties:

            # pyname is the name of the property in the binding class i.e. comment or security_modifiedTime
            pyname = prop[0]

            if pyname is None or pyname.isspace():
                raise Exception(f"pyname missing for '{binding_obj}'")

            # special case. Do not try to extract the ID if the binding class is not an Element
            # because only Elements have IDs
            if helpers.is_binding_object_kind_not_iri_and_the_field_is_id(binding_obj, pyname):
                continue

            # change the trimmed pyname to snake case so that it will match the domain
            # class property name and also handle the special cases
            converted_pyname = helpers.get_domain_property_name_from_binding_property_name(pyname)

            if hasattr(element, converted_pyname):
                value = getattr(element, converted_pyname)
                converted_value = self._convert_field_to_property_or_return_id_of_id_haver(
                    value, shacl_set, binding_obj, pyname
                )

                is_string_with_non_empty_value = type(converted_value) is str and len(converted_value) > 0
                is_string = isinstance(converted_value, str)

                if converted_value is not None and (is_string_with_non_empty_value or not is_string):
                    setattr(binding_obj, pyname, converted_value)

        shacl_set.add(binding_obj)
