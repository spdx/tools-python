# SPDX-License-Identifier: Apache-2.0
#
# This file was auto-generated by dev/gen_python_model_from_spec.py
# Do not manually edit!

from ..core import CreationInfo, ExternalIdentifier, ExternalReference, IntegrityMethod
from abc import ABC, abstractmethod
from beartype.typing import List, Optional
from dataclasses import field

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties


@dataclass_with_properties
class Element(ABC):
    """
    An Element is a representation of a fundamental concept either directly inherent to the Bill of Materials (BOM)
    domain or indirectly related to the BOM domain and necessary for contextually characterizing BOM concepts and
    relationships. Within SPDX-3.0 structure this is the base class acting as a consistent, unifying, and interoperable
    foundation for all explicit and inter-relatable content objects.
    """
    spdx_id: str
    """
    SpdxId uniquely identifies an Element which may thereby be referenced by other Elements. These references may be
    internal or external. While there may be several versions of the same Element, each one needs to be able to be
    referred to uniquely so that relationships between Elements can be clearly articulated.
    """
    name: Optional[str] = None
    """
    This field identifies the name of an Element as designated by the creator. The name of an Element is an important
    convention and easier to refer to than the URI.
    """
    summary: Optional[str] = None
    """
    A summary is a short description of an Element. Here, the intent is to allow the Element creator to provide concise
    information about the function or use of the Element.
    """
    description: Optional[str] = None
    """
    This field is a detailed description of the Element. It may also be extracted from the Element itself. The intent is
    to provide recipients of the SPDX file with a detailed technical explanation of the functionality, anticipated use,
    and anticipated implementation of the Element. This field may also include a description of improvements over prior
    versions of the Element.
    """
    comment: Optional[str] = None
    """
    A comment is an optional field for creators of the Element to provide comments to the readers/reviewers of the
    document.
    """
    creation_info: CreationInfo
    """
    CreationInfo provides information about the creation of the Element.
    """
    verified_using: List[IntegrityMethod] = field(default_factory=list)
    """
    VerifiedUsing provides an IntegrityMethod with which the integrity of an Element can be asserted.
    """
    external_reference: List[ExternalReference] = field(default_factory=list)
    """
    This field points to a resource outside the scope of the SPDX-3.0 content that provides additional characteristics
    of an Element.
    """
    external_identifier: List[ExternalIdentifier] = field(default_factory=list)
    """
    ExternalIdentifier points to a resource outside the scope of SPDX-3.0 content that uniquely identifies an Element.
    """
    extension: Optional[str] = None
    """
    TODO
    """

    @abstractmethod
    def __init__(self):
        pass
