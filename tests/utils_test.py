
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


from collections import OrderedDict
import io
import json
import ntpath
import os
import posixpath
import re

import xmltodict
import yaml

import spdx
from spdx import utils


test_data_dir = os.path.join(os.path.dirname(__file__), 'data')


def get_test_loc(test_path, test_data_dir=test_data_dir, debug=False, exists=True):
    """
    Given a `test_path` relative to the `test_data_dir` directory, return the
    location to a test file or directory for this path. No copy is done.
    """
    if debug:
        import inspect
        caller = inspect.stack()[1][3]
        print('\nget_test_loc,%(caller)s,"%(test_path)s","%(test_data_dir)s"' % locals())

    assert test_path
    assert test_data_dir

    if not os.path.exists(test_data_dir):
        raise IOError("[Errno 2] No such directory: test_data_dir not found:"
                      " '%(test_data_dir)s'" % locals())

    tpath = to_os_native_path(test_path)
    test_loc = os.path.abspath(os.path.join(test_data_dir, tpath))

    if exists and not os.path.exists(test_loc):
        raise IOError("[Errno 2] No such file or directory: "
                      "test_path not found: '%(test_loc)s'" % locals())

    return test_loc


def to_os_native_path(path):
    """
    Normalize a path to use the native OS path separator.
    """
    path = path.replace(posixpath.sep, os.path.sep)
    path = path.replace(ntpath.sep, os.path.sep)
    path = path.rstrip(os.path.sep)
    return path


def strip_variable_text(rdf_text):
    """
    Return rdf_text stripped from variable parts such as rdf nodeids
    """

    replace_nid = re.compile('rdf:nodeID="[^\"]*"').sub
    rdf_text = replace_nid('', rdf_text)

    replace_creation = re.compile('<ns1:creationInfo>.*</ns1:creationInfo>', re.DOTALL).sub
    rdf_text = replace_creation('', rdf_text)

    replace_pcc = re.compile('<ns1:packageVerificationCode>.*</ns1:packageVerificationCode>', re.DOTALL).sub
    rdf_text = replace_pcc('', rdf_text)
    return rdf_text


def load_and_clean_rdf(location):
    """
    Return plain Python nested data for the SPDX RDF file at location suitable
    for comparison. The file content is cleaned from variable parts such as
    dates, generated UUIDs and versions

    NOTE: we use plain dicts to avoid ordering issues in XML. the SPDX tool and
    lxml do not seem to return a consistent ordering that is needed for tests.
    """
    with io.open(location, encoding='utf-8') as l:
        content = l.read()
    content = strip_variable_text(content)
    data = xmltodict.parse(content, dict_constructor=dict)
    return sort_nested(data)


def sort_nested(data):
    """
    Return a new dict with any nested list sorted recursively.
    """
    if isinstance(data, dict):
        new_data = {}
        for k, v in data.items():
            if isinstance(v, list):
                v = sorted(v)
            if isinstance(v, dict):
                v = sort_nested(v)
            new_data[k] = v
        return new_data
    elif isinstance(data, list):
        new_data = []
        for v in sorted(data):
            if isinstance(v, list):
                v = sort_nested(v)
            if isinstance(v, dict):
                v = sort_nested(v)
            new_data.append(v)
        return new_data


def check_rdf_scan(expected_file, result_file, regen=False):
    """
    Check that expected and result_file are equal.
    Both are paths to SPDX RDF XML files, UTF-8 encoded.
    """
    result = load_and_clean_rdf(result_file)
    if regen:
        expected = result
        with io.open(expected_file, 'w', encoding='utf-8') as o:
            json.dump(expected, o, indent=2)
    else:
        with io.open(expected_file, 'r', encoding='utf-8') as i:
            expected = sort_nested(json.load(i))
    assert expected == result


def load_and_clean_tv(location):
    """
    Return a mapping for the SPDX TV file at location suitable for comparison.
    The file content is cleaned from variable parts such as dates, generated
    UUIDs and versions
    """
    with io.open(location, encoding='utf-8') as l:
        content = l.read()
    content = [l for l in content.splitlines(False)
        if l and l.strip() and not l.startswith(('Creator: ', 'Created: ',))]
    return '\n'.join(content)


def check_tv_scan(expected_file, result_file, regen=False):
    """
    Check that expected and result_file are equal.
    Both are paths to plain SPDX tv text files, UTF-8 encoded.
    """
    result = load_and_clean_tv(result_file)
    if regen:
        with io.open(expected_file, 'w') as o:
            o.write(result)

    expected = load_and_clean_tv(expected_file)
    assert expected == result


def load_and_clean_json(location):
    """
    Return plain Python nested data for the SPDX JSON file at location suitable
    for comparison. The file content is cleaned from variable parts such as
    dates, generated UUIDs and versions
    """
    with io.open(location, encoding='utf-8') as l:
        content = l.read()
    data = json.loads(content)

    if 'creationInfo' in data['Document']:
        del(data['Document']['creationInfo'])

    return sort_nested(data)


def check_json_scan(expected_file, result_file, regen=False):
    """
    Check that expected_file and result_file are equal.
    Both are paths to SPDX JSON files, UTF-8 encoded.
    """
    result = load_and_clean_json(result_file)
    if regen:
        with io.open(expected_file, 'w', encoding='utf-8') as o:
            o.write(result)

    expected = load_and_clean_json(expected_file)
    assert expected == result


def load_and_clean_yaml(location):
    """
    Return plain Python nested data for the SPDX YAML file at location suitable
    for comparison. The file content is cleaned from variable parts such as
    dates, generated UUIDs and versions
    """
    with io.open(location, encoding='utf-8') as l:
        content = l.read()
    data = yaml.safe_load(content)

    if 'creationInfo' in data['Document']:
        del(data['Document']['creationInfo'])

    return sort_nested(data)


def check_yaml_scan(expected_file, result_file, regen=False):
    """
    Check that expected_file and result_file are equal.
    Both are paths to SPDX YAML files, UTF-8 encoded.
    """
    result = load_and_clean_yaml(result_file)
    if regen:
        with io.open(expected_file, 'w', encoding='utf-8') as o:
            o.write(result)

    expected = load_and_clean_yaml(expected_file)
    assert expected == result


def load_and_clean_xml(location):
    """
    Return plain Python nested data for the SPDX XML file at location suitable
    for comparison. The file content is cleaned from variable parts such as
    dates, generated UUIDs and versions
    """
    with io.open(location, encoding='utf-8') as l:
        content = l.read()
    data = xmltodict.parse(content, encoding='utf-8')

    if 'creationInfo' in data['SpdxDocument']['Document']:
        del(data['SpdxDocument']['Document']['creationInfo'])

    return sort_nested(data)


def check_xml_scan(expected_file, result_file, regen=False):
    """
    Check that expected_file and result_file are equal.
    Both are paths to SPDX XML files, UTF-8 encoded.
    """
    result = load_and_clean_xml(result_file)
    if regen:
        with io.open(expected_file, 'w', encoding='utf-8') as o:
            o.write(result)

    expected = load_and_clean_xml(expected_file)
    assert expected == result


class TestParserUtils(object):
    """
    Helper class to represent SPDX Document models as Python types after parsing
    to be compared to expected data from a JSON file.
    """

    @classmethod
    def license_to_dict(cls, license):
        """
        Represents spdx.document.License, spdx.document.LicenseConjunction or
        spdx.document.LicenseDisjunction as a Python dictionary
        """
        CONJ_SEP = re.compile(' AND | and ')
        DISJ_SEP = re.compile(' OR | or ')
        if license is None:
            return None
        license_dict = OrderedDict()

        if isinstance(license, spdx.document.LicenseConjunction):
            license_dict['type'] = 'Conjunction'
            sep_regex = CONJ_SEP
        elif isinstance(license, spdx.document.LicenseDisjunction):
            license_dict['type'] = 'Disjunction'
            sep_regex = DISJ_SEP
        else:
            license_dict['type'] = 'Single'
            license_dict['identifier'] = license.identifier
            license_dict['name'] = license.full_name
            return license_dict

        license_dict['identifier'] = sorted(sep_regex.split(license.identifier))
        license_dict['name'] = sorted(sep_regex.split(license.full_name))

        return license_dict

    @classmethod
    def version_to_dict(cls, version):
        """
        Represents spdx.version.Version as a Python dictionary
        """
        return OrderedDict([
            ('major', int(version.major)),
            ('minor', int(version.minor))
        ])

    @classmethod
    def entity_to_dict(cls, entity):
        """
        Represents spdx.creationInfo.Creator subclasses as a dictionary
        """
        if entity is None:
            return None
        entity_dict = OrderedDict(name=entity.name)

        if isinstance(entity, spdx.creationinfo.Tool):
            entity_dict['type'] = 'Tool'
            return entity_dict

        entity_dict['email'] = entity.email
        entity_dict['type'] = 'Person'

        if isinstance(entity, spdx.creationinfo.Organization):
            entity_dict['type'] = 'Organization'
            return entity_dict

        return entity_dict

    @classmethod
    def checksum_to_dict(cls, checksum):
        """
        Represents spdx.checksum.Algorithm as a Python dictionary
        """
        if checksum is None:
            return None
        return OrderedDict([
            ('identifier', checksum.identifier),
            ('value', checksum.value)])

    @classmethod
    def package_to_dict(cls, package):
        """
        Represents spdx.package.Package as a Python dictionary
        """
        lics_from_files = []
        if package.are_files_analyzed:
            lics_from_files = sorted(package.licenses_from_files, key=lambda lic: lic.identifier)
        return OrderedDict([
            ('id', package.spdx_id),
            ('name', package.name),
            ('packageFileName', package.file_name),
            ('summary', package.summary),
            ('description', package.description),
            ('versionInfo', package.version),
            ('sourceInfo', package.source_info),
            ('downloadLocation', package.download_location),
            ('homepage', package.homepage),
            ('originator', cls.entity_to_dict(package.originator)),
            ('supplier', cls.entity_to_dict(package.supplier)),
            ('licenseConcluded', cls.license_to_dict(package.conc_lics)),
            ('licenseDeclared', cls.license_to_dict(package.license_declared)),
            ('copyrightText', package.cr_text),
            ('licenseComment', package.license_comment),
            ('checksum', cls.checksum_to_dict(package.check_sum)),
            ('files', cls.files_to_list(sorted(package.files))),
            ('licenseInfoFromFiles', [cls.license_to_dict(lic) for lic in lics_from_files]),
            ('verificationCode', OrderedDict([
                ('value', package.verif_code),
                ('excludedFilesNames', sorted(package.verif_exc_files))])
            )
        ])

    @classmethod
    def files_to_list(cls, files):
        """
        Represents a list of spdx.file.File as a Python list of dictionaries
        """
        files_list = []

        for file in files:
            lics_from_files = sorted(file.licenses_in_file, key=lambda lic: lic.identifier)
            contributors = sorted(file.contributors, key=lambda c: c.name)
            file_dict = OrderedDict([
                ('id', file.spdx_id),
                ('name', file.name),
                ('type', file.type),
                ('comment', file.comment),
                ('licenseConcluded', cls.license_to_dict(file.conc_lics)),
                ('copyrightText', file.copyright),
                ('licenseComment', file.license_comment),
                ('notice', file.notice),
                ('checksum', cls.checksum_to_dict(file.chk_sum)),
                ('licenseInfoFromFiles', [cls.license_to_dict(lic) for lic in lics_from_files]),
                ('contributors', [cls.entity_to_dict(contributor) for contributor in contributors]),
                ('dependencies', sorted(file.dependencies)),
                ('artifactOfProjectName', file.artifact_of_project_name),
                ('artifactOfProjectHome', file.artifact_of_project_home),
                ('artifactOfProjectURI', file.artifact_of_project_uri),
            ])
            files_list.append(file_dict)

        return files_list

    @classmethod
    def ext_document_references_to_list(cls, ext_doc_refs):
        """
        Represents a list of spdx.document.ExternalDocumentRef as a Python list of dictionaries
        """
        ext_doc_refs_list = []

        for ext_doc_ref in ext_doc_refs:
            ext_doc_ref_dict = OrderedDict([
                ('externalDocumentId', ext_doc_ref.external_document_id),
                ('spdxDocument', ext_doc_ref.spdx_document_uri),
                ('checksum', cls.checksum_to_dict(ext_doc_ref.check_sum)),
            ])
            ext_doc_refs_list.append(ext_doc_ref_dict)

        return ext_doc_refs_list

    @classmethod
    def extracted_licenses_to_list(cls, extracted_licenses):
        """
        Represents a list of spdx.document.ExtractedLicense as a Python list of dictionaries
        """
        extracted_licenses_list = []

        for extracted_license in extracted_licenses:
            extracted_license_dict = OrderedDict([
                ('name', extracted_license.full_name),
                ('identifier', extracted_license.identifier),
                ('text', extracted_license.text),
                ('comment', extracted_license.comment),
                ('cross_refs', sorted(extracted_license.cross_ref)),
            ])
            if extracted_license_dict not in extracted_licenses_list:
                extracted_licenses_list.append(extracted_license_dict)

        return extracted_licenses_list

    @classmethod
    def annotations_to_list(cls, annotations):
        """
        Represents a list of spdx.annotation.Annotation as a Python list of dictionaries
        """
        annotations_list = []

        for annotation in annotations:
            annotation_dict = OrderedDict([
                ('id', annotation.spdx_id),
                ('comment', annotation.comment),
                ('type', annotation.annotation_type),
                ('annotator', cls.entity_to_dict(annotation.annotator)),
                ('date', utils.datetime_iso_format(annotation.annotation_date)),
            ])
            annotations_list.append(annotation_dict)

        return annotations_list

    @classmethod
    def reviews_to_list(cls, reviews):
        """
        Represents a list of spdx.review.Review as a Python list of dictionaries
        """
        reviews_list = []

        for review in reviews:
            review_dict = OrderedDict([
                ('comment', review.comment),
                ('reviewer', cls.entity_to_dict(review.reviewer)),
                ('date', utils.datetime_iso_format(review.review_date))
             ])
            reviews_list.append(review_dict)

        return reviews_list

    @classmethod
    def snippets_to_list(cls, snippets):
        """
        Represents a list of spdx.snippet.Snippet as a Python list of dictionaries
        """
        snippets_list = []

        for snippet in snippets:
            lics_from_snippet = sorted(snippet.licenses_in_snippet, key=lambda lic: lic.identifier)
            snippet_dict = OrderedDict([
                ('id', snippet.spdx_id),
                ('name', snippet.name),
                ('comment', snippet.comment),
                ('copyrightText', snippet.copyright),
                ('licenseComments', snippet.license_comment),
                ('fileId', snippet.snip_from_file_spdxid),
                ('licenseConcluded', cls.license_to_dict(snippet.conc_lics)),
                ('licenseInfoFromSnippet', [cls.license_to_dict(lic) for lic in lics_from_snippet]),
            ])
            snippets_list.append(snippet_dict)

        return snippets_list

    @classmethod
    def to_dict(cls, doc):
        """
        Represents a SPDX Document (spdx.document.Document) as nested Python types
        """
        creators = sorted(doc.creation_info.creators, key=lambda c: c.name)
        return OrderedDict([
            ('id', doc.spdx_id),
            ('specVersion', cls.version_to_dict(doc.version)),
            ('documentNamespace', doc.namespace),
            ('name', doc.name),
            ('comment', doc.comment),
            ('dataLicense', cls.license_to_dict(doc.data_license)),
            ('licenseListVersion', cls.version_to_dict(doc.creation_info.license_list_version)),
            ('creators', [cls.entity_to_dict(creator) for creator in creators]),
            ('created', utils.datetime_iso_format(doc.creation_info.created)),
            ('creatorComment', doc.creation_info.comment),
            ('files', cls.files_to_list(doc.unpackaged_files)),
            ('packages', [cls.package_to_dict(p) for p in doc.packages]),
            ('externalDocumentRefs', cls.ext_document_references_to_list(sorted(doc.ext_document_references))),
            ('extractedLicenses', cls.extracted_licenses_to_list(sorted(doc.extracted_licenses))),
            ('annotations', cls.annotations_to_list(sorted(doc.annotations))),
            ('reviews', cls.reviews_to_list(sorted(doc.reviews))),
            ('snippets', cls.snippets_to_list(sorted(doc.snippet))),
        ])
