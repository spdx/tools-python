# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import TextIO

from spdx_tools.spdx3.model import Agent, Organization, Person, SoftwareAgent
from spdx_tools.spdx3.writer.console.element_writer import write_element_properties


def write_agent(agent: Agent, text_output: TextIO, heading: bool = True):
    if heading:
        if isinstance(agent, Person):
            text_output.write("## Person\n")
        if isinstance(agent, Organization):
            text_output.write("## Organization\n")
        if isinstance(agent, SoftwareAgent):
            text_output.write("## SoftwareAgent\n")
    write_element_properties(agent, text_output)
