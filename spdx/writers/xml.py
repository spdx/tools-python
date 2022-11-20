# Copyright (c) the SPDX tools authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import xml.etree.ElementTree as ET

from spdx import creationinfo, file
from spdx.checksum import CHECKSUM_ALGORITHM_TO_XML_DICT
from spdx.utils import NoAssert, SPDXNone
from spdx.writers.tagvalue import InvalidDocumentError
from spdx.parsers.loggers import ErrorMessages


def add_not_empty(parent, element_name, element_value):
    if element_value is not None:
        ET.SubElement(parent, element_name).text = str(element_value)


def add_checksum(parent, tag, ident, value):
    checksum_element = ET.SubElement(parent, tag)
    ET.SubElement(checksum_element, 'checksumValue').text = value
    algo = CHECKSUM_ALGORITHM_TO_XML_DICT.get(ident) or 'checksumAlgorithm_sha1'
    ET.SubElement(checksum_element, 'algorithm').text = algo


def add_license(parent, tag, new_license):
    license_text = None
    if isinstance(new_license, NoAssert):
        license_text = new_license.to_value()
    elif isinstance(new_license, SPDXNone):
        license_text = 'NONE'
    else:
        license_text = new_license.identifier
    ET.SubElement(parent, tag).text = license_text


def add_version(parent, tag, version):
    ET.SubElement(parent, tag).text = '{}.{}'.format(version.major, version.minor)


def add_pkg_external_reference(parent, ext_ref):
    ext_ref_element = ET.SubElement(parent, 'externalRefs')
    add_not_empty(ext_ref_element, 'referenceCategory', ext_ref.category)
    add_not_empty(ext_ref_element, 'referenceLocator', ext_ref.locator)
    add_not_empty(ext_ref_element, 'referenceType', ext_ref.pkg_ext_ref_type)
    add_not_empty(ext_ref_element, 'comment', ext_ref.comment)


def add_annotation(parent, annotation):
    annotation_element = ET.SubElement(parent, 'annotations')
    add_not_empty(annotation_element, 'annotationDate', annotation.annotation_date)
    add_not_empty(annotation_element, 'annotationType', annotation.annotation_type)
    add_not_empty(annotation_element, 'annotator', annotation.annotator)
    add_not_empty(annotation_element, 'comment', annotation.comment)
    add_not_empty(annotation_element, 'SPDXID', annotation.spdx_id)


def write_document(document, out, validate=True):
    if validate:
        messages = ErrorMessages()
        messages = document.validate(messages)
        if messages:
            raise InvalidDocumentError(messages)

    doc_element = ET.Element('Document')
    add_not_empty(doc_element, 'SPDXID', document.spdx_id)
    add_not_empty(doc_element, 'spdxVersion', str(document.version))
    # creationInfo
    creation_info_element = ET.SubElement(doc_element, 'creationInfo')
    add_not_empty(creation_info_element, 'comment', document.creation_info.comment)
    for creator in document.creation_info.creators:
        if isinstance(creator, creationinfo.Tool):
            ET.SubElement(creation_info_element, 'creators').text = creator.to_value()
        elif isinstance(creator, creationinfo.Person):
            ET.SubElement(creation_info_element, 'creators').text = creator.to_value()
        elif isinstance(creator, creationinfo.Organization):
            ET.SubElement(creation_info_element, 'creators').text = creator.to_value()
    add_not_empty(creation_info_element, 'created', document.creation_info.created_iso_format)
    if document.creation_info.license_list_version is not None:
        add_version(creation_info_element, 'licenseListVersion', document.creation_info.license_list_version)
    #
    add_not_empty(doc_element, 'name', document.name)
    add_not_empty(doc_element, 'dataLicense', document.data_license.identifier)
    add_not_empty(doc_element, 'comment', document.comment)
    # externalDocumentRefs
    for externalDocumentRef in document.ext_document_references:
        external_document_refs_element = ET.SubElement(doc_element, 'externalDocumentRefs')
        add_checksum(external_document_refs_element, 'checksum', externalDocumentRef.check_sum.identifier,
                     externalDocumentRef.check_sum.value)
        add_not_empty(external_document_refs_element, 'spdxDocument', externalDocumentRef.spdx_document_uri)
        add_not_empty(external_document_refs_element, 'externalDocumentId', externalDocumentRef.external_document_id)
    # hasExtractedLicensingInfos
    for extractedLicense in document.extracted_licenses:
        extracted_licensing_infos_element = ET.SubElement(doc_element, 'hasExtractedLicensingInfos')
        add_not_empty(extracted_licensing_infos_element, 'extractedText', extractedLicense.text)
        add_not_empty(extracted_licensing_infos_element, 'comment', extractedLicense.comment)
        add_not_empty(extracted_licensing_infos_element, 'licenseId', extractedLicense.identifier)
        add_not_empty(extracted_licensing_infos_element, 'name', extractedLicense.full_name)
        for see_also in extractedLicense.cross_ref:
            add_not_empty(extracted_licensing_infos_element, 'seeAlsos', see_also)
    # annotations
    for annotation in document.annotations:
        add_annotation(doc_element, annotation)
    # documentDescribes
    for d in document.describes:
        add_not_empty(doc_element, 'documentDescribes', d)
    add_not_empty(doc_element, 'documentNamespace', document.namespace)

    # packages
    for package in document.packages:
        packages_element = ET.SubElement(doc_element, 'packages')
        add_not_empty(packages_element, 'SPDXID', package.spdx_id)
        # annotations
        for annotation in package.annotations:
            add_annotation(packages_element, annotation)
        #
        add_not_empty(packages_element, 'attributionTexts', package.attribution_text)
        add_not_empty(packages_element, 'builtDate', package.built_date)
        # checksums
        for ident, value in package.checksums.items():
            add_checksum(packages_element, 'checksums', ident, value)
        #
        add_not_empty(packages_element, 'copyrightText', package.cr_text)
        add_not_empty(packages_element, 'description', package.description)
        add_not_empty(packages_element, 'downloadLocation', package.download_location)
        # externalRefs
        for ext_ref in package.external_references:
            add_pkg_external_reference(packages_element, ext_ref)
        # filesAnalyzed
        if package.files_analyzed is not None:
            ET.SubElement(packages_element, 'filesAnalyzed').text = 'true' if package.files_analyzed else 'false'
        add_not_empty(packages_element, 'homepage', package.homepage)
        add_not_empty(packages_element, 'licenseComments', package.license_comment)
        if not isinstance(package.conc_lics, SPDXNone):
            add_license(packages_element, 'licenseConcluded', package.conc_lics)
        if not isinstance(package.license_declared, SPDXNone):
            add_license(packages_element, 'licenseDeclared', package.license_declared)
        for license_from_file in package.licenses_from_files:
            add_not_empty(packages_element, 'licenseInfoFromFiles', license_from_file.identifier)
        add_not_empty(packages_element, 'name', package.name)
        add_not_empty(packages_element, 'originator', package.originator)
        add_not_empty(packages_element, 'packageFileName', package.file_name)
        # packageVerificationCode
        if package.verif_code is not None:
            package_verification_code_element = ET.SubElement(packages_element, 'packageVerificationCode')
            add_not_empty(package_verification_code_element, 'packageVerificationCodeValue', package.verif_code)
            for verif_exc_file in package.verif_exc_files:
                add_not_empty(package_verification_code_element, 'packageVerificationCodeExcludedFiles', verif_exc_file)
        # packagePrimaryPurpose
        for package_primary_purpose in package.primary_purpose:
            add_not_empty(packages_element, 'primaryPackagePurpose', package_primary_purpose)
        # this is a weird place for hasFiles -- everything else is more-or-less alphabetic order
        for package_has_file in package.has_files:
            add_not_empty(packages_element, 'hasFiles', package_has_file)
        add_not_empty(packages_element, 'releaseDate', package.release_date)
        add_not_empty(packages_element, 'sourceInfo', package.source_info)
        add_not_empty(packages_element, 'summary', package.summary)
        add_not_empty(packages_element, 'supplier', package.supplier)
        add_not_empty(packages_element, 'validUntilDate', package.valid_until_date)
        add_not_empty(packages_element, 'versionInfo', package.version)

    # files
    for phile in document.files:
        file_element = ET.SubElement(doc_element, 'files')
        add_not_empty(file_element, 'SPDXID', phile.spdx_id)
        # annotations
        for annotation in phile.annotations:
            add_annotation(file_element, annotation)
        # checksums
        for ident, value in phile.checksums.items():
            add_checksum(file_element, 'checksums', ident, value)
        add_not_empty(file_element, 'comment', phile.comment)
        add_not_empty(file_element, 'copyrightText', phile.copyright)
        # fileContributors
        for contributor in phile.contributors:
            add_not_empty(file_element, 'fileContributors', contributor)
        add_not_empty(file_element, 'fileName', phile.name)
        # fileTypes
        for file_type in phile.file_types:
            file_type_name = file.FILE_TYPE_TO_XML_DICT.get(file_type)
            if file_type_name is None:
                raise RuntimeError('unknown file type {}'.format(file_type))
            add_not_empty(file_element, 'fileTypes', file_type_name)
        add_license(file_element, 'licenseConcluded', phile.conc_lics)
        add_not_empty(file_element, 'licenseComments', phile.license_comment)

        for license_in_file in phile.licenses_in_file:
            add_license(file_element, 'licenseInfoInFiles', license_in_file)

        add_not_empty(file_element, 'noticeText', phile.notice)

        if len(phile.artifact_of_project_name) > 0 or \
                len(phile.artifact_of_project_home) > 0 or \
                len(phile.artifact_of_project_uri) > 0:
            artifact_of_element = ET.SubElement(file_element, 'artifactOf')
            for apn in phile.artifact_of_project_name:
                add_not_empty(artifact_of_element, 'name', apn)
            for aph in phile.artifact_of_project_home:
                add_not_empty(artifact_of_element, 'homePage', aph)
            for apu in phile.artifact_of_project_uri:
                add_not_empty(artifact_of_element, 'projectUri', apu)
        for ident, value in phile.checksums.items():
            add_checksum(file_element, 'checksums', ident, value)

    # snippets
    for snippet in document.snippet:
        snippets_element = ET.SubElement(doc_element, 'snippets')
        add_not_empty(snippets_element, 'comment', snippet.comment)
        add_not_empty(snippets_element, 'name', snippet.name)
        add_not_empty(snippets_element, 'copyrightText', snippet.copyright)
        add_not_empty(snippets_element, 'licenseConcluded', snippet.conc_lics)
        for license_in_snippet in snippet.licenses_in_snippet:
            add_not_empty(snippets_element, 'licenseInfoInSnippets', license_in_snippet)
        add_not_empty(snippets_element, 'licenseComments', snippet.license_comment)
        add_not_empty(snippets_element, 'SPDXID', snippet.spdx_id)
        add_not_empty(snippets_element, 'snippetFromFile', snippet.snip_from_file_spdxid)
        # add the snippet ranges
        if snippet.ranges is not None and len(snippet.ranges) > 0:
            for ranje in snippet.ranges:
                ranges_element = ET.SubElement(snippets_element, 'ranges')
                end_pointer = ranje.get('endPointer')
                if end_pointer is not None:
                    end_pointer_element = ET.SubElement(ranges_element, 'endPointer')
                    for k, v in end_pointer.items():
                        add_not_empty(end_pointer_element, k, v)
                start_pointer = ranje.get('startPointer')
                if start_pointer is not None:
                    start_pointer_element = ET.SubElement(ranges_element, 'startPointer')
                    for k, v in start_pointer.items():
                        add_not_empty(start_pointer_element, k, v)


    # relationships
    for relationship in document.relationships:
        relationships_element = ET.SubElement(doc_element, 'relationships')
        add_not_empty(relationships_element, 'spdxElementId', relationship.spdxelementid)
        add_not_empty(relationships_element, 'relatedSpdxElement', relationship.relatedspdxelement)
        add_not_empty(relationships_element, 'relationshipType', relationship.relationshiptype)

    # reviewers
    for review in document.reviews:
        reviewers_element = ET.SubElement(doc_element, 'reviewers')
        add_not_empty(reviewers_element, 'comment', review.comment)
        add_not_empty(reviewers_element, 'reviewer', review.reviewer)  # might not work
        add_not_empty(reviewers_element, 'reviewDate', review.review_date_iso_format)

    if hasattr(ET, 'indent'):
        ET.indent(doc_element)

    xml_text = ET.tostring(doc_element)

    out.write(xml_text.decode())
