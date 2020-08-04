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

from unittest import TestCase

import tests.testing_utils as testing_utils

from spdx.document import Document, License
import spdx.parsers.tagvaluebuilders as builders
from spdx.version import Version


class TestDocumentBuilder(TestCase):
    maxDiff = None

    def setUp(self):
        self.document = Document()
        self.builder = builders.DocBuilder()

    def test_correct_version(self):
        version_str = "SPDX-2.1"
        self.builder.set_doc_version(self.document, version_str)
        assert self.document.version.major == 2 and self.document.version.minor == 1

    @testing_utils.raises(builders.CardinalityError)
    def test_version_cardinality(self):
        version_str = "SPDX-2.1"
        self.builder.set_doc_version(self.document, version_str)
        self.builder.set_doc_version(self.document, version_str)

    @testing_utils.raises(builders.SPDXValueError)
    def test_version_value(self):
        version_str = "2.1"
        self.builder.set_doc_version(self.document, version_str)

    def test_correct_data_lics(self):
        lics_str = "CC0-1.0"
        self.builder.set_doc_data_lics(self.document, lics_str)
        assert self.document.data_license == License.from_identifier(lics_str)

    @testing_utils.raises(builders.SPDXValueError)
    def test_data_lics_value(self):
        lics_str = "GPL"
        self.builder.set_doc_data_lics(self.document, lics_str)

    @testing_utils.raises(builders.CardinalityError)
    def test_data_lics_cardinality(self):
        lics_str = "CC0-1.0"
        self.builder.set_doc_data_lics(self.document, lics_str)
        self.builder.set_doc_data_lics(self.document, lics_str)

    def test_correct_name(self):
        name_str = "Sample_Document-V2.1"
        self.builder.set_doc_name(self.document, name_str)
        assert self.document.name == name_str

    @testing_utils.raises(builders.CardinalityError)
    def test_name_cardinality(self):
        name_str = "Sample_Document-V2.1"
        self.builder.set_doc_name(self.document, name_str)
        self.builder.set_doc_name(self.document, name_str)

    def test_correct_doc_namespace(self):
        doc_namespace_str = "https://spdx.org/spdxdocs/spdx-example-444504E0-4F89-41D3-9A0C-0305E82C3301"
        self.builder.set_doc_namespace(self.document, doc_namespace_str)
        assert self.document.namespace == doc_namespace_str

    @testing_utils.raises(builders.SPDXValueError)
    def test_doc_namespace_value(self):
        doc_namespace_str = "https://spdx.org/spdxdocs/spdx-example-444504E0-4F89-41D3-9A0C-0305E82C3301#SPDXRef-DOCUMENT"
        self.builder.set_doc_data_lics(self.document, doc_namespace_str)

    @testing_utils.raises(builders.CardinalityError)
    def test_doc_namespace_cardinality(self):
        doc_namespace_str = "https://spdx.org/spdxdocs/spdx-example-444504E0-4F89-41D3-9A0C-0305E82C3301"
        self.builder.set_doc_namespace(self.document, doc_namespace_str)
        self.builder.set_doc_namespace(self.document, doc_namespace_str)

    def test_correct_data_comment(self):
        comment_str = "This is a comment."
        comment_text = "<text>" + comment_str + "</text>"
        self.builder.set_doc_comment(self.document, comment_text)
        assert self.document.comment == comment_str

    @testing_utils.raises(builders.CardinalityError)
    def test_comment_cardinality(self):
        comment_str = "This is a comment."
        comment_text = "<text>" + comment_str + "</text>"
        self.builder.set_doc_comment(self.document, comment_text)
        self.builder.set_doc_comment(self.document, comment_text)

    @testing_utils.raises(builders.SPDXValueError)
    def test_comment_value(self):
        comment = "<text>slslss<text"
        self.builder.set_doc_comment(self.document, comment)


class TestExternalDocumentRefBuilder(TestCase):
    maxDiff = None

    def setUp(self):
        self.document = Document()
        self.builder = builders.ExternalDocumentRefBuilder()

    def test_external_doc_id(self):
        ext_doc_id = "DocumentRef-spdx-tool-2.1"
        self.builder.set_ext_doc_id(self.document, ext_doc_id)
        assert (
            self.document.ext_document_references[-1].external_document_id == ext_doc_id
        )

    def test_spdx_doc_uri(self):
        spdx_doc_uri = "https://spdx.org/spdxdocs/spdx-tools-v2.1-3F2504E0-4F89-41D3-9A0C-0305E82C3301"
        self.builder.set_ext_doc_id(self.document, "DocumentRef-spdx-tool-2.1")
        self.builder.set_spdx_doc_uri(self.document, spdx_doc_uri)
        assert (
            self.document.ext_document_references[-1].spdx_document_uri == spdx_doc_uri
        )

    def test_checksum(self):
        chksum = "SHA1: d6a770ba38583ed4bb4525bd96e50461655d2759"
        chksum_val = "d6a770ba38583ed4bb4525bd96e50461655d2759"
        self.builder.set_ext_doc_id(self.document, "DocumentRef-spdx-tool-2.1")
        self.builder.set_chksum(self.document, chksum)
        assert self.document.ext_document_references[-1].check_sum.value == chksum_val

    def test_add_ext_doc_refs(self):
        ext_doc_id_val = "DocumentRef-spdx-tool-2.1"
        spdx_doc_uri = "http://spdx.org/spdxdocs/spdx-tools-v2.1-3F2504E0-4F89-41D3-9A0C-0305E82C3301"
        chksum = "SHA1: d6a770ba38583ed4bb4525bd96e50461655d2759"
        chksum_val = "d6a770ba38583ed4bb4525bd96e50461655d2759"

        self.builder.add_ext_doc_refs(
            self.document, ext_doc_id_val, spdx_doc_uri, chksum
        )
        assert (
            self.document.ext_document_references[-1].external_document_id
            == ext_doc_id_val
        )
        assert (
            self.document.ext_document_references[-1].spdx_document_uri == spdx_doc_uri
        )
        assert self.document.ext_document_references[-1].check_sum.value == chksum_val


class TestEntityBuilder(TestCase):
    maxDiff = None

    def setUp(self):
        self.builder = builders.EntityBuilder()
        self.document = Document()

    def test_tool(self):
        tool_name = "autoanal-2.0"
        tool_str = "Tool: " + tool_name
        tool = self.builder.build_tool(self.document, tool_str)
        assert tool.name == tool_name

    @testing_utils.raises(builders.SPDXValueError)
    def test_tool_value_error(self):
        tool_str = "tool: ll"
        self.builder.build_tool(self.document, tool_str)

    def test_org_with_email(self):
        org_name = "Example"
        org_email = "example@example.org"
        org_str = "Organization: {0} ( {1} )".format(org_name, org_email)
        org = self.builder.build_org(self.document, org_str)
        assert org.name == org_name
        assert org.email == org_email

    def test_org(self):
        org_name = "Example"
        org_str = "Organization: {0} ()".format(org_name)
        org = self.builder.build_org(self.document, org_str)
        assert org.name == org_name
        assert org.email is None

    @testing_utils.raises(builders.SPDXValueError)
    def test_org_value_error(self):
        org_name = "Example"
        org_str = "Organization {0}".format(org_name)
        self.builder.build_org(self.document, org_str)

    def test_person_with_email(self):
        per_name = "Bob"
        per_email = "bob@example.org"
        per_str = "Person: {0} ( {1} )".format(per_name, per_email)
        per = self.builder.build_person(self.document, per_str)
        assert per.name == per_name
        assert per.email == per_email

    def test_per(self):
        per_name = "Bob"
        per_str = "Person: {0} ()".format(per_name)
        per = self.builder.build_person(self.document, per_str)
        assert per.name == per_name
        assert per.email is None

    @testing_utils.raises(builders.SPDXValueError)
    def test_per_value_error(self):
        per_name = "Bob"
        per_str = "Person {0}".format(per_name)
        self.builder.build_person(self.document, per_str)


class TestCreationInfoBuilder(TestCase):
    maxDiff = None

    def setUp(self):
        self.document = Document()
        self.builder = builders.CreationInfoBuilder()
        self.entity_builder = builders.EntityBuilder()

    def test_add_creator(self):
        per_str = "Person: Bob (bob@example.com)"
        per = self.entity_builder.build_person(self.document, per_str)
        assert self.builder.add_creator(self.document, per)
        assert len(self.document.creation_info.creators) == 1
        assert self.document.creation_info.creators[0] == per

    @testing_utils.raises(builders.SPDXValueError)
    def test_invalid_creator_type(self):
        self.builder.add_creator(self.document, "hello")

    def test_created(self):
        created_str = "2010-02-03T00:00:00Z"
        assert self.builder.set_created_date(self.document, created_str)

    @testing_utils.raises(builders.CardinalityError)
    def test_more_than_one_created(self):
        created_str = "2010-02-03T00:00:00Z"
        self.builder.set_created_date(self.document, created_str)
        self.builder.set_created_date(self.document, created_str)

    @testing_utils.raises(builders.SPDXValueError)
    def test_created_value(self):
        created_str = "2010-02-03T00:00:00"
        self.builder.set_created_date(self.document, created_str)

    def test_license_list_vers(self):
        vers_str = "1.2"
        assert self.builder.set_lics_list_ver(self.document, vers_str)
        assert self.document.creation_info.license_list_version == Version(1, 2)

    @testing_utils.raises(builders.SPDXValueError)
    def test_lics_list_ver_value(self):
        self.builder.set_lics_list_ver(self.document, "1 2")

    @testing_utils.raises(builders.CardinalityError)
    def test_lics_list_ver_card(self):
        self.builder.set_lics_list_ver(self.document, "1.2")
        self.builder.set_lics_list_ver(self.document, "1.3")


class TestReviewBuilder(TestCase):
    maxDiff = None

    def setUp(self):
        self.entity_builder = builders.EntityBuilder()
        self.builder = builders.ReviewBuilder()
        self.document = Document()

    @testing_utils.raises(builders.OrderError)
    def test_reviewed_without_reviewer(self):
        date_str = "2010-02-03T00:00:00Z"
        self.builder.add_review_date(self.document, date_str)

    @testing_utils.raises(builders.OrderError)
    def test_comment_without_reviewer(self):
        comment = "<text>Comment</text>"
        self.builder.add_review_comment(self.document, comment)

    @testing_utils.raises(builders.CardinalityError)
    def test_comment_cardinality(self):
        comment = "<text>Comment</text>"
        self.add_reviewer()
        assert self.builder.add_review_comment(self.document, comment)
        self.builder.add_review_comment(self.document, comment)

    @testing_utils.raises(builders.CardinalityError)
    def test_reviewed_cardinality(self):
        date_str = "2010-02-03T00:00:00Z"
        self.add_reviewer()
        assert self.builder.add_review_date(self.document, date_str)
        self.builder.add_review_date(self.document, date_str)

    def test_comment_reset(self):
        comment = "<text>Comment</text>"
        self.add_reviewer()
        assert self.builder.add_review_comment(self.document, comment)
        self.add_reviewer()
        assert self.builder.add_review_comment(self.document, comment)

    def test_reviewed_reset(self):
        date_str = "2010-02-03T00:00:00Z"
        self.add_reviewer()
        assert self.builder.add_review_date(self.document, date_str)
        self.add_reviewer()
        assert self.builder.add_review_date(self.document, date_str)

    @testing_utils.raises(builders.SPDXValueError)
    def test_date_value(self):
        date_str = "2010-2-03T00:00:00Z"
        self.add_reviewer()
        self.builder.add_review_date(self.document, date_str)

    @testing_utils.raises(builders.SPDXValueError)
    def test_comment_value(self):
        comment = "<text>Comment<text>"
        self.add_reviewer()
        self.builder.add_review_comment(self.document, comment)

    def add_reviewer(self):
        per_str = "Person: Bob (bob@example.com)"
        per = self.entity_builder.build_person(self.document, per_str)
        self.builder.add_reviewer(self.document, per)


class TestAnnotationBuilder(TestCase):
    maxDiff = None

    def setUp(self):
        self.entity_builder = builders.EntityBuilder()
        self.builder = builders.AnnotationBuilder()
        self.document = Document()

    @testing_utils.raises(builders.OrderError)
    def test_annotation_without_annotator(self):
        date_str = "2014-08-06T00:00:00Z"
        self.builder.add_annotation_date(self.document, date_str)

    @testing_utils.raises(builders.OrderError)
    def test_comment_without_annotator(self):
        comment = "<text>Comment without annotator</text>"
        self.builder.add_annotation_comment(self.document, comment)

    @testing_utils.raises(builders.OrderError)
    def test_type_without_annotator(self):
        annotation_type = "REVIEW"
        self.builder.add_annotation_type(self.document, annotation_type)

    @testing_utils.raises(builders.OrderError)
    def test_spdx_id_without_annotator(self):
        spdx_id = "SPDXRef-45"
        self.builder.set_annotation_spdx_id(self.document, spdx_id)

    @testing_utils.raises(builders.CardinalityError)
    def test_annotation_comment_cardinality(self):
        comment = "<text>Annotation Comment</text>"
        self.add_annotator()
        assert self.builder.add_annotation_comment(self.document, comment)
        self.builder.add_annotation_comment(self.document, comment)

    @testing_utils.raises(builders.CardinalityError)
    def test_annotation_cardinality(self):
        date_str = "2014-08-06T00:00:00Z"
        self.add_annotator()
        assert self.builder.add_annotation_date(self.document, date_str)
        self.builder.add_annotation_date(self.document, date_str)

    @testing_utils.raises(builders.CardinalityError)
    def test_annotation_spdx_id_cardinality(self):
        spdx_id = "SPDXRef-45"
        self.add_annotator()
        self.builder.set_annotation_spdx_id(self.document, spdx_id)
        self.builder.set_annotation_spdx_id(self.document, spdx_id)

    def test_annotation_comment_reset(self):
        comment = "<text>Annotation Comment</text>"
        self.add_annotator()
        assert self.builder.add_annotation_comment(self.document, comment)
        self.add_annotator()
        assert self.builder.add_annotation_comment(self.document, comment)

    def test_annotation_reset(self):
        date_str = "2014-08-06T00:00:00Z"
        self.add_annotator()
        assert self.builder.add_annotation_date(self.document, date_str)
        self.add_annotator()
        assert self.builder.add_annotation_date(self.document, date_str)

    @testing_utils.raises(builders.SPDXValueError)
    def test_annotation_date_value(self):
        date_str = "2014-8-06T00:00:00Z"
        self.add_annotator()
        self.builder.add_annotation_date(self.document, date_str)

    @testing_utils.raises(builders.SPDXValueError)
    def test_annotation_comment_value(self):
        comment = "<text>Annotation Comment<text>"
        self.add_annotator()
        self.builder.add_annotation_comment(self.document, comment)

    @testing_utils.raises(builders.SPDXValueError)
    def test_incorrect_annotation_type_value(self):
        annotation_type = "Some random value instead of REVIEW or OTHER"
        self.add_annotator()
        self.builder.add_annotation_type(self.document, annotation_type)

    def test_correct_annotation_type(self):
        annotation_type = "REVIEW"
        self.add_annotator()
        assert self.builder.add_annotation_type(self.document, annotation_type)

    def test_correct_annotation_spdx_id(self):
        spdx_id = "SPDXRef-45"
        self.add_annotator()
        self.builder.set_annotation_spdx_id(self.document, spdx_id)

    @testing_utils.raises(builders.CardinalityError)
    def test_annotation_type_cardinality(self):
        annotation_type = "REVIEW"
        self.add_annotator()
        assert self.builder.add_annotation_type(self.document, annotation_type)
        self.builder.add_annotation_type(self.document, annotation_type)

    def add_annotator(self):
        per_str = "Person: Jim (jim@example.com)"
        per = self.entity_builder.build_person(self.document, per_str)
        self.builder.add_annotator(self.document, per)


class TestRelationshipBuilder(TestCase):
    maxDiff = None

    def setUp(self):
        self.entity_builder = builders.EntityBuilder()
        self.builder = builders.RelationshipBuilder()
        self.document = Document()

    @testing_utils.raises(builders.OrderError)
    def test_relationship_comment_without_relationship(self):
        comment = "<text>Comment without relationship</text>"
        self.builder.add_relationship_comment(self.document, comment)

    def test_relationship_comment_reset(self):
        comment = "<text>Relationship Comment</text>"
        self.add_relationship()
        assert self.builder.add_relationship_comment(self.document, comment)
        self.add_relationship()
        assert self.builder.add_relationship_comment(self.document, comment)

    @testing_utils.raises(builders.SPDXValueError)
    def test_relationship_comment_value(self):
        comment = "<text>Relationship Comment<text>"
        self.add_relationship()
        self.builder.add_relationship_comment(self.document, comment)

    def test_correct_relationship(self):
        relationship = "SPDXRef-DOCUMENT DESCRIBES SPDXRef-File"
        assert self.builder.add_relationship(self.document, relationship)

    def add_relationship(self):
        relate_str = "SPDXRef-DOCUMENT DESCRIBES SPDXRef-File"
        self.builder.add_relationship(self.document, relate_str)


class TestPackageBuilder(TestCase):
    maxDiff = None

    def setUp(self):
        self.builder = builders.PackageBuilder()
        self.document = Document()
        self.entity_builder = builders.EntityBuilder()

    @testing_utils.raises(builders.CardinalityError)
    def test_package_cardinality(self):
        assert self.builder.create_package(self.document, "pkg1")
        self.builder.create_package(self.document, "pkg2")

    def make_package(self):
        self.builder.create_package(self.document, "pkg")

    def make_person(self):
        per_str = "Person: Bob (bob@example.com)"
        per = self.entity_builder.build_person(self.document, per_str)
        return per

    @testing_utils.raises(builders.OrderError)
    def test_vers_order(self):
        self.builder.set_pkg_vers(self.document, "1.1")

    @testing_utils.raises(builders.OrderError)
    def test_file_name_order(self):
        self.builder.set_pkg_file_name(self.document, "test.jar")

    @testing_utils.raises(builders.OrderError)
    def test_pkg_supplier_order(self):
        self.builder.set_pkg_supplier(self.document, self.make_person())

    @testing_utils.raises(builders.OrderError)
    def test_pkg_originator_order(self):
        self.builder.set_pkg_originator(self.document, self.make_person())

    @testing_utils.raises(builders.OrderError)
    def test_pkg_down_loc_order(self):
        self.builder.set_pkg_down_location(self.document, "http://example.com/pkg")

    @testing_utils.raises(builders.OrderError)
    def test_pkg_home_order(self):
        self.builder.set_pkg_home(self.document, "http://example.com")

    @testing_utils.raises(builders.OrderError)
    def test_pkg_verif_order(self):
        self.builder.set_pkg_verif_code(self.document, "some code")

    @testing_utils.raises(builders.OrderError)
    def test_pkg_chksum_order(self):
        self.builder.set_pkg_chk_sum(self.document, "some code")

    @testing_utils.raises(builders.OrderError)
    def test_pkg_source_info_order(self):
        self.builder.set_pkg_source_info(self.document, "hello")

    @testing_utils.raises(builders.OrderError)
    def test_pkg_licenses_concluded_order(self):
        self.builder.set_pkg_licenses_concluded(self.document, "some license")

    @testing_utils.raises(builders.OrderError)
    def test_pkg_lics_from_file_order(self):
        self.builder.set_pkg_license_from_file(self.document, "some license")

    @testing_utils.raises(builders.OrderError)
    def test_pkg_lics_decl_order(self):
        self.builder.set_pkg_license_declared(self.document, "license")

    @testing_utils.raises(builders.OrderError)
    def test_pkg_lics_comment_order(self):
        self.builder.set_pkg_license_comment(self.document, "<text>hello</text>")

    @testing_utils.raises(builders.OrderError)
    def test_pkg_attribution_text_order(self):
        self.builder.set_pkg_attribution_text(self.document, "<text>hello</text>")

    def test_correct_pkg_attribution_text(self):
        self.builder.create_package(self.document, "pkg")
        self.builder.set_pkg_attribution_text(self.document, "<text>something</text>")

    @testing_utils.raises(builders.SPDXValueError)
    def test_incorrect_pkg_attribution_text(self):
        self.builder.create_package(self.document, "pkg")
        self.builder.set_pkg_attribution_text(self.document, "not_free_form_text")

    @testing_utils.raises(builders.OrderError)
    def test_pkg_cr_text_order(self):
        self.builder.set_pkg_cr_text(self.document, "<text>Something</text>")

    @testing_utils.raises(builders.OrderError)
    def test_pkg_summary_order(self):
        self.builder.set_pkg_summary(self.document, "<text>Something</text>")

    @testing_utils.raises(builders.OrderError)
    def test_set_pkg_desc_order(self):
        self.builder.set_pkg_desc(self.document, "<text>something</text>")

    @testing_utils.raises(builders.OrderError)
    def test_set_pkg_spdx_id_order(self):
        self.builder.set_pkg_spdx_id(self.document, "SPDXRe-Package")

    @testing_utils.raises(builders.OrderError)
    def test_set_pkg_files_analyzed_order(self):
        self.builder.set_pkg_files_analyzed(self.document, "True")

    @testing_utils.raises(builders.OrderError)
    def test_set_pkg_comment_order(self):
        self.builder.set_pkg_comment(self.document, "<text>something</text>")

    def test_correct_pkg_comment(self):
        self.builder.create_package(self.document, "pkg")
        self.builder.set_pkg_comment(self.document, "<text>something</text>")

    @testing_utils.raises(builders.SPDXValueError)
    def test_incorrect_pkg_comment(self):
        self.builder.create_package(self.document, "pkg")
        self.builder.set_pkg_comment(self.document, "not_free_form_text")

    def test_correct_pkg_spdx_id(self):
        self.builder.create_package(self.document, "pkg")
        assert self.builder.set_pkg_spdx_id(self.document, "SPDXRef-Package")
        assert self.document.package.spdx_id == "SPDXRef-Package"

    @testing_utils.raises(builders.SPDXValueError)
    def test_incorrect_pkg_spdx_id(self):
        self.builder.create_package(self.document, "pkg")
        assert self.builder.set_pkg_spdx_id(self.document, "SPDXRe-Package")

    @testing_utils.raises(builders.SPDXValueError)
    def test_incorrect_pkg_files_analyzed(self):
        self.builder.create_package(self.document, "pkg")
        assert self.builder.set_pkg_files_analyzed(self.document, "XYZ")

    def test_correct_pkg_files_analyzed_1(self):
        self.builder.create_package(self.document, "pkg")
        assert self.builder.set_pkg_files_analyzed(self.document, "True")

    def test_correct_pkg_files_analyzed_2(self):
        self.builder.create_package(self.document, "pkg")
        assert self.builder.set_pkg_files_analyzed(self.document, "true")

    def test_correct_pkg_ext_ref_category(self):
        category = "SECURITY"
        self.builder.create_package(self.document, "pkg")
        self.builder.set_pkg_ext_ref_category(self.document, category)
        assert self.document.package.pkg_ext_refs[-1].category == category

    @testing_utils.raises(builders.SPDXValueError)
    def test_incorrect_pkg_ext_ref_category(self):
        category = "some_other_value"
        self.builder.create_package(self.document, "pkg")
        self.builder.set_pkg_ext_ref_category(self.document, category)

    def test_correct_pkg_ext_ref_type(self):
        pkg_ext_ref_type = "cpe23Type"
        self.builder.create_package(self.document, "pkg")
        self.builder.set_pkg_ext_ref_type(self.document, pkg_ext_ref_type)
        assert (
            self.document.package.pkg_ext_refs[-1].pkg_ext_ref_type == pkg_ext_ref_type
        )

    @testing_utils.raises(builders.SPDXValueError)
    def test_incorrect_pkg_ext_ref_type(self):
        pkg_ext_ref_type = "cpe23Type_with_special_symbols&%"
        self.builder.create_package(self.document, "pkg")
        self.builder.set_pkg_ext_ref_type(self.document, pkg_ext_ref_type)

    def test_correct_pkg_ext_ref_locator(self):
        locator = "cpe:2.3:a:pivotal_software:spring_framework:4.1.0:*:*:*"
        self.builder.create_package(self.document, "pkg")
        self.builder.set_pkg_ext_ref_locator(self.document, locator)
        assert self.document.package.pkg_ext_refs[-1].locator == locator

    @testing_utils.raises(builders.OrderError)
    def test_pkg_ext_ref_without_pkg(self):
        locator = "cpe:2.3:a:pivotal_software:spring_framework:4.1.0:*:*:*"
        self.builder.set_pkg_ext_ref_locator(self.document, locator)

    def test_correct_pkg_ext_comment(self):
        comment_str = "This is a comment."
        comment_text = "<text>" + comment_str + "</text>"
        self.builder.create_package(self.document, "pkg")
        self.builder.set_pkg_ext_ref_category(self.document, "SECURITY")
        self.builder.add_pkg_ext_ref_comment(self.document, comment_text)
        assert self.document.package.pkg_ext_refs[-1].comment == comment_str

    @testing_utils.raises(builders.OrderError)
    def test_pkg_ext_comment_without_pkg_ext_ref(self):
        comment_str = "This is a comment."
        comment_text = "<text>" + comment_str + "</text>"
        self.builder.create_package(self.document, "pkg")
        self.builder.add_pkg_ext_ref_comment(self.document, comment_text)


class TestSnippetBuilder(TestCase):
    maxDiff = None

    def setUp(self):
        self.entity_builder = builders.EntityBuilder()
        self.builder = builders.SnippetBuilder()
        self.document = Document()

    def test_create_snippet(self):
        assert self.builder.create_snippet(self.document, "SPDXRef-Snippet")

    @testing_utils.raises(builders.SPDXValueError)
    def test_incorrect_snippet_spdx_id(self):
        self.builder.create_snippet(self.document, "Some_value_with_$%")

    def test_snippet_name(self):
        self.builder.create_snippet(self.document, "SPDXRef-Snippet")
        self.builder.set_snippet_name(self.document, "Name_of_snippet")

    @testing_utils.raises(builders.OrderError)
    def test_snippet_name_order(self):
        self.builder.set_snippet_name(self.document, "Name_of_snippet")

    def test_snippet_comment(self):
        self.builder.create_snippet(self.document, "SPDXRef-Snippet")
        self.builder.set_snippet_comment(self.document, "<text>Comment</text>")

    @testing_utils.raises(builders.OrderError)
    def test_snippet_comment_order(self):
        self.builder.set_snippet_comment(self.document, "<text>Comment</text>")

    @testing_utils.raises(builders.SPDXValueError)
    def test_snippet_comment_text_value(self):
        self.builder.create_snippet(self.document, "SPDXRef-Snippet")
        self.builder.set_snippet_comment(self.document, "Comment.")

    @testing_utils.raises(builders.OrderError)
    def test_snippet_attribution_text_order(self):
        self.builder.set_snippet_attribution_text(self.document, "<text>hello</text>")

    def test_correct_snippet_attribution_text(self):
        self.builder.create_snippet(self.document, "SPDXRef-Snippet")
        self.builder.set_snippet_attribution_text(
            self.document, "<text>something</text>"
        )

    @testing_utils.raises(builders.SPDXValueError)
    def test_incorrect_snippet_attribution_text(self):
        self.builder.create_snippet(self.document, "SPDXRef-Package")
        self.builder.set_snippet_attribution_text(self.document, "not_free_form_text")

    def test_snippet_copyright(self):
        self.builder.create_snippet(self.document, "SPDXRef-Snippet")
        self.builder.set_snippet_copyright(
            self.document, "<text>Copyright 2008-2010 John Smith</text>"
        )

    @testing_utils.raises(builders.SPDXValueError)
    def test_snippet_copyright_text_value(self):
        self.builder.create_snippet(self.document, "SPDXRef-Snippet")
        self.builder.set_snippet_copyright(
            self.document, "Copyright 2008-2010 John Smith"
        )

    @testing_utils.raises(builders.OrderError)
    def test_snippet_copyright_order(self):
        self.builder.set_snippet_copyright(
            self.document, "<text>Copyright 2008-2010 John Smith</text>"
        )

    def test_snippet_lic_comment(self):
        self.builder.create_snippet(self.document, "SPDXRef-Snippet")
        self.builder.set_snippet_lic_comment(self.document, "<text>Lic comment</text>")

    @testing_utils.raises(builders.SPDXValueError)
    def test_snippet_lic_comment_text_value(self):
        self.builder.create_snippet(self.document, "SPDXRef-Snippet")
        self.builder.set_snippet_lic_comment(self.document, "Lic comment")

    @testing_utils.raises(builders.OrderError)
    def test_snippet_lic_comment_order(self):
        self.builder.set_snippet_lic_comment(self.document, "<text>Lic comment</text>")

    def test_snippet_from_file_spdxid(self):
        self.builder.create_snippet(self.document, "SPDXRef-Snippet")
        self.builder.set_snip_from_file_spdxid(self.document, "SPDXRef-DoapSource")

    @testing_utils.raises(builders.SPDXValueError)
    def test_snippet_from_file_spdxid_value(self):
        self.builder.create_snippet(self.document, "SPDXRef-Snippet")
        self.builder.set_snip_from_file_spdxid(self.document, "#_$random_chars")

    @testing_utils.raises(builders.OrderError)
    def test_snippet_from_file_spdxid_order(self):
        self.builder.set_snip_from_file_spdxid(self.document, "SPDXRef-DoapSource")

    @testing_utils.raises(builders.CardinalityError)
    def test_snippet_from_file_spdxid_cardinality(self):
        self.builder.create_snippet(self.document, "SPDXRef-Snippet")
        self.builder.set_snip_from_file_spdxid(self.document, "SPDXRef-DoapSource")
        self.builder.set_snip_from_file_spdxid(self.document, "SPDXRef-somevalue")

    def test_snippet_conc_lics(self):
        self.builder.create_snippet(self.document, "SPDXRef-Snippet")
        self.builder.set_snip_concluded_license(
            self.document, License.from_identifier("Apache-2.0")
        )

    @testing_utils.raises(builders.SPDXValueError)
    def test_snippet_conc_lics_value(self):
        self.builder.create_snippet(self.document, "SPDXRef-Snippet")
        self.builder.set_snip_concluded_license(self.document, "Apache-2.0")

    @testing_utils.raises(builders.OrderError)
    def test_snippet_conc_lics_order(self):
        self.builder.set_snip_concluded_license(
            self.document, License.from_identifier("Apache-2.0")
        )

    @testing_utils.raises(builders.CardinalityError)
    def test_snippet_conc_lics_cardinality(self):
        self.builder.create_snippet(self.document, "SPDXRef-Snippet")
        self.builder.set_snip_concluded_license(
            self.document, License.from_identifier("Apache-2.0")
        )
        self.builder.set_snip_concluded_license(
            self.document, License.from_identifier("Apache-2.0")
        )

    def test_snippet_lics_info(self):
        self.builder.create_snippet(self.document, "SPDXRef-Snippet")
        self.builder.set_snippet_lics_info(
            self.document, License.from_identifier("Apache-2.0")
        )
        self.builder.set_snippet_lics_info(
            self.document, License.from_identifier("GPL-2.0-or-later")
        )

    @testing_utils.raises(builders.SPDXValueError)
    def test_snippet_lics_info_value(self):
        self.builder.create_snippet(self.document, "SPDXRef-Snippet")
        self.builder.set_snippet_lics_info(self.document, "Apache-2.0")

    @testing_utils.raises(builders.OrderError)
    def test_snippet_lics_info_order(self):
        self.builder.set_snippet_lics_info(
            self.document, License.from_identifier("Apache-2.0")
        )
