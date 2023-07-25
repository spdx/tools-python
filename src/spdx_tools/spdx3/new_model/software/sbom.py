# SPDX-License-Identifier: Apache-2.0
#
# This file was auto-generated by dev/gen_python_model_from_spec.py
# Do not manually edit!

from ..core import Bom, CreationInfo, Element, ExternalIdentifier, ExternalMap, ExternalReference, IntegrityMethod, NamespaceMap
from ..software import SbomType
from beartype.typing import List, Optional
from dataclasses import field
from spdx_tools.common.typing.type_checks import check_types_and_set_values

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties


@dataclass_with_properties
class Sbom(Bom):
    """
    A Software Bill of Materials (SBOM) is a collection of SPDX Elements describing a single package. This could include
    details of the content and composition of the product, provenance details of the product and/or its composition,
    licensing information, known quality or security issues, etc.
    """
    sbom_type: List[SbomType] = field(default_factory=list)
    """
    This field is a reasonable estimation of the type of SBOM created from a creator perspective. It is intended to be
    used to give guidance on the elements that may be contained within it. Aligning with the guidance produced in [Types
    of Software Bill of Material (SBOM)
    Documents](https://www.cisa.gov/sites/default/files/2023-04/sbom-types-document-508c.pdf).
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
        sbom_type: List[SbomType] = None,
    ):
        verified_using = [] if verified_using is None else verified_using
        external_reference = [] if external_reference is None else external_reference
        external_identifier = [] if external_identifier is None else external_identifier
        namespaces = [] if namespaces is None else namespaces
        imports = [] if imports is None else imports
        sbom_type = [] if sbom_type is None else sbom_type
        check_types_and_set_values(self, locals())
