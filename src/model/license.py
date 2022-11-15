# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from spdx import config


def determine_full_name(identifier: str, full_name: str):
    if full_name is not None:
        return full_name
    # Note: the license map contains both the ids and names of licenses as keys, with the name resp. id as value
    if identifier in config.LICENSE_MAP:
        return config.LICENSE_MAP[identifier]
    return identifier


def determine_identifier(identifier: str, full_name: str):
    if identifier is not None:
        return identifier
    # Note: the license map contains both the ids and names of licenses as keys, with the name resp. id as value
    if full_name in config.LICENSE_MAP:
        return config.LICENSE_MAP[full_name]
    return full_name


class License:
    identifier: str
    full_name: str

    def __init__(self, identifier: str = None, full_name: str = None):
        """Create a new license from identifier, full name or both. If only either identifier or full name is
        provided, we try to retrieve the other value from the list of known licenses. If the license is unknown and
        only one value is provided, both identifier and full name are set to this value."""
        if identifier is None and full_name is None:
            raise ValueError("Must provide either identifier or full name for a license")
        self.identifier = determine_identifier(identifier, full_name)
        self.full_name = determine_full_name(identifier, full_name)
