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
from spdx.parsers.parse_anything import parse_file
import spdx.file as spdxfile

import click


@click.command()
@click.option("--file", prompt="File name", help="The file to be parsed")
@click.option("--force", is_flag=True, help="print information even if there are some parsing errors")
def main(file, force):
    """
    COMMAND-LINE TOOL for parsing file of RDF, XML, JSON, YAML and XML format.

    To use : run `parser` using terminal or run `parser --file <file name>`

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
    print("Package Name: {0}".format(doc.package.name))
    print("Package Version: {0}".format(doc.package.version))
    print(
        "Package Download Location: {0}".format(doc.package.download_location)
    )
    print("Package Homepage: {0}".format(doc.package.homepage))
    if doc.package.check_sum:
        print("Package Checksum: {0}".format(doc.package.check_sum.value))
    print("Package Attribution Text: {0}".format(doc.package.attribution_text))
    print("Package verification code: {0}".format(doc.package.verif_code))
    print(
        "Package excluded from verif: {0}".format(
            ",".join(doc.package.verif_exc_files)
        )
    )
    print("Package license concluded: {0}".format(doc.package.conc_lics))
    print("Package license declared: {0}".format(doc.package.license_declared))
    print("Package licenses from files:")
    for lics in doc.package.licenses_from_files:
        print("\t{0}".format(lics))
    print("Package Copyright text: {0}".format(doc.package.cr_text))
    print("Package summary: {0}".format(doc.package.summary))
    print("Package description: {0}".format(doc.package.description))
    print("Package Files:")
    VALUES = {
        spdxfile.FileType.SOURCE: "SOURCE",
        spdxfile.FileType.OTHER: "OTHER",
        spdxfile.FileType.BINARY: "BINARY",
        spdxfile.FileType.ARCHIVE: "ARCHIVE",
    }
    for f in doc.files:
        print("\tFile name: {0}".format(f.name))
        print("\tFile type: {0}".format(VALUES[f.type]))
        print("\tFile Checksum: {0}".format(f.chk_sum.value))
        print("\tFile license concluded: {0}".format(f.conc_lics))
        print(
            "\tFile license info in file: {0}".format(
                ",".join(map(lambda l: l.identifier, f.licenses_in_file))
            )
        )
        print(
            "\tFile artifact of project name: {0}".format(
                ",".join(f.artifact_of_project_name)
            )
        )

    print("Document Extracted licenses:")
    for lics in doc.extracted_licenses:
        print("\tIdentifier: {0}".format(lics.identifier))
        print("\tName: {0}".format(lics.full_name))
        print("\License Text: {0}".format(lics.text))

    print("Annotations:")
    for an in doc.annotations:
        print("\tAnnotator: {0}".format(an.annotator))
        print("\tAnnotation Date: {0}".format(an.annotation_date))
        print("\tAnnotation Comment: {0}".format(an.comment))
        print("\tAnnotation Type: {0}".format(an.annotation_type))
        print("\tAnnotation SPDX Identifier: {0}".format(an.spdx_id))

        # print(doc.__dict__)

        print("Relationships: ")
        for relation in doc.relationships:
            print("\tRelationship: {0}".format(relation.relationship))
            try:
                print("\tRelationship: {0}".format(relation.comment))
            except:
                continue

if __name__ == "__main__":
    main()
