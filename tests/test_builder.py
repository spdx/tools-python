
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

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import unittest
from unittest import TestCase

import tests.testing_utils as testing_utils

from spdx.document import Document, License
import spdx.parsers.tagvaluebuilders as builders
from spdx.version import Version


class TestDocumentBuilder(unittest.case.TestCase):

    def setUp(self):
        self.document = Document()
        self.builder = builders.DocBuilder()

    def test_correct_version(self):
        version_str = 'SPDX-1.2'
        self.builder.set_doc_version(self.document, version_str)
        assert (self.document.version.major == 1 and
                self.document.version.minor == 2)

    @testing_utils.raises(builders.CardinalityError)
    def test_version_cardinality(self):
        version_str = 'SPDX-1.2'
        self.builder.set_doc_version(self.document, version_str)
        self.builder.set_doc_version(self.document, version_str)

    @testing_utils.raises(builders.SPDXValueError)
    def test_version_value(self):
        version_str = '1.2'
        self.builder.set_doc_version(self.document, version_str)

    @testing_utils.raises(builders.IncompatibleVersionError)
    def test_version_number(self):
        version_str = 'SPDX-2.0'
        self.builder.set_doc_version(self.document, version_str)

    def test_correct_data_lics(self):
        lics_str = 'CC0-1.0'
        self.builder.set_doc_data_lics(self.document, lics_str)
        assert self.document.data_license == License.from_identifier(lics_str)

    @testing_utils.raises(builders.SPDXValueError)
    def test_data_lics_value(self):
        lics_str = 'GPL'
        self.builder.set_doc_data_lics(self.document, lics_str)

    @testing_utils.raises(builders.CardinalityError)
    def test_data_lics_cardinality(self):
        lics_str = 'CC0-1.0'
        self.builder.set_doc_data_lics(self.document, lics_str)
        self.builder.set_doc_data_lics(self.document, lics_str)

    def test_correct_data_comment(self):
        comment_str = 'This is a comment.'
        comment_text = '<text>' + comment_str + '</text>'
        self.builder.set_doc_comment(self.document, comment_text)
        assert self.document.comment == comment_str

    @testing_utils.raises(builders.CardinalityError)
    def test_comment_cardinality(self):
        comment_str = 'This is a comment.'
        comment_text = '<text>' + comment_str + '</text>'
        self.builder.set_doc_comment(self.document, comment_text)
        self.builder.set_doc_comment(self.document, comment_text)

    @testing_utils.raises(builders.SPDXValueError)
    def test_comment_value(self):
        comment = '<text>slslss<text'
        self.builder.set_doc_comment(self.document, comment)


class TestEntityBuilder(TestCase):

    def setUp(self):
        self.builder = builders.EntityBuilder()
        self.document = Document()

    def test_tool(self):
        tool_name = 'autoanal-2.0'
        tool_str = 'Tool: ' + tool_name
        tool = self.builder.build_tool(self.document, tool_str)
        assert tool.name == tool_name

    @testing_utils.raises(builders.SPDXValueError)
    def test_tool_value_error(self):
        tool_str = 'tool: ll'
        self.builder.build_tool(self.document, tool_str)

    def test_org_with_email(self):
        org_name = 'Example'
        org_email = 'example@example.org'
        org_str = 'Organization: {0} ( {1} )'.format(org_name, org_email)
        org = self.builder.build_org(self.document, org_str)
        assert org.name == org_name
        assert org.email == org_email

    def test_org(self):
        org_name = 'Example'
        org_str = 'Organization: {0} ()'.format(org_name)
        org = self.builder.build_org(self.document, org_str)
        assert org.name == org_name
        assert org.email is None

    @testing_utils.raises(builders.SPDXValueError)
    def test_org_value_error(self):
        org_name = 'Example'
        org_str = 'Organization {0}'.format(org_name)
        self.builder.build_org(self.document, org_str)

    def test_person_with_email(self):
        per_name = 'Bob'
        per_email = 'bob@example.org'
        per_str = 'Person: {0} ( {1} )'.format(per_name, per_email)
        per = self.builder.build_person(self.document, per_str)
        assert per.name == per_name
        assert per.email == per_email

    def test_per(self):
        per_name = 'Bob'
        per_str = 'Person: {0} ()'.format(per_name)
        per = self.builder.build_person(self.document, per_str)
        assert per.name == per_name
        assert per.email is None

    @testing_utils.raises(builders.SPDXValueError)
    def test_per_value_error(self):
        per_name = 'Bob'
        per_str = 'Person {0}'.format(per_name)
        self.builder.build_person(self.document, per_str)


class TestCreationInfoBuilder(TestCase):

    def setUp(self):
        self.document = Document()
        self.builder = builders.CreationInfoBuilder()
        self.entity_builder = builders.EntityBuilder()

    def test_add_creator(self):
        per_str = 'Person: Bob (bob@example.com)'
        per = self.entity_builder.build_person(self.document, per_str)
        assert self.builder.add_creator(self.document, per)
        assert len(self.document.creation_info.creators) == 1
        assert self.document.creation_info.creators[0] == per

    @testing_utils.raises(builders.SPDXValueError)
    def test_invalid_creator_type(self):
        self.builder.add_creator(self.document, 'hello')

    def test_created(self):
        created_str = '2010-02-03T00:00:00Z'
        assert self.builder.set_created_date(self.document, created_str)

    @testing_utils.raises(builders.CardinalityError)
    def test_more_than_one_created(self):
        created_str = '2010-02-03T00:00:00Z'
        self.builder.set_created_date(self.document, created_str)
        self.builder.set_created_date(self.document, created_str)

    @testing_utils.raises(builders.SPDXValueError)
    def test_created_value(self):
        created_str = '2010-02-03T00:00:00'
        self.builder.set_created_date(self.document, created_str)

    def test_license_list_vers(self):
        vers_str = '1.2'
        assert self.builder.set_lics_list_ver(self.document, vers_str)
        assert (self.document.creation_info.license_list_version ==
                Version(1, 2))

    @testing_utils.raises(builders.SPDXValueError)
    def test_lics_list_ver_value(self):
        self.builder.set_lics_list_ver(self.document, '1 2')

    @testing_utils.raises(builders.CardinalityError)
    def test_lics_list_ver_card(self):
        self.builder.set_lics_list_ver(self.document, '1.2')
        self.builder.set_lics_list_ver(self.document, '1.3')


class TestReviewBuilder(TestCase):

    def setUp(self):
        self.entity_builder = builders.EntityBuilder()
        self.builder = builders.ReviewBuilder()
        self.document = Document()

    @testing_utils.raises(builders.OrderError)
    def test_reviewed_without_reviewer(self):
        date_str = '2010-02-03T00:00:00Z'
        self.builder.add_review_date(self.document, date_str)

    @testing_utils.raises(builders.OrderError)
    def test_comment_without_reviewer(self):
        comment = '<text>Comment</text>'
        self.builder.add_review_comment(self.document, comment)

    @testing_utils.raises(builders.CardinalityError)
    def test_comment_cardinality(self):
        comment = '<text>Comment</text>'
        self.add_reviewer()
        assert self.builder.add_review_comment(self.document, comment)
        self.builder.add_review_comment(self.document, comment)

    @testing_utils.raises(builders.CardinalityError)
    def test_reviewed_cardinality(self):
        date_str = '2010-02-03T00:00:00Z'
        self.add_reviewer()
        assert self.builder.add_review_date(self.document, date_str)
        self.builder.add_review_date(self.document, date_str)

    def test_comment_reset(self):
        comment = '<text>Comment</text>'
        self.add_reviewer()
        assert self.builder.add_review_comment(self.document, comment)
        self.add_reviewer()
        assert self.builder.add_review_comment(self.document, comment)

    def test_reviewed_reset(self):
        date_str = '2010-02-03T00:00:00Z'
        self.add_reviewer()
        assert self.builder.add_review_date(self.document, date_str)
        self.add_reviewer()
        assert self.builder.add_review_date(self.document, date_str)

    @testing_utils.raises(builders.SPDXValueError)
    def test_date_value(self):
        date_str = '2010-2-03T00:00:00Z'
        self.add_reviewer()
        self.builder.add_review_date(self.document, date_str)

    @testing_utils.raises(builders.SPDXValueError)
    def test_comment_value(self):
        comment = '<text>Comment<text>'
        self.add_reviewer()
        self.builder.add_review_comment(self.document, comment)

    def add_reviewer(self):
        per_str = 'Person: Bob (bob@example.com)'
        per = self.entity_builder.build_person(self.document, per_str)
        self.builder.add_reviewer(self.document, per)


class TestPackageBuilder(TestCase):

    def setUp(self):
        self.builder = builders.PackageBuilder()
        self.document = Document()
        self.entity_builder = builders.EntityBuilder()

    @testing_utils.raises(builders.CardinalityError)
    def test_package_cardinality(self):
        assert self.builder.create_package(self.document, 'pkg1')
        self.builder.create_package(self.document, 'pkg2')

    def make_package(self):
        self.builder.create_package(self.document, 'pkg')

    def make_person(self):
        per_str = 'Person: Bob (bob@example.com)'
        per = self.entity_builder.build_person(self.document, per_str)
        return per

    @testing_utils.raises(builders.OrderError)
    def test_vers_order(self):
        self.builder.set_pkg_vers(self.document, '1.1')

    @testing_utils.raises(builders.OrderError)
    def test_file_name_order(self):
        self.builder.set_pkg_file_name(self.document, 'test.jar')

    @testing_utils.raises(builders.OrderError)
    def test_pkg_supplier_order(self):
        self.builder.set_pkg_supplier(self.document, self.make_person())

    @testing_utils.raises(builders.OrderError)
    def test_pkg_originator_order(self):
        self.builder.set_pkg_originator(self.document, self.make_person())

    @testing_utils.raises(builders.OrderError)
    def test_pkg_down_loc_order(self):
        self.builder.set_pkg_down_location(
            self.document, 'http://example.com/pkg')

    @testing_utils.raises(builders.OrderError)
    def test_pkg_home_order(self):
        self.builder.set_pkg_home(self.document, 'http://example.com')

    @testing_utils.raises(builders.OrderError)
    def test_pkg_verif_order(self):
        self.builder.set_pkg_verif_code(self.document, 'some code')

    @testing_utils.raises(builders.OrderError)
    def test_pkg_chksum_order(self):
        self.builder.set_pkg_chk_sum(self.document, 'some code')

    @testing_utils.raises(builders.OrderError)
    def test_pkg_source_info_order(self):
        self.builder.set_pkg_source_info(self.document, 'hello')

    @testing_utils.raises(builders.OrderError)
    def test_pkg_licenses_concluded_order(self):
        self.builder.set_pkg_licenses_concluded(self.document, 'some license')

    @testing_utils.raises(builders.OrderError)
    def test_pkg_lics_from_file_order(self):
        self.builder.set_pkg_license_from_file(self.document, 'some license')

    @testing_utils.raises(builders.OrderError)
    def test_pkg_lics_decl_order(self):
        self.builder.set_pkg_license_declared(self.document, 'license')

    @testing_utils.raises(builders.OrderError)
    def test_pkg_lics_comment_order(self):
        self.builder.set_pkg_license_comment(
            self.document, '<text>hello</text>')

    @testing_utils.raises(builders.OrderError)
    def test_pkg_cr_text_order(self):
        self.builder.set_pkg_cr_text(self.document, '<text>Something</text>')

    @testing_utils.raises(builders.OrderError)
    def test_pkg_summary_order(self):
        self.builder.set_pkg_summary(self.document, '<text>Something</text>')

    @testing_utils.raises(builders.OrderError)
    def test_set_pkg_desc_order(self):
        self.builder.set_pkg_desc(self.document, '<text>something</text>')


if __name__ == '__main__':
    unittest.main()
