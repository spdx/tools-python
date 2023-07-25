# SPDX-License-Identifier: Apache-2.0
#
# This file was auto-generated by dev/gen_python_model_from_spec.py
# Do not manually edit!

from spdx_tools.common.typing.type_checks import check_types_and_set_values

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties


@dataclass_with_properties
class MediaType(str):
    """
    The MediaType is a String constrained to the RFC 2046 specification. It provides a standardized way of indicating
    the type of content of an Element. A list of all possible media types is available at
    https://www.iana.org/assignments/media-types/media-types.xhtml.
    """

    def __init__(
        self,
    ):
        check_types_and_set_values(self, locals())
