# Copyright 2014 Ahmed H. Ismail

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import nose
import spdx.parsers.tagvaluebuilders as builders
from spdx.document import Document, License
from spdx.version import Version

class TestDocumentBuilder(object):

    def __init__(self):
        self.document = Document()
        self.builder = builders.DocBuilder()

    def test_correct_version(self):
        version_str = 'SPDX-1.2'
        self.builder.set_doc_version(self.document, version_str)
        assert (self.document.version.major == 1) & (self.document.version.minor == 2)

    @nose.tools.raises(builders.CardinalityError)
    def test_version_cardinality(self):
        version_str = 'SPDX-1.2'
        self.builder.set_doc_version(self.document, version_str)
        self.builder.set_doc_version(self.document, version_str)

    @nose.tools.raises(builders.ValueError)
    def test_version_value(self):
        version_str = '1.2'
        self.builder.set_doc_version(self.document, version_str)

    @nose.tools.raises(builders.IncompatibleVersionError)
    def test_version_number(self):
        version_str = 'SPDX-2.0'
        self.builder.set_doc_version(self.document, version_str)

    def test_correct_data_lics(self):
        lics_str = 'CC0-1.0'
        self.builder.set_doc_data_lics(self.document, lics_str)
        assert self.document.data_license == License.from_identifier(lics_str)

    @nose.tools.raises(builders.ValueError)
    def test_data_lics_value(self):
        lics_str = 'GPL'
        self.builder.set_doc_data_lics(self.document, lics_str)

    @nose.tools.raises(builders.CardinalityError)
    def test_data_lics_cardinality(self):
        lics_str = 'CC0-1.0'
        self.builder.set_doc_data_lics(self.document, lics_str)
        self.builder.set_doc_data_lics(self.document, lics_str)

    def test_correct_data_comment(self):
        comment_str = 'This is a comment.'
        comment_text = '<text>' + comment_str + '</text>'
        self.builder.set_doc_comment(self.document, comment_text)
        assert self.document.comment == comment_str

    @nose.tools.raises(builders.CardinalityError)
    def test_comment_cardinality(self):
        comment_str = 'This is a comment.'
        comment_text = '<text>' + comment_str + '</text>'
        self.builder.set_doc_comment(self.document, comment_text)
        self.builder.set_doc_comment(self.document, comment_text)

    @nose.tools.raises(builders.ValueError)
    def test_comment_value(self):
        comment = '<text>slslss<text'
        self.builder.set_doc_comment(self.document, comment)


class TestEntityBuilder(object):
    def __init__(self):
        self.builder = builders.EntityBuilder()
        self.document = Document()

    def test_tool(self):
        tool_name = 'autoanal-2.0'
        tool_str = 'Tool: ' + tool_name
        tool = self.builder.build_tool(self.document, tool_str)
        assert tool.name == tool_name

    @nose.tools.raises(builders.ValueError)
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

    @nose.tools.raises(builders.ValueError)
    def test_org_value_error(self):
        org_name = 'Example'
        org_str = 'Organization: {0}'.format(org_name)
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

    @nose.tools.raises(builders.ValueError)
    def test_per_value_error(self):
        per_name = 'Bob'
        per_str = 'Person: {0}'.format(per_name)
        self.builder.build_person(self.document, per_str)

class TestCreationInfoBuilder(object):
    def __init__(self):
        self.document = Document()
        self.builder = builders.CreationInfoBuilder()
        self.entity_builder = builders.EntityBuilder()

    def test_add_creator(self):
        per_str = 'Person: Bob (bob@example.com)'
        per = self.entity_builder.build_person(self.document, per_str)
        assert self.builder.add_creator(self.document, per)
        assert len(self.document.creation_info.creators) == 1
        assert self.document.creation_info.creators[0] == per

    @nose.tools.raises(builders.ValueError)
    def test_invalid_creator_type(self):
        self.builder.add_creator(self.document, 'hello')

    def test_created(self):
        created_str = '2010-02-03T00:00:00Z'
        assert self.builder.set_created_date(self.document, created_str)

    @nose.tools.raises(builders.CardinalityError)
    def test_more_than_one_created(self):
        created_str = '2010-02-03T00:00:00Z'
        self.builder.set_created_date(self.document, created_str)
        self.builder.set_created_date(self.document, created_str)

    @nose.tools.raises(builders.ValueError)
    def test_created_value(self):
        created_str = '2010-02-03T00:00:00'
        self.builder.set_created_date(self.document, created_str)

    def test_license_list_vers(self):
        vers_str = '1.2'
        assert self.builder.set_lics_list_ver(self.document, vers_str)
        assert  (self.document.creation_info.license_list_version == 
            Version(1, 2))

    @nose.tools.raises(builders.ValueError)
    def test_lics_list_ver_value(self):
        self.builder.set_lics_list_ver(self.document, '1 2')

    @nose.tools.raises(builders.CardinalityError)
    def test_lics_list_ver_card(self):
       self.builder.set_lics_list_ver(self.document, '1.2')
       self.builder.set_lics_list_ver(self.document, '1.3') 


