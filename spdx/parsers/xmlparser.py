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

from spdx.document import Document
from spdx.file import FileType, FILE_TYPE_FROM_XML_DICT
from spdx.parsers import jsonyamlxml

ANNOTATION_KEYS = ['SPDXID', 'annotationDate', 'annotationType', 'annotator', 'comment']
EXT_LIC_KEYS = ['comment', 'licenseId', 'extractedText', 'name', 'seeAlso']
EXT_REF_KEYS = ['checksum', 'externalDocumentId', 'spdxDocument']
FILE_KEYS = ['SPDXID', 'artifactOf', 'checksum', 'comment', 'copyrightText', 'fileType',
             'licenseComments', 'licenseConcluded', 'licenseInfoFromFiles',
             'name', 'sha1']
PACKAGE_KEYS = ['SPDXID', 'annotations', 'attributionTexts', 'checksum', 'copyrightText', 'description',
                'downloadLocation', 'File', 'filesAnalyzed', 'homepage', 'licenseComments',
                'licenseConcluded', 'licenseDeclared', 'licenseInfoFromFiles', 'name', 'originator',
                'packageFileName', 'packageVerificationCode', 'sha1', 'sourceInfo', 'summary',
                'supplier', 'versionInfo']
RELATIONSHIP_KEYS = ['comment', 'spdxElementId', 'relationshipType', 'relatedSpdxElement']
REVIEW_KEYS = ['comment', 'reviewDate', 'reviewer']
SNIPPET_KEYS = ['SPDXID', 'attributionTexts', 'comment', 'copyrightText', 'fileId',
                'name', 'licenseComments', 'licenseConcluded', 'licenseInfoFromSnippet']


class Parser(jsonyamlxml.Parser):
    """
    Wrapper class for xml.Parser to provide an interface similar to
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
                    algo = algo[18:].upper()
                checksum_dict['algorithm'] = algo
            elif child.tag == 'checksumValue':
                checksum_dict['checksumValue'] = child.text
            else:
                self.logger.log('unknown tag "{}"'.format(child.tag))
                self.error = True
        return checksum_dict

    def parse_doc_annotations(self, annotations_node):
        annotations = {}
        for child in annotations_node:
            if child.tag in ANNOTATION_KEYS:
                annotations[child.tag] = child.text
            else:
                self.logger.log('unhandled child tag "{}"'.format(child.tag))
                self.error = True
        super(__class__, self).parse_annotations([annotations])

    def parse_creation_info(self, creation_node):
        for child in creation_node:
            if child.tag == 'comment':
                self.parse_creation_info_comment(child.text)
            elif child.tag == 'created':
                self.parse_creation_info_created(child.text)
            elif child.tag == 'creators':
                entity = self.builder.create_entity(self.document, child.text)
                self.builder.add_creator(self.document, entity)
            elif child.tag == 'licenseListVersion':
                self.parse_creation_info_lic_list_version(child.text)
            else:
                self.logger.log('unhandled child tag "{}"'.format(child.tag))
                self.error = True

    def parse_doc_described_objects(self, doc_describes_node):
        for child in doc_describes_node:
            if child.tag == 'Package':
                self.parse_package(child)
            else:
                self.logger.log('unhandled child tag "{}"'.format(child.tag))
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
                self.logger.log('unhandled child tag "{}"'.format(child.tag))
                self.error = True
        super(__class__, self).parse_external_document_refs([ext_doc_refs])

    def parse_extracted_license_info(self, eli_node):
        extracted_license_info = {}
        for child in eli_node:
            if child.tag in EXT_LIC_KEYS:
                if child.tag == 'seeAlso':
                    see_list = extracted_license_info.get('seeAlso') or []
                    see_list.append(child.text)
                    extracted_license_info['seeAlso'] = see_list
                else:
                    extracted_license_info[child.tag] = child.text
            else:
                self.logger.log('unhandled child tag "{}"'.format(child.tag))
                self.error = True
        super().parse_extracted_license_info([extracted_license_info])

    def parse_file(self, file_node):
        this_file = {}
        for child in file_node:
            if child.tag in FILE_KEYS:
                if child.tag == 'artifactOf':
                    artifact_list = this_file.get('artifactOf') or []
                    artifact_dict = {}
                    for art_child in child:
                        if art_child.tag in ['homePage', 'name', 'projectUri']:
                            artifact_dict[art_child.tag] = art_child.text
                    artifact_list.append(artifact_dict)
                    this_file['artifactOf'] = artifact_list
                elif child.tag == 'checksum':
                    checksums = this_file.get('checksums') or []
                    checksums.append(self.checksum_node_to_dict(child))
                    this_file['checksums'] = checksums
                elif child.tag == 'fileType':
                    file_types = this_file.get('fileTypes') or []
                    file_type = child.text
                    if file_type.startswith('fileType_'):
                        file_type = file_type[9:].upper()
                    file_types.append(file_type)
                    this_file['fileTypes'] = file_types
                elif child.tag == 'licenseInfoFromFiles':
                    liff_list = this_file.get('licenseInfoFromFiles') or []
                    liff_list.append(child.text)
                    this_file['licenseInfoFromFiles'] = liff_list
                else:
                    this_file[child.tag] = child.text
            else:
                self.logger.log('unhandled child tag "{}"'.format(child.tag))
                self.error = True
        super().parse_file(this_file)

    def parse_package(self, package_node):
        package = {}
        file_nodes = []
        liff_nodes = []
        for child in package_node:
            if child.tag in PACKAGE_KEYS:
                if child.tag == 'checksum':
                    checksum = self.checksum_node_to_dict(child)
                    checksums = package.get('checksums') or []
                    checksums.append(checksum)
                    package['checksums'] = checksums
                elif child.tag == 'File':
                    file_nodes.append(child)
                    package['files'] = []  # will get later
                elif child.tag == 'licenseInfoFromFiles':
                    liff_nodes.append(child)
                    package[child.tag] = []  # will get later
                elif child.tag == 'packageVerificationCode':
                    pkg_verf_code_dict = {}
                    for pkg_child in child:
                        if pkg_child.tag == 'packageVerificationCodeValue':
                            pkg_verf_code_dict['packageVerificationCodeValue'] = pkg_child.text
                        elif pkg_child.tag == 'packageVerificationCodeExcludedFiles':
                            pvcef_list = pkg_verf_code_dict.get(pkg_child.tag) or []
                            pvcef_list.append(pkg_child.text)
                            pkg_verf_code_dict[pkg_child.tag] = pvcef_list
                    package[child.tag] = pkg_verf_code_dict
                else:
                    package[child.tag] = child.text
            else:
                self.logger.log('unhandled child tag "{}"'.format(child.tag))
                self.error = True
        super().parse_package(package)
        for file_node in file_nodes:
            self.parse_file(file_node)
        liff_list = []
        for liff_node in liff_nodes:
            liff_list.append(liff_node.text)
        self.parse_pkg_license_info_from_files(liff_list)

    def parse_relationships(self, relationships_node):
        relationship = {}
        for child in relationships_node:
            if child.tag in RELATIONSHIP_KEYS:
                relationship[child.tag] = child.text
            else:
                self.logger.log('unhandled child tag "{}"'.format(child.tag))
                self.error = True
        super().parse_relationships([relationship])

    def parse_reviews(self, reviews_node):
        review = {}
        for child in reviews_node:
            if child.tag in REVIEW_KEYS:
                review[child.tag] = child.text
            else:
                self.logger.log('unhandled child tag "{}"'.format(child.tag))
                self.error = True
        super().parse_reviews([review])

    def parse_snippets(self, snippet_node):
        snippet = {}
        for child in snippet_node:
            if child.tag in SNIPPET_KEYS:
                if child.tag == 'licenseInfoFromSnippet':
                    lics_list = snippet.get(child.tag) or []
                    lics_list.append(child.text)
                    snippet[child.tag] = lics_list
                else:
                    snippet[child.tag] = child.text
            else:
                self.logger.log('unhandled child tag "{}"'.format(child.tag))
                self.error = True
        super().parse_snippets([snippet])

    def parse_document(self, doc_node):
        self.document = Document()
        describes_nodes = []
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
                describes_nodes.append(child)
#                self.parse_doc_described_objects(child)
            elif child.tag == 'documentNamespace':
                self.parse_doc_namespace(child.text)
            elif child.tag == 'externalDocumentRefs':
                self.parse_external_document_refs(child)
            elif child.tag == 'hasExtractedLicensingInfos':
                self.parse_extracted_license_info(child)
            elif child.tag == 'name':
                self.parse_doc_name(child.text)
            elif child.tag == 'relationships':
                self.parse_relationships(child)
            elif child.tag == 'reviewers':
                self.parse_reviews(child)
            elif child.tag == 'snippets':
                self.parse_snippets(child)
            elif child.tag == 'spdxVersion':
                self.parse_doc_version(child.text)
            else:
                self.logger.log('unhandled child tag "{}"'.format(child.tag))
                self.error = True
        for describes_node in describes_nodes:
            self.parse_doc_described_objects(describes_node)

    def parse(self, file):
        self.error = True
        tree = ET.ElementTree(file=file)
        root = tree.getroot()
        for child in root:
            if child.tag == 'Document':
                self.error = False
                self.parse_document(child)
                break

        return self.document, self.error
