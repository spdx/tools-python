# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import TextIO

from spdx3.model.agent import Agent
from spdx3.model.organization import Organization
from spdx3.model.person import Person
from spdx3.model.software_agent import SoftwareAgent
from spdx3.writer.console.element_writer import write_element_properties


def write_agent(agent: Agent, text_output: TextIO, heading: bool = True):
    if heading:
        if isinstance(agent, Person):
            text_output.write("## Person\n")
        if isinstance(agent, Organization):
            text_output.write("## Organization\n")
        if isinstance(agent, SoftwareAgent):
            text_output.write("## SoftwareAgent\n")
    write_element_properties(agent, text_output)
