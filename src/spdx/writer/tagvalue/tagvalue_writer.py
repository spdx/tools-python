#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from typing import TextIO

from spdx.model.document import Document
from spdx.writer.tagvalue.annotation_writer import write_annotation
from spdx.writer.tagvalue.creation_info_writer import write_creation_info
from spdx.writer.tagvalue.extracted_licensing_info_writer import write_extracted_licensing_info
from spdx.writer.tagvalue.file_writer import write_file
from spdx.writer.tagvalue.package_writer import write_package
from spdx.writer.tagvalue.relationship_writer import write_relationship
from spdx.writer.tagvalue.snippet_writer import write_snippet
from spdx.writer.tagvalue.tagvalue_writer_helper_functions import write_separator, scan_relationships, \
    get_file_ids_with_contained_snippets, write_optional_heading, write_list_of_elements


def write_document_to_file(document: Document, file_name: str):
    with open(file_name, "w") as out:
        write_document(document, out)


def write_document(document: Document, text_output: TextIO):
    relationships_to_write, contained_files_by_package_id = scan_relationships(document.relationships,
                                                                               document.packages, document.files)
    file_ids_with_contained_snippets = get_file_ids_with_contained_snippets(document.snippets, document.files)
    packaged_file_ids = [file.spdx_id for files_list in contained_files_by_package_id.values()
                         for file in files_list]
    filed_snippet_ids = [snippet.spdx_id for snippets_list in file_ids_with_contained_snippets.values()
                         for snippet in snippets_list]

    text_output.write("## Document Information\n")
    write_creation_info(document.creation_info, text_output)
    write_separator(text_output)

    for snippet in document.snippets:
        if snippet.spdx_id not in filed_snippet_ids:
            write_snippet(snippet, text_output)
            write_separator(text_output)

    for file in document.files:
        if file.spdx_id not in packaged_file_ids:
            write_file(file, text_output)
            write_separator(text_output)
            if file.spdx_id in file_ids_with_contained_snippets:
                write_list_of_elements(file_ids_with_contained_snippets[file.spdx_id], write_snippet, text_output,
                                       with_separator=True)

    for package in document.packages:
        write_package(package, text_output)
        write_separator(text_output)
        if package.spdx_id in contained_files_by_package_id:
            for file in contained_files_by_package_id[package.spdx_id]:
                write_file(file, text_output)
                write_separator(text_output)
                if file.spdx_id in file_ids_with_contained_snippets:
                    write_list_of_elements(file_ids_with_contained_snippets[file.spdx_id], write_snippet, text_output,
                                           with_separator=True)

    write_optional_heading(document.extracted_licensing_info, "## License Information\n", text_output)
    write_list_of_elements(document.extracted_licensing_info, write_extracted_licensing_info, text_output,
                           with_separator=True)

    write_optional_heading(relationships_to_write, "## Relationships\n", text_output)
    write_list_of_elements(relationships_to_write, write_relationship, text_output)
    write_separator(text_output)

    write_optional_heading(document.annotations, "## Annotations\n", text_output)
    write_list_of_elements(document.annotations, write_annotation, text_output, with_separator=True)
