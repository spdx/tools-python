# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

from .general_templates import FILE_HEADER

CLS_FILE = FILE_HEADER + """{imports}
from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties


@dataclass_with_properties
class {typename}({parent}):{docstring}
{properties}
{constructor}"""

CLS_IMPORTS = "from {module} import {types}\n"

CLS_PROP = "    {prop_name}: {prop_type}{default}{docstring}\n"

CLS_INIT = """    def __init__(
        self,{arguments}
    ):{remaps}
        check_types_and_set_values(self, locals())
"""
CLS_INIT_ARG = "\n        {prop_name}: {prop_type},"
CLS_INIT_ARG_OPT = "\n        {prop_name}: {prop_type} = None,"
CLS_INIT_REMAP = "\n        {prop_name} = {default} if {prop_name} is None else {prop_name}"

CLS_INIT_ABSTRACT = """    @abstractmethod
    def __init__(self):
        pass
"""
