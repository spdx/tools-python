#  Copyright (c) 2023 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from conversion.convert_creation_information import convert_creation_information
from spdx3.model.spdx_document import SpdxDocument

from spdx.model.document import Document as Document2

""" We want to implement a conversion from the data model in src.spdx to the data model in src.spdx3.
    As there are many fundamental differences between these version we want each conversion method to take
    the object from src.spdx and return all objects that the input is translated to."""
def convert_spdx_document(document: Document2) -> SpdxDocument:
    spdx_document: SpdxDocument = convert_creation_information(document.creation_info)

    return spdx_document

