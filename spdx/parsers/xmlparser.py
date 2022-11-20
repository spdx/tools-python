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

import xml.etree.ElementTree as ET

from spdx.checksum import CHECKSUM_ALGORITHM_FROM_XML_DICT
from spdx.document import Document
from spdx.parsers import jsonyamlxml

ANNOTATION_KEYS = ['SPDXID', 'annotationDate', 'annotationType', 'annotator', 'comment']
EXT_LIC_KEYS = ['comment', 'licenseId', 'extractedText', 'name', 'seeAlsos']
EXT_REF_KEYS = ['checksum', 'externalDocumentId', 'spdxDocument']
FILE_KEYS = ['artifactOf', 'annotations',
             'checksums', 'comment', 'copyrightText',
             'fileContributors', 'fileName', 'fileTypes',
             'licenseComments', 'licenseConcluded', 'licenseInfoInFiles',
             'noticeText',
             'SPDXID',]
PACKAGE_KEYS = ['SPDXID', 'annotations', 'attributionTexts', 'builtDate', 'checksums', 'copyrightText',
                'description', 'downloadLocation', 'externalRefs', 'filesAnalyzed', 'hasFiles', 'homepage',
                'licenseComments', 'licenseConcluded', 'licenseDeclared', 'licenseInfoFromFiles', 'name',
                'originator', 'packageFileName', 'packageVerificationCode', 'primaryPackagePurpose',
                'releaseDate', 'sourceInfo', 'summary', 'supplier', 'validUntilDate', 'versionInfo']
PKG_EXT_REF_KEYS = ['referenceCategory', 'referenceLocator', 'referenceType', 'comment']
RELATIONSHIP_KEYS = ['comment', 'spdxElementId', 'relationshipType', 'relatedSpdxElement']
REVIEW_KEYS = ['comment', 'reviewDate', 'reviewer']
SNIPPET_KEYS = ['SPDXID', 'attributionTexts', 'comment', 'copyrightText',
                'licenseComments', 'licenseConcluded', 'licenseInfoInSnippets',
                'name', 'ranges', 'snippetFromFile']


class Parser(jsonyamlxml.Parser):
    """
    Wrapper class for jsonyamlxml.Parser to provide an interface similar to
    RDF and TV Parser classes (i.e., spdx.parsers.<format name>.Parser) for XML parser.
    It also avoids to repeat jsonyamlxml.Parser.parse code for JSON, YAML and XML parsers
    """

    def __init__(self, builder, logger):
        super(Parser, self).__init__(builder, logger)
        self.document = None
        self.error = False

    def checksum_node_to_dict(self, checksum_node):
        checksum_dict = {}
        for child in checksum_node:
            if child.tag == 'algorithm':
                algo = child.text
                if algo.startswith('checksumAlgorithm_'):
                    algo = CHECKSUM_ALGORITHM_FROM_XML_DICT.get(algo)
                checksum_dict['algorithm'] = algo
            elif child.tag == 'checksumValue':
                checksum_dict['checksumValue'] = child.text
            else:
                self.logger.log('unknown tag "{}"'.format(child.tag))
                self.error = True
        return checksum_dict

    @staticmethod
    def annotations_node_to_dict(annotations_node):
        annotation_dict = {}
        for child in annotations_node:
            if child.tag in ANNOTATION_KEYS:
                annotation_dict[child.tag] = child.text
        return annotation_dict

    @staticmethod
    def external_document_ref_node_to_dict(node):
        ext_doc_ref = {}
        for child in node:
            if child.tag in PKG_EXT_REF_KEYS:
                ext_doc_ref[child.tag] = child.text
            else:
                raise RuntimeError(f'external_document_ref_node key error: {child.tag}')
        return ext_doc_ref

    def parse_doc_annotations(self, annotations_node):
        super().parse_doc_annotations(self.annotations_node_to_dict(annotations_node))

    def parse_package_annotations(self, annotations_node):
        super().parse_pkg_annotations(self.annotations_node_to_dict(annotations_node))

    def parse_creation_info(self, creation_node):
        creation_info = {}
        for child in creation_node:
            if child.tag == 'comment':
                creation_info['comment'] = child.text
                self.parse_creation_info_comment(child.text)
            elif child.tag == 'created':
                self.parse_creation_info_created(child.text)
            elif child.tag == 'creators':
                entity = self.builder.create_entity(self.document, child.text)
                self.builder.add_creator(self.document, entity)
            elif child.tag == 'licenseListVersion':
                self.parse_creation_info_lic_list_version(child.text)
            else:
                self.logger.log('unhandled creation_info child tag "{}"'.format(child.tag))
                self.error = True

    def parse_external_document_refs(self, ext_doc_refs_node):
        ext_doc_refs = {}
        for child in ext_doc_refs_node:
            if child.tag in EXT_REF_KEYS:
                if child.tag == 'checksum':
                    ext_doc_refs[child.tag] = self.checksum_node_to_dict(child)
                else:
                    ext_doc_refs[child.tag] = child.text
            else:
                self.logger.log('unhandled external_document_refs child tag "{}"'.format(child.tag))
                self.error = True
        super().parse_external_document_refs([ext_doc_refs])

    def parse_extracted_license_info(self, eli_node):
        extracted_license_info = {}
        for child in eli_node:
            if child.tag in EXT_LIC_KEYS:
                if child.tag == 'seeAlsos':
                    see_list = extracted_license_info.get(child.tag) or []
                    see_list.append(child.text)
                    if len(see_list) > 0:
                        extracted_license_info[child.tag] = see_list
                else:
                    extracted_license_info[child.tag] = child.text
            else:
                self.logger.log('unhandled extracted_license_info child tag "{}"'.format(child.tag))
                self.error = True
        super().parse_extracted_license_info([extracted_license_info])

    def parse_file(self, file_node):
        this_file = {}
        for child in file_node:
            if child.tag in FILE_KEYS:
                if child.tag == 'annotations':
                    annotations_list = this_file.get(child.tag, [])
                    annotations_list.append(self.annotations_node_to_dict(child))
                    this_file[child.tag] = annotations_list
                elif child.tag == 'artifactOf':
                    artifact_list = this_file.get('artifactOf') or []
                    artifact_dict = {}
                    for art_child in child:
                        if art_child.tag in ['homePage', 'name', 'projectUri']:
                            artifact_dict[art_child.tag] = art_child.text
                    artifact_list.append(artifact_dict)
                    this_file['artifactOf'] = artifact_list
                elif child.tag == 'checksums':
                    checksums = this_file.get('checksums', [])
                    checksums.append(self.checksum_node_to_dict(child))
                    this_file['checksums'] = checksums
                elif child.tag == 'fileContributors':
                    fc_list = this_file.get(child.tag, [])
                    fc_list.append(child.text)
                    this_file[child.tag] = fc_list
                elif child.tag == 'fileTypes':
                    file_types = this_file.get(child.tag, [])
                    file_type = child.text
                    if file_type.startswith('fileType_'):
                        file_type = file_type[9:].upper()
                    file_types.append(file_type)
                    this_file[child.tag] = file_types
                elif child.tag == 'licenseInfoInFiles':
                    liff_list = this_file.get(child.tag, [])
                    liff_list.append(child.text)
                    this_file[child.tag] = liff_list
                else:
                    this_file[child.tag] = child.text
            else:
                self.logger.log('unhandled file child tag "{}"'.format(child.tag))
                self.error = True
        super().parse_file(this_file)

    def parse_package(self, package_node):
        package = {}
        for child in package_node:
            if child.tag in PACKAGE_KEYS:
                if child.tag == 'annotations':
                    annotations_list = package.get(child.tag, [])
                    annotations_list.append(self.annotations_node_to_dict(child))
                    package[child.tag] = annotations_list
                elif child.tag == 'checksums':
                    checksums = package.get('checksums') or []
                    _checksum = self.checksum_node_to_dict(child)
                    checksums.append(_checksum)
                    package['checksums'] = checksums
                elif child.tag == 'externalRefs':
                    external_refs = package.get('externalRefs', [])
                    external_refs.append(self.external_document_ref_node_to_dict(child))
                    package['externalRefs'] = external_refs
                elif child.tag == 'hasFiles':
                    files = package.get('hasFiles', [])
                    files.append(child.text)
                    package['hasFiles'] = files
                elif child.tag == 'licenseInfoFromFiles':
                    liff_list = package.get(child.tag, [])
                    liff_list.append(child.text)
                    package[child.tag] = liff_list
                elif child.tag == 'filesAnalyzed':
                    package['filesAnalyzed'] = child.text.lower() == 'true'
                elif child.tag == 'packageVerificationCode':
                    pkg_verf_code_dict = {}
                    for pkg_child in child:
                        if pkg_child.tag == 'packageVerificationCodeValue':
                            pkg_verf_code_dict['packageVerificationCodeValue'] = pkg_child.text
                        elif pkg_child.tag == 'packageVerificationCodeExcludedFiles':
                            pvcef_list = pkg_verf_code_dict.get(pkg_child.tag, [])
                            pvcef_list.append(pkg_child.text)
                            pkg_verf_code_dict[pkg_child.tag] = pvcef_list
                    package[child.tag] = pkg_verf_code_dict
                elif child.tag == 'primaryPackagePurpose':
                    ppp_list = package.get(child.tag, [])
                    ppp_type = child.text
                    if ppp_type.startswith('packagePurpose_'):
                        ppp_type = ppp_type[15:].upper()
                    ppp_list.append(ppp_type)
                    package[child.tag] = ppp_list
                else:
                    package[child.tag] = child.text
            else:
                self.logger.log('unhandled package child tag "{}"'.format(child.tag))
                self.error = True
        super().parse_package(package)

    def parse_relationships(self, relationships_node):
        relationship = {}
        for child in relationships_node:
            if child.tag in RELATIONSHIP_KEYS:
                relationship[child.tag] = child.text
            else:
                self.logger.log('unhandled relationships child tag "{}"'.format(child.tag))
                self.error = True
        super().parse_relationships([relationship])

    def parse_reviews(self, reviews_node):
        review = {}
        for child in reviews_node:
            if child.tag in REVIEW_KEYS:
                review[child.tag] = child.text
            else:
                self.logger.log('unhandled reviews child tag "{}"'.format(child.tag))
                self.error = True
        return review

    @staticmethod
    def snippet_range_to_dict(range_child):
        # TODO parse out this data in a dict that will look like what came from json
        snippet_range = {}
        for rchild in range_child:
            if rchild.tag == 'startPointer':
                start_pointer = {}
                for start_child in rchild:
                    if start_child.tag in ['offset', 'lineNumber']:
                        start_pointer[start_child.tag] = int(start_child.text)
                    else:
                        start_pointer[start_child.tag] = start_child.text
                snippet_range[rchild.tag] = start_pointer
            elif rchild.tag == 'endPointer':
                end_pointer = {}
                for end_child in rchild:
                    if end_child.tag in ['offset', 'lineNumber']:
                        end_pointer[end_child.tag] = int(end_child.text)
                    else:
                        end_pointer[end_child.tag] = end_child.text
                snippet_range[rchild.tag] = end_pointer
        return snippet_range

    def parse_snippets(self, snippet_node):
        snippet = {}
        for child in snippet_node:
            if child.tag in SNIPPET_KEYS:
                if child.tag == 'licenseInfoInSnippets':
                    lics_list = snippet.get(child.tag) or []
                    lics_list.append(child.text)
                    snippet[child.tag] = lics_list
                elif child.tag == 'ranges':
                    ranges = snippet.get(child.tag, [])
                    ranges.append(self.snippet_range_to_dict(child))
                    snippet[child.tag] = ranges
                else:
                    snippet[child.tag] = child.text
            else:
                self.logger.log('unhandled snippets child tag "{}"'.format(child.tag))
                self.error = True
        return snippet

    def parse_document(self, doc_node):
        self.document = Document()
        reviews = []
        snippets = []
        for child in doc_node:
            if child.tag == 'SPDXID':
                self.parse_doc_id(child.text)
            elif child.tag == 'annotations':
                self.parse_doc_annotations(child)
            elif child.tag == 'comment':
                self.parse_doc_comment(child.text)
            elif child.tag == 'creationInfo':
                self.parse_creation_info(child)
            elif child.tag == 'dataLicense':
                self.parse_doc_data_license(child.text)
            elif child.tag == 'documentDescribes':
                self.parse_doc_described_objects(child.text)
            elif child.tag == 'documentNamespace':
                self.parse_doc_namespace(child.text)
            elif child.tag == 'externalDocumentRefs':
                self.parse_external_document_refs(child)
            elif child.tag == 'files':
                self.parse_file(child)
            elif child.tag == 'hasExtractedLicensingInfos':
                self.parse_extracted_license_info(child)
            elif child.tag == 'name':
                self.parse_doc_name(child.text)
            elif child.tag == 'packages':
                self.parse_package(child)
            elif child.tag == 'relationships':
                self.parse_relationships(child)
            elif child.tag == 'reviewers':
                review = self.parse_reviews(child)
                if review is not None:
                    reviews.append(review)
            elif child.tag == 'snippets':
                snippet = self.parse_snippets(child)
                if snippet is not None:
                    snippets.append(snippet)
            elif child.tag == 'spdxVersion':
                self.parse_doc_version(child.text)
            else:
                self.logger.log('unhandled document child tag "{}"'.format(child.tag))
                self.error = True
        if len(reviews) > 0:
            super().parse_reviews(reviews)
        if len(snippets) > 0:
            super().parse_snippets(snippets)

    def parse(self, file):
        self.error = True
        tree = ET.ElementTree(file=file)
        root = tree.getroot()
        if root.tag == 'Document':
            self.error = False
            self.parse_document(root)
        return self.document, self.error
