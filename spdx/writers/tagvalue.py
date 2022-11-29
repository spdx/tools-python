# Copyright (c) 2014 Ahmed H. Ismail
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from itertools import zip_longest
from typing import List, TextIO, Tuple, Dict

from spdx import license, utils
from spdx import file as spdx_file
from spdx.document import Document
from spdx.file import File
from spdx.package import Package
from spdx.parsers.loggers import ErrorMessages
from spdx.relationship import Relationship
from spdx.snippet import Snippet
from spdx.version import Version


class InvalidDocumentError(Exception):
    """
    Raised when attempting to write an invalid document.
    """

    pass


def write_separator(out):
    out.write("\n")


def write_separators(out):
    out.write("\n" * 2)


def format_verif_code(package):
    if len(package.verif_exc_files) == 0:
        return package.verif_code
    else:
        return "{0} ({1})".format(package.verif_code, ",".join(package.verif_exc_files))


def write_value(tag, value, out):
    out.write("{0}: {1}\n".format(tag, value))


def write_range(tag, value, out):
    out.write("{0}: {1}:{2}\n".format(tag, value[0], value[1]))


def write_text_value(tag, value, out):
    if "\n" in value:
        out.write("{0}: <text>{1}</text>\n".format(tag, value))
    else:
        write_value(tag, value, out)


def write_creation_info(creation_info, out):
    """
    Write the creation info to out.
    """
    out.write("# Creation Info\n\n")
    # Write sorted creators
    for creator in sorted(creation_info.creators):
        write_value("Creator", creator, out)

    # write created
    write_value("Created", creation_info.created_iso_format, out)
    # possible comment
    if creation_info.has_comment:
        write_text_value("CreatorComment", creation_info.comment, out)


def write_review(review, out):
    """
    Write the fields of a single review to out.
    """
    write_value("Reviewer", review.reviewer, out)
    write_value("ReviewDate", review.review_date_iso_format, out)
    if review.has_comment:
        write_text_value("ReviewComment", review.comment, out)


def write_annotation(annotation, out):
    """
    Write the fields of a single annotation to out.
    """
    write_value("Annotator", annotation.annotator, out)
    write_value("AnnotationDate", annotation.annotation_date_iso_format, out)
    if annotation.has_comment:
        write_text_value("AnnotationComment", annotation.comment, out)
    write_value("AnnotationType", annotation.annotation_type, out)
    if annotation.spdx_id:
        write_value("SPDXREF", annotation.spdx_id, out)


def write_relationship(relationship_term, out):
    """
    Write the fields of relationships to out.
    """
    write_value("Relationship", relationship_term.relationship, out)
    if relationship_term.has_comment:
        write_text_value(
            "RelationshipComment", relationship_term.relationship_comment, out
        )


def write_file_type(ftype, out):
    write_value("FileType", ftype, out)


def write_file(spdx_file, out):
    """
    Write a file fields to out.
    """
    out.write("# File\n\n")
    write_value("FileName", spdx_file.name, out)
    if spdx_file.spdx_id:
        write_value("SPDXID", spdx_file.spdx_id, out)
    for file_type in spdx_file.file_types:
        write_file_type(file_type.name, out)
    for file_checksum in spdx_file.checksums.values():
        write_value("FileChecksum", file_checksum.to_tv(), out)
    if spdx_file.has_optional_field("conc_lics"):
        if isinstance(
            spdx_file.conc_lics, (license.LicenseConjunction, license.LicenseDisjunction)
        ):
            write_value("LicenseConcluded", "({0})".format(spdx_file.conc_lics), out)
        else:
            write_value("LicenseConcluded", spdx_file.conc_lics, out)

    # write sorted list
    for lics in sorted(spdx_file.licenses_in_file):
        write_value("LicenseInfoInFile", lics, out)

    if spdx_file.has_optional_field("copyright"):
        if isinstance(spdx_file.copyright, str):
            write_text_value("FileCopyrightText", spdx_file.copyright, out)
        else:
            write_value("FileCopyrightText", spdx_file.copyright, out)

    if spdx_file.has_optional_field("license_comment"):
        write_text_value("LicenseComments", spdx_file.license_comment, out)

    if spdx_file.has_optional_field("attribution_text"):
        write_text_value("FileAttributionText", spdx_file.attribution_text, out)

    if spdx_file.has_optional_field("comment"):
        write_text_value("FileComment", spdx_file.comment, out)

    if spdx_file.has_optional_field("notice"):
        write_text_value("FileNotice", spdx_file.notice, out)

    for contributor in sorted(spdx_file.contributors):
        write_value("FileContributor", contributor, out)

    for dependency in sorted(spdx_file.dependencies):
        write_value("FileDependency", dependency, out)

    names = spdx_file.artifact_of_project_name
    homepages = spdx_file.artifact_of_project_home
    uris = spdx_file.artifact_of_project_uri

    for name, homepage, uri in sorted(zip_longest(names, homepages, uris)):
        write_value("ArtifactOfProjectName", name, out)
        if homepage is not None:
            write_value("ArtifactOfProjectHomePage", homepage, out)
        if uri is not None:
            write_value("ArtifactOfProjectURI", uri, out)


def write_snippet(snippet, out):
    """
    Write snippet fields to out.
    """
    out.write("# Snippet\n\n")
    write_value("SnippetSPDXID", snippet.spdx_id, out)
    write_value("SnippetFromFileSPDXID", snippet.snip_from_file_spdxid, out)
    if snippet.has_optional_field("copyright"):
        write_text_value("SnippetCopyrightText", snippet.copyright, out)
    write_range("SnippetByteRange", snippet.byte_range, out)
    if snippet.has_optional_field("line_range"):
        write_range("SnippetLineRange", snippet.line_range, out)
    if snippet.has_optional_field("name"):
        write_value("SnippetName", snippet.name, out)
    if snippet.has_optional_field("comment"):
        write_text_value("SnippetComment", snippet.comment, out)
    if snippet.has_optional_field("license_comment"):
        write_text_value("SnippetLicenseComments", snippet.license_comment, out)
    if snippet.has_optional_field("attribution_text"):
        write_text_value("SnippetAttributionText", snippet.attribution_text, out)
    if snippet.has_optional_field("conc_lics"):
        if isinstance(
            snippet.conc_lics, (license.LicenseConjunction, license.LicenseDisjunction)
        ):
            write_value("SnippetLicenseConcluded", "({0})".format(snippet.conc_lics), out)
        else:
            write_value("SnippetLicenseConcluded", snippet.conc_lics, out)
    # Write sorted list
    for lics in sorted(snippet.licenses_in_snippet):
        write_value("LicenseInfoInSnippet", lics, out)


def write_package(package, out):
    """
    Write a package fields to out.
    """
    out.write("# Package\n\n")
    if package.name:
        write_value("PackageName", package.name, out)
    if package.spdx_id:
        write_value("SPDXID", package.spdx_id, out)
    if package.has_optional_field("version"):
        write_value("PackageVersion", package.version, out)
    write_value("PackageDownloadLocation", package.download_location, out)

    if package.has_optional_field("files_analyzed"):
        write_value("FilesAnalyzed", package.files_analyzed, out)

    if package.has_optional_field("summary"):
        write_text_value("PackageSummary", package.summary, out)

    if package.has_optional_field("attribution_text"):
        write_text_value("PackageAttributionText", package.attribution_text, out)

    if package.has_optional_field("source_info"):
        write_text_value("PackageSourceInfo", package.source_info, out)

    if package.has_optional_field("file_name"):
        write_value("PackageFileName", package.file_name, out)

    if package.has_optional_field("supplier"):
        write_value("PackageSupplier", package.supplier, out)

    if package.has_optional_field("originator"):
        write_value("PackageOriginator", package.originator, out)

    for package_checksum in package.checksums.values():
        write_value("PackageChecksum", package_checksum.to_tv(), out)

    if package.has_optional_field("verif_code"):
        write_value("PackageVerificationCode", format_verif_code(package), out)

    if package.has_optional_field("description"):
        write_text_value("PackageDescription", package.description, out)

    if package.has_optional_field("comment"):
        write_text_value("PackageComment", package.comment, out)

    if package.has_optional_field("license_declared"):
        if isinstance(
            package.license_declared,
            (license.LicenseConjunction, license.LicenseDisjunction),
        ):
            write_value(
                "PackageLicenseDeclared", "({0})".format(package.license_declared), out
            )
        else:
            write_value("PackageLicenseDeclared", package.license_declared, out)

    if package.has_optional_field("conc_lics"):
        if isinstance(
            package.conc_lics, (license.LicenseConjunction, license.LicenseDisjunction)
        ):
            write_value("PackageLicenseConcluded", "({0})".format(package.conc_lics), out)
        else:
            write_value("PackageLicenseConcluded", package.conc_lics, out)

    # Write sorted list of licenses.
    for lics in sorted(package.licenses_from_files):
        write_value("PackageLicenseInfoFromFiles", lics, out)

    if package.has_optional_field("license_comment"):
        write_text_value("PackageLicenseComments", package.license_comment, out)

    if package.has_optional_field("cr_text"):
        if isinstance(package.cr_text, str):
            write_text_value("PackageCopyrightText", package.cr_text, out)
        else:
            write_value("PackageCopyrightText", package.cr_text, out)

    if package.has_optional_field("homepage"):
        write_value("PackageHomePage", package.homepage, out)

    for pkg_ref in package.pkg_ext_refs:
        pkg_ref_str = " ".join(
            [pkg_ref.category, pkg_ref.pkg_ext_ref_type, pkg_ref.locator]
        )
        write_value("ExternalRef", pkg_ref_str, out)
        if pkg_ref.comment:
            write_text_value("ExternalRefComment", pkg_ref.comment, out)

    if package.has_optional_field("primary_package_purpose"):
        write_value("PrimaryPackagePurpose", package.primary_package_purpose.name.replace("_", "-"), out)

    if package.has_optional_field("built_date"):
        write_value("BuiltDate", utils.datetime_iso_format(package.built_date), out)

    if package.has_optional_field("release_date"):
        write_value("ReleaseDate", utils.datetime_iso_format(package.release_date), out)

    if package.has_optional_field("valid_until_date"):
        write_value("ValidUntilDate", utils.datetime_iso_format(package.valid_until_date), out)


def write_extracted_licenses(lics, out):
    """
    Write extracted licenses fields to out.
    """
    write_value("LicenseID", lics.identifier, out)

    if lics.full_name is not None:
        write_value("LicenseName", lics.full_name, out)

    if lics.comment is not None:
        write_text_value("LicenseComment", lics.comment, out)

    for xref in sorted(lics.cross_ref):
        write_value("LicenseCrossReference", xref, out)

    write_text_value("ExtractedText", lics.text, out)


def write_document(document, out, validate=True):
    """
    Write an SPDX tag value document.
    - document - spdx.document instance.
    - out - file like object that will be written to.
    Optionally `validate` the document before writing and raise
    InvalidDocumentError if document.validate returns False.
    """
    messages = ErrorMessages()
    messages = document.validate(messages)
    if validate and messages:
        raise InvalidDocumentError(messages)

    # Write out document information
    out.write("# Document Information\n\n")
    write_value("SPDXVersion", str(document.version), out)
    write_value("DataLicense", document.data_license.identifier, out)
    if document.namespace:
        write_value("DocumentNamespace", document.namespace, out)
    if document.name:
        write_value("DocumentName", document.name, out)
    if document.creation_info.license_list_version:
        version: Version = document.creation_info.license_list_version
        write_value("LicenseListVersion", str(version.major) + "." + str(version.minor), out)
    write_value("SPDXID", "SPDXRef-DOCUMENT", out)
    if document.has_comment:
        write_text_value("DocumentComment", document.comment, out)
    for doc_ref in document.ext_document_references:
        doc_ref_str = " ".join(
            [
                doc_ref.external_document_id,
                doc_ref.spdx_document_uri,
                doc_ref.checksum.identifier.name + ": " + doc_ref.checksum.value,
            ]
        )
        write_value("ExternalDocumentRef", doc_ref_str, out)
    write_separators(out)
    # Write out creation info
    write_creation_info(document.creation_info, out)
    write_separators(out)

    # Write sorted reviews
    if document.reviews:
        out.write("# Reviews\n\n")
        for review in sorted(document.reviews):
            write_review(review, out)
            write_separator(out)
        write_separator(out)

    # Write sorted annotations
    if document.annotations:
        out.write("# Annotations\n\n")
        for annotation in sorted(document.annotations):
            write_annotation(annotation, out)
            write_separator(out)
        write_separator(out)

    relationships_to_write, contained_files_by_package_id = scan_relationships(document.relationships,
                                                                               document.packages, document.files)
    contained_snippets_by_file_id = determine_files_containing_snippets(document.snippet, document.files)
    packaged_file_ids = [file.spdx_id for files_list in contained_files_by_package_id.values()
                         for file in files_list]
    filed_snippet_ids = [snippet.spdx_id for snippets_list in contained_snippets_by_file_id.values()
                         for snippet in snippets_list]

    # Write Relationships
    if relationships_to_write:
        out.write("# Relationships\n\n")
        for relationship in relationships_to_write:
            write_relationship(relationship, out)
        write_separators(out)

    # Write snippet info
    for snippet in document.snippet:
        if snippet.spdx_id not in filed_snippet_ids:
            write_snippet(snippet, out)
            write_separators(out)

    # Write file info
    for file in document.files:
        if file.spdx_id not in packaged_file_ids:
            write_file(file, out)
            write_separators(out)
            if file.spdx_id in contained_snippets_by_file_id:
                write_snippets(contained_snippets_by_file_id[file.spdx_id], out)

    # Write out package info
    for package in document.packages:
        write_package(package, out)
        write_separators(out)
        if package.spdx_id in contained_files_by_package_id:
            for file in contained_files_by_package_id[package.spdx_id]:
                write_file(file, out)
                write_separators(out)
                if file.spdx_id in contained_snippets_by_file_id:
                    write_snippets(contained_snippets_by_file_id[file.spdx_id], out)
                    break

    if document.extracted_licenses:
        out.write("# Extracted Licenses\n\n")
        for lic in sorted(document.extracted_licenses):
            write_extracted_licenses(lic, out)
            write_separator(out)
        write_separator(out)


def write_snippets(snippets_to_write: List, out: TextIO) -> None:
    for snippet in snippets_to_write:
        write_snippet(snippet, out)
        write_separators(out)


def scan_relationships(relationships: List[Relationship], packages: List[Package], files: List[File]) \
        -> Tuple[List, Dict]:
    contained_files_by_package_id = dict()
    relationships_to_write = []
    files_by_spdx_id = {file.spdx_id: file for file in files}
    packages_spdx_ids = [package.spdx_id for package in packages]
    for relationship in relationships:
        if relationship.relationship_type == "CONTAINS" and \
            relationship.spdx_element_id in packages_spdx_ids and \
                relationship.related_spdx_element in files_by_spdx_id.keys():
            contained_files_by_package_id.setdefault(relationship.spdx_element_id, []).append(
                files_by_spdx_id[relationship.related_spdx_element])
            if relationship.has_comment:
                relationships_to_write.append(relationship)
        elif relationship.relationship_type == "CONTAINED_BY" and \
            relationship.related_spdx_element in packages_spdx_ids and \
                relationship.spdx_element_id in files_by_spdx_id:
            contained_files_by_package_id.setdefault(relationship.related_spdx_element, []).append(
                files_by_spdx_id[relationship.spdx_element_id])
            if relationship.has_comment:
                relationships_to_write.append(relationship)
        else:
            relationships_to_write.append(relationship)

    return relationships_to_write, contained_files_by_package_id


def determine_files_containing_snippets(snippets: List[Snippet], files: List[File]) -> Dict:
    contained_snippets_by_file_id = dict()
    for snippet in snippets:
        if snippet.snip_from_file_spdxid in [file.spdx_id for file in files]:
            contained_snippets_by_file_id.setdefault(snippet.snip_from_file_spdxid, []).append(snippet)

    return contained_snippets_by_file_id
