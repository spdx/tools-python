# Copyright 2014 Ahmed H. Ismail

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


class InvalidDocumentError(Exception):

    """Raised if attempting to write an invalid document."""
    pass


def write_seperators(out):
    for i in xrange(0, 4):
        out.write('\n')


def write_creation_info(creation_info, out):
    """Writes out the creation info, does not check if it's valid."""
    out.write('# Creation Info\n\n')
    # Write creators
    for creator in creation_info.creators:
        out.write('Creator: {0}\n'.format(creator.to_value()))
    # write created
    out.write('Created: {0}\n'.format(creation_info.created_iso_format))
    # possible comment
    if creation_info.has_comment():
        out.write(
            'CreatorComment: <text>{0}</text>\n'.format(creation_info.comment))


def write_review(review, out):
    """Writes out the fields of a single review in tag/value format."""
    out.write('# Review\n\n')
    out.write('Reviewer: {0}\n'.format(review.reviewer.to_value()))
    out.write('ReviewDate: {0}\n'.format(review.review_date_iso_format))
    if review.has_comment():
        out.write('ReviewComment: {0}\n'.format(review.comment))


def write_package(package, out):
    pass


def write_extr_licens(lics, out):
    pass


def write_document(document, out):
    """Writes out a tag value representation of the document.
    Out must implement a method write that takes a single string.
    """
    if not document.validate():
        raise InvalidDocumentError()
    # Write out document information
    out.write('# Document Information\n\n')
    out.write('SPDXVersion: SPDX-{0}.{1}\n'.format(document.version.major,
                                                   document.version.minor))
    out.write('DataLicense: {0}\n'.format(document.data_license.identifier))
    if document.has_comment():
        out.write(
            'DocumentComment: <text>{0}</text>\n'.format(document.comment))
    write_seperators(out)
    # Write out creation info
    write_creation_info(document.creation_info, out)
    write_seperators(out)
    # Write out reviews
    for review in document.reviews:
        write_review(review, out)
        write_seperators(out)
    # Write out package info
    write_package(document.package, out)
    write_seperators(out)
    for lic in document.extracted_licenses:
        write_extr_licens(lic)
        write_seperators(out)
