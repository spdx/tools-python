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