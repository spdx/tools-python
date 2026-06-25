import enum
import inspect
import typing
from types import UnionType
from typing import Any, Dict, Optional, Tuple, Union

from semantic_version import Version
from spdx_python_model import v3_0_1 as spdx_3_0

from spdx_tools.spdx3.binding import helpers
from spdx_tools.spdx3.model import (
    Element,
    ExternalIdentifierType,
    ExternalReferenceType,
    ProfileIdentifierType,
    RelationshipType,
)
from spdx_tools.spdx3.model.ai.ai_package import SafetyRiskAssessmentType
from spdx_tools.spdx3.model.ai.energy_unit_type import EnergyUnitType
from spdx_tools.spdx3.model.annotation import AnnotationType
from spdx_tools.spdx3.model.artifact import SupportType
from spdx_tools.spdx3.model.dataset.dataset_package import (
    ConfidentialityLevelType,
    DatasetAvailabilityType,
    DatasetType,
)
from spdx_tools.spdx3.model.hash import HashAlgorithm
from spdx_tools.spdx3.model.lifecycle_scoped_relationship import LifecycleScopeType
from spdx_tools.spdx3.model.presence_type import PresenceType
from spdx_tools.spdx3.model.relationship import RelationshipCompleteness
from spdx_tools.spdx3.model.security.cvss_severity_type import CvssSeverityType
from spdx_tools.spdx3.model.security.exploit_catalog_vuln_assessment_relationship import ExploitCatalogType
from spdx_tools.spdx3.model.security.ssvc_vuln_assessment_relationship import SsvcDecisionType
from spdx_tools.spdx3.model.security.vex_not_affected_vuln_assessment_relationship import VexJustificationType
from spdx_tools.spdx3.model.software import SoftwarePurpose
from spdx_tools.spdx3.model.software.content_identifier import ContentIdentifierType
from spdx_tools.spdx3.model.software.file import FileKindType
from spdx_tools.spdx3.model.software.sbom import SbomType
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.casing_tools import camel_case_to_snake_case


def convert_to_payload(spdx: spdx_3_0.SHACLObjectSet) -> Payload:
    converter = SHACLToSpdx3Converter()

    for shacl_object in spdx.foreach():
        converter.read(shacl_object)

    return converter.payload


BINDING_NAME_TO_ENUM_MAPPING = {
    "ai_autonomyType": PresenceType,
    "ai_energyUnitType": EnergyUnitType,
    "ai_safetyRiskAssessment": SafetyRiskAssessmentType,
    "ai_useSensitivePersonalInformation": PresenceType,
    "dataset_confidentialityLevel": ConfidentialityLevelType,
    "dataset_datasetAvailability": DatasetAvailabilityType,
    "dataset_datasetType": DatasetType,
    "dataset_hasSensitivePersonalInformation": PresenceType,
    "security_catalogType": ExploitCatalogType,
    "security_decisionType": SsvcDecisionType,
    "security_justificationType": VexJustificationType,
    "security_severity": CvssSeverityType,
    "software_additionalPurpose": SoftwarePurpose,
    "software_contentIdentifierType": ContentIdentifierType,
    "software_fileKind": FileKindType,
    "software_primaryPurpose": SoftwarePurpose,
    "software_sbomType": SbomType,
    "annotationType": AnnotationType,
    "externalIdentifierType": ExternalIdentifierType,
    "externalRefType": ExternalReferenceType,
    "algorithm": HashAlgorithm,
    "completeness": RelationshipCompleteness,
    "profileConformance": ProfileIdentifierType,
    "relationshipType": RelationshipType,
    "scope": LifecycleScopeType,
    "supportType": SupportType,
}


def _parse_compact_iri_to_enum(compact_iri: str | None, binding_value: str) -> enum.Enum | None:
    """
    This will attempt to parse a given SPDX 3 compact IRI and value and will either return the parsed enum or a None.

    The compact_iri is the SPDX name of the attribute in the binding class
    The binding_value is the URI value of the enum in the binding class
    For example, if the compact_iri is "security_severity" and it has a binding_value
    of "https://spdx.org/rdf/3.0.1/terms/Security/CvssSeverityType/high", the output should be Severity.HIGH
    """

    if compact_iri is None:
        return None

    enum_class = BINDING_NAME_TO_ENUM_MAPPING.get(compact_iri, None)

    if enum_class:
        enum_value = camel_case_to_snake_case(binding_value.split("/")[-1]).upper()
        return enum_class[enum_value]

    return None


class SHACLToSpdx3Converter:
    payload: Payload

    def __init__(self):
        self.payload = Payload()

    def read(self, obj: spdx_3_0.SHACLObject) -> None:
        parsed_element = self._parse_node(obj)

        if isinstance(parsed_element, Element):
            self.payload.add_element(parsed_element)

    def _parse_node(self, obj: spdx_3_0.SHACLObject) -> Element | tuple:
        target_class = helpers.convert_binding_iri_to_domain_class(obj.get_type())

        if target_class is None:
            raise TypeError(
                (
                    f"Cannot convert abstract binding class '{obj.__class__.__name__}'"
                    "to domain class. There is an issue with the SPDX 3 file."
                )
            )

        # Convert properties and create new instance
        kwargs = self._convert_properties(obj, target_class)

        # Handle special case of Tuple types because we're mapping the SPDX DictionaryEntry to
        # a Tuple[str, str] for later entry into a dict and tuple doesn't accept kwargs
        # this method should only return a tuple within a recursive call, and should only return
        # an Element to read()

        if issubclass(target_class, tuple):
            return tuple(kwargs.values())
        else:
            return target_class(**kwargs)

    # This is needed because the SPDX 3 model's types can be optional, like "a: dict[str, str] | None"
    # or "b: Optional[dict[str, str]]"" and we need to detect these
    def _is_dict(self, param_cls: type | None) -> bool:
        param_type = typing.get_origin(param_cls)
        is_plain_dict = param_type is dict
        is_dict_in_union_type = False
        is_union = param_type is UnionType or param_type is Union
        if is_union:
            # just do one level of checking
            if any(typing.get_origin(arg_cls) is dict for arg_cls in typing.get_args(param_cls)):
                is_dict_in_union_type = True

        return is_plain_dict or is_dict_in_union_type

    def _parse_single_value(self, binding_value: Any, domain_value_class: Any | None, compact_iri: str | None) -> Any:
        if binding_value is None:
            return None

        # Handle special cases
        # In this case, the binding stores versions as strings, but the domain model uses semantic_version.Version
        # and domain_value_class will be Version
        if domain_value_class is Version:
            return Version(binding_value)
        elif isinstance(binding_value, spdx_3_0.SHACLObject):
            if binding_value.NODE_KIND == spdx_3_0.NodeKind.BlankNodeOrIRI:
                # if a node is a BlankNodeOrIRI (i.e. Non-Element class), then it must be converted in place
                return self._parse_node(binding_value)
            else:
                # otherwise, it is an Element class and we just need to return its ID
                return binding_value["@id"]
        else:
            if isinstance(binding_value, str):
                # check if it is an enum
                result: enum.Enum | None = _parse_compact_iri_to_enum(compact_iri, binding_value)
                if result:
                    return result
            return binding_value

    def _convert_properties(self, binding_obj: spdx_3_0.SHACLObject, target_class: type) -> Dict[str, Any]:
        """
        Map properties from binding object to target class.

        Returns a dictionary of parameters to be passed to the target class constructor.
        """

        kwargs: Dict[str, Any] = {}
        # Get target class's initialization parameters
        domain_class_parameters = inspect.signature(target_class.__init__).parameters

        domain_prop_name_to_type: Dict[str, type] = {}
        # make map of domain property name to domain property type
        for param_name, param in domain_class_parameters.items():
            param_cls = param.annotation
            domain_prop_name_to_type[param_name] = param_cls

        # get binding class's properties
        binding_class_properties: list[Tuple[Optional[str], str, Optional[str]]] = list(binding_obj.property_keys())
        for pyname, iri, compact_iri in binding_class_properties:

            binding_value = binding_obj[iri]

            if pyname is None:
                raise Exception(f"pyname missing for '{binding_obj}'")

            # pyname is the name of the property in the binding class i.e. comment or security_modifiedTime
            # iri is the full URI of the property i.e.  https://spdx.org/rdf/3.0.1/terms/Core/comment
            # compact_iri is also the name of the property, but in some cases, like the SPDX id, they will differ

            # special case. Do not try to extract the ID if the binding class is
            # not an Element because only Elements have IDs
            if helpers.is_binding_object_kind_not_iri_and_the_field_is_id(binding_obj, pyname):
                continue

            # change the trimmed pyname to snake case so that it will match the domain class
            # property name and also handle the special cases
            converted_pyname = helpers.get_domain_property_name_from_binding_property_name(pyname)

            param_cls = domain_prop_name_to_type.get(converted_pyname)

            if hasattr(binding_obj, pyname):
                # Handle lists and single values
                if isinstance(binding_value, spdx_3_0.ListProxy):
                    if self._is_dict(param_cls):
                        value = dict(self._parse_single_value(item, param_cls, compact_iri) for item in binding_value)
                    else:
                        # Treat this as a list
                        value = [self._parse_single_value(item, param_cls, compact_iri) for item in binding_value]
                else:
                    value = self._parse_single_value(binding_value, param_cls, compact_iri)

                kwargs[converted_pyname] = value

        return kwargs
