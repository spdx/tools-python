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


from typing import Optional, List


class ExtractedLicensingInfo:
    license_id: Optional[str]
    extracted_text: Optional[str]
    license_name: Optional[str]
    comment: Optional[str]
    cross_references: List[str]

    def __init__(self, license_id: Optional[str] = None, extracted_text: Optional[str] = None,
                 license_name: Optional[str] = None, comment: Optional[str] = None,
                 cross_references: List[str] = None):
        self.license_id = license_id
        self.extracted_text = extracted_text
        self.license_name = license_name
        self.comment = comment
        self.cross_references = [] if cross_references is None else cross_references
