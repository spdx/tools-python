# Copyright (c) Xavier Figueroa
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from spdx.writers.tagvalue import InvalidDocumentError
from spdx.writers.jsonyamlxml import Writer
from spdx.parsers.loggers import ErrorMessages
import numpy as np
import datetime


# this method has been added by the WhiteSouse PS Team.
def json_converter(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, datetime.datetime):
        return obj.__str__()


def write_document(document, out, validate=True):

    if validate:
        messages = ErrorMessages()
        messages = document.validate(messages)
        if messages:
            raise InvalidDocumentError(messages)

    writer = Writer(document)
    document_object = writer.create_document()
    json.dump(document_object, out, indent=4, default=json_converter)
