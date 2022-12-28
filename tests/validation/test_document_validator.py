#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from typing import List

from src.model.document import Document
from src.validation.document_validator import validate_full_spdx_document
from src.validation.validation_message import ValidationMessage
from tests.valid_defaults import get_creation_info, get_package, get_file, get_snippet, get_annotation, \
    get_relationship, get_extracted_licensing_info


def test_valid_document():
    document = Document(get_creation_info(), [get_package(), get_package()], [get_file(), get_file()],
                        [get_snippet(), get_snippet()], [get_annotation(), get_annotation()],
                        [get_relationship(), get_relationship()],
                        [get_extracted_licensing_info(), get_extracted_licensing_info()])
    validation_messages: List[ValidationMessage] = validate_full_spdx_document(document, "2.3")

    assert validation_messages == []

# TODO: https://github.com/spdx/tools-python/issues/375
