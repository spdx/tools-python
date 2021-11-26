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


def add_checksum(parent, tag, new_checksum):
    checksum_element = ET.SubElement(parent, tag)
    ET.SubElement(checksum_element, 'checksumValue').text = new_checksum.value
    algo = CHECKSUM_ALGORITHM_TO_XML_DICT.get(new_checksum.identifier) or 'checksumAlgorithm_sha1'
    ET.SubElement(checksum_element, 'algorithm').text = algo


def add_license(parent, tag, new_license):
    license_text = None
    if isinstance(new_license, NoAssert):
        license_text = new_license.to_value()
    elif isinstance(license_text, SPDXNone):
        license_text = 'NONE'
    else:
        license_text = new_license.identifier
    ET.SubElement(parent, tag).text = license_text


def add_version(parent, tag, version):
    ET.SubElement(parent, tag).text = '{}.{}'.format(version.major, version.minor)


def write_document(document, out, validate=True):
    if validate:
        messages = ErrorMessages()
        messages = document.validate(messages)
        if messages:
            raise InvalidDocumentError(messages)

    spdx_doc_element = ET.Element('SpdxDocument')
    doc_element = ET.SubElement(spdx_doc_element, 'Document')
    add_not_empty(doc_element, 'comment', document.comment)
    add_not_empty(doc_element, 'name', document.name)
    document_describes_element = ET.SubElement(doc_element, 'documentDescribes')
    for package in document.packages:
        packages_element = ET.SubElement(document_describes_element, 'Package')
        add_not_empty(packages_element, 'SPDXID', package.spdx_id)
        add_not_empty(packages_element, 'originator', package.originator)
        add_not_empty(packages_element, 'attributionTexts', package.attribution_text)
        for phile in package.files:
            file_element = ET.SubElement(packages_element, 'File')
            add_not_empty(file_element, 'comment', phile.comment)
            for license_in_file in phile.licenses_in_file:
                add_license(file_element, 'licenseInfoFromFiles', license_in_file)
            sha1 = None
            for checksum in phile.chk_sums:
                if checksum.identifier == 'SHA1':
                    sha1 = checksum.value
                    break
            add_not_empty(file_element, 'sha1', sha1)
            add_not_empty(file_element, 'name', phile.name)
            add_not_empty(file_element, 'copyrightText', phile.copyright)
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
            add_license(file_element, 'licenseConcluded', phile.conc_lics)
            add_not_empty(file_element, 'licenseComments', phile.license_comment)
            for checksum in phile.chk_sums:
                add_checksum(file_element, 'checksum', checksum)
            for file_type in phile.file_types:
                file_type_name = file.FILE_TYPE_TO_XML_DICT.get(file_type)
                if file_type_name is None:
                    raise RuntimeError('unknown file type {}'.format(file_type))
                add_not_empty(file_element, 'fileType', file_type_name)
            add_not_empty(file_element, 'SPDXID', phile.spdx_id)

        for license_from_file in package.licenses_from_files:
            add_not_empty(packages_element, 'licenseInfoFromFiles', license_from_file.identifier)
        add_not_empty(packages_element, 'sha1', package.check_sum.value)
        add_not_empty(packages_element, 'name', package.name)
        add_not_empty(packages_element, 'packageFileName', package.file_name)
        add_not_empty(packages_element, 'licenseComments', package.license_comment)
        add_not_empty(packages_element, 'summary', package.summary)
        add_not_empty(packages_element, 'sourceInfo', package.source_info)
        add_not_empty(packages_element, 'copyrightText', package.cr_text)
        package_verification_code_element = ET.SubElement(packages_element, 'packageVerificationCode')
        add_not_empty(package_verification_code_element, 'packageVerificationCodeValue', package.verif_code)
        for verif_exc_file in package.verif_exc_files:
            add_not_empty(package_verification_code_element, 'packageVerificationCodeExcludedFiles', verif_exc_file)
        add_license(packages_element, 'licenseConcluded', package.conc_lics)
        add_not_empty(packages_element, 'supplier', package.supplier)
        add_checksum(packages_element, 'checksum', package.check_sum)
        add_not_empty(packages_element, 'versionInfo', package.version)
        add_license(packages_element, 'licenseDeclared', package.license_declared)
        add_not_empty(packages_element, 'downloadLocation', package.download_location)
        add_not_empty(packages_element, 'description', package.description)
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
    # externalDocumentRefs
    for externalDocumentRef in document.ext_document_references:
        external_document_refs_element = ET.SubElement(doc_element, 'externalDocumentRefs')
        add_checksum(external_document_refs_element, 'checksum', externalDocumentRef.check_sum)
        add_not_empty(external_document_refs_element, 'spdxDocument', externalDocumentRef.spdx_document_uri)
        add_not_empty(external_document_refs_element, 'externalDocumentId', externalDocumentRef.external_document_id)
    # documentNamespace
    add_not_empty(doc_element, 'documentNamespace', document.namespace)
    # annotations
    for annotation in document.annotations:
        annotations_element = ET.SubElement(doc_element, 'annotations')
        add_not_empty(annotations_element, 'comment', annotation.comment)
        add_not_empty(annotations_element, 'annotationType', annotation.annotation_type)
        add_not_empty(annotations_element, 'SPDXID', annotation.spdx_id)
        add_not_empty(annotations_element, 'annotationDate', annotation.annotation_date_iso_format)
        add_not_empty(annotations_element, 'annotator', annotation.annotator)  # might not work.
    # dataLicense
    add_not_empty(doc_element, 'dataLicense', document.data_license.identifier)
    # reviewers
    for review in document.reviews:
        reviewers_element = ET.SubElement(doc_element, 'reviewers')
        add_not_empty(reviewers_element, 'comment', review.comment)
        add_not_empty(reviewers_element, 'reviewer', review.reviewer)  # might not work
        add_not_empty(reviewers_element, 'reviewDate', review.review_date_iso_format)
    # hasExtractedLicensingInfos
    for extractedLicense in document.extracted_licenses:
        extracted_licensing_infos_element = ET.SubElement(doc_element, 'hasExtractedLicensingInfos')
        add_not_empty(extracted_licensing_infos_element, 'extractedText', extractedLicense.text)
        add_not_empty(extracted_licensing_infos_element, 'comment', extractedLicense.comment)
        add_not_empty(extracted_licensing_infos_element, 'licenseId', extractedLicense.identifier)
        add_not_empty(extracted_licensing_infos_element, 'name', extractedLicense.full_name)
        for see_also in extractedLicense.cross_ref:
            add_not_empty(extracted_licensing_infos_element, 'seeAlso', see_also)
    # spdxVersion
    add_not_empty(doc_element, 'spdxVersion', str(document.version))
    # SPDXID
    add_not_empty(doc_element, 'SPDXID', document.spdx_id)
    # snippets
    for snippet in document.snippet:
        snippets_element = ET.SubElement(doc_element, 'snippets')
        add_not_empty(snippets_element, 'comment', snippet.comment)
        add_not_empty(snippets_element, 'name', snippet.name)
        add_not_empty(snippets_element, 'copyrightText', snippet.copyright)
        add_not_empty(snippets_element, 'licenseConcluded', snippet.conc_lics)  # might not work
        for license_in_snippet in snippet.licenses_in_snippet:
            add_not_empty(snippets_element, 'licenseInfoFromSnippet', license_in_snippet)  # probably wont work
        add_not_empty(snippets_element, 'licenseComments', snippet.license_comment)
        add_not_empty(snippets_element, 'SPDXID', snippet.spdx_id)
        add_not_empty(snippets_element, 'fileId', snippet.snip_from_file_spdxid)
    # relationships
    for relationship in document.relationships:
        relationships_element = ET.SubElement(doc_element, 'relationships')
        add_not_empty(relationships_element, 'spdxElementId', relationship.spdxelementid)
        add_not_empty(relationships_element, 'relatedSpdxElement', relationship.relatedspdxelement)
        add_not_empty(relationships_element, 'relationshipType', relationship.relationshiptype)

    if hasattr(ET, 'indent'):
        ET.indent(spdx_doc_element)

    xml_text = ET.tostring(spdx_doc_element)

    out.write(xml_text.decode())
