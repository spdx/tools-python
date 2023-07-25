# SPDX-License-Identifier: Apache-2.0
#
# This file was auto-generated by dev/gen_python_model_from_spec.py
# Do not manually edit!

from ..core import CreationInfo, Element, ElementCollection, ExternalIdentifier, ExternalMap, ExternalReference, IntegrityMethod, NamespaceMap
from beartype.typing import List, Optional
from spdx_tools.common.typing.type_checks import check_types_and_set_values

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties


@dataclass_with_properties
class Bundle(ElementCollection):
    """
    A bundle is a collection of Elements that have a shared context.
    """
    context: Optional[str] = None
    """
    A context gives information about the circumstances or unifying properties that Elements of the bundle have been
    assembled under.
    """

    def __init__(
        self,
        spdx_id: str,
        creation_info: CreationInfo,
        element: List[Element],
        root_element: List[Element],
        name: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        comment: Optional[str] = None,
        verified_using: List[IntegrityMethod] = None,
        external_reference: List[ExternalReference] = None,
        external_identifier: List[ExternalIdentifier] = None,
        extension: Optional[str] = None,
        namespaces: List[NamespaceMap] = None,
        imports: List[ExternalMap] = None,
        context: Optional[str] = None,
    ):
        verified_using = [] if verified_using is None else verified_using
        external_reference = [] if external_reference is None else external_reference
        external_identifier = [] if external_identifier is None else external_identifier
        namespaces = [] if namespaces is None else namespaces
        imports = [] if imports is None else imports
        check_types_and_set_values(self, locals())
