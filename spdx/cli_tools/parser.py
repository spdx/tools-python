#!/usr/bin/env python

# Copyright (c) 2020 Yash Varshney
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from spdx import utils
from spdx.parsers.parse_anything import parse_file
import spdx.file as spdxfile

import click


@click.command()
@click.option("--file", prompt="File name", help="The file to be parsed")
@click.option("--force", is_flag=True, help="print information even if there are some parsing errors")
def main(file, force):
    """
    COMMAND-LINE TOOL for parsing file of RDF, XML, JSON, YAML and XML format.

    To use : run `pyspdxtools_parser` using terminal or run `pyspdxtools_parser --file <file name>`

    """
    doc, errors = parse_file(file)
    if errors:
        print("Errors while parsing: ", errors)
        if not force:
            return 1

    print("doc comment: {0}".format(doc.comment))
    print("Creators:")
    for c in doc.creation_info.creators:
        print("\t{0}".format(c))
    print("Document review information:")
    for review in doc.reviews:
        print("\tReviewer: {0}".format(review.reviewer))
        print("\tDate: {0}".format(review.review_date))
        print("\tComment: {0}".format(review.comment))
    print("Creation comment: {0}".format(doc.creation_info.comment))
    for package in doc.packages:
        print("Package Name: {0}".format(package.name))
        print("Package Version: {0}".format(package.version))
        print(
            "Package Download Location: {0}".format(package.download_location)
        )
        print("Package Homepage: {0}".format(package.homepage))
        for checksum in doc.package.checksums.values():
            print("Package Checksum: {0} {1}".format(checksum.identifier.name, checksum.value))
        print("Package Attribution Text: {0}".format(package.attribution_text))
        print("Package verification code: {0}".format(package.verif_code))
        print(
            "Package excluded from verif: {0}".format(
                ",".join(package.verif_exc_files)
            )
        )
        print("Package license concluded: {0}".format(package.conc_lics))
        print("Package license declared: {0}".format(package.license_declared))
        print("Package licenses from files:")
        for lics in package.licenses_from_files:
            print("\t{0}".format(lics))
        print("Package Copyright text: {0}".format(package.cr_text))
        print("Package summary: {0}".format(package.summary))
        print("Package description: {0}".format(package.description))
        if len(package.pkg_ext_refs) > 0:
            print("Package external references:")
            for ref in package.pkg_ext_refs:
                print(f"\tCategory: {ref.category}")
                print(f"\tType: {ref.pkg_ext_ref_type}")
                print(f"\tLocator: {ref.locator}")
                if ref.comment:
                    print(f"\tComment: {ref.comment}")
    if doc.files:
        print("Files:")
    for f in doc.files:
        print("\tFile name: {0}".format(f.name))
        for file_type in f.file_types:
            print("\tFile type: {0}".format(file_type.name))
        for file_checksum in f.checksums.values():
            print("\tFile Checksum: {0} {1}".format(file_checksum.identifier.name, file_checksum.value))
        print("\tFile license concluded: {0}".format(f.conc_lics))
        print(
            "\tFile license info in file: {0}".format(
                ",".join(
                    map(lambda l: l.identifier if not isinstance(l, (utils.SPDXNone, utils.NoAssert)) else l.to_value(),
                        f.licenses_in_file))
            )
        )
        print(
            "\tFile artifact of project name: {0}".format(
                ",".join(f.artifact_of_project_name)
            )
        )

    if doc.extracted_licenses:
        print("Document Extracted licenses:")
    for lics in doc.extracted_licenses:
        print("\tIdentifier: {0}".format(lics.identifier))
        print("\tName: {0}".format(lics.full_name))
        print("\License Text: {0}".format(lics.text))
    if doc.annotations:
        print("Annotations:")
    for an in doc.annotations:
        print("\tAnnotator: {0}".format(an.annotator))
        print("\tAnnotation Date: {0}".format(an.annotation_date))
        print("\tAnnotation Comment: {0}".format(an.comment))
        print("\tAnnotation Type: {0}".format(an.annotation_type))
        print("\tAnnotation SPDX Identifier: {0}".format(an.spdx_id))

    if doc.relationships:
        print("Relationships: ")
    for relation in doc.relationships:
        print("\tRelationship: {0}".format(relation.relationship))
        try:
            print("\tRelationship: {0}".format(relation.comment))
        except:
            continue


if __name__ == "__main__":
    main()
