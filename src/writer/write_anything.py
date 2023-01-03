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
from src.formats import file_name_to_format, FileFormat
from src.model.document import Document
from src.writer.json import json_writer
from src.writer.tagvalue import tagvalue_writer


def write_file(document: Document, file_name: str, validate: bool = True):
    output_format = file_name_to_format(file_name)
    if output_format == FileFormat.JSON:
        json_writer.write_document(document, file_name, validate)
    elif output_format == FileFormat.YAML:
        raise NotImplementedError("Currently, the yaml writer is not implemented")
    elif output_format == FileFormat.XML:
        raise NotImplementedError("Currently, the xml writer is not implemented")
    elif output_format == FileFormat.TAG_VALUE:
        tagvalue_writer.write_document_to_file(document, file_name)
    elif output_format == FileFormat.RDF_XML:
        raise NotImplementedError("Currently, the rdf writer is not implemented")
