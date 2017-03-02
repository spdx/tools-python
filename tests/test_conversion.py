
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

import codecs
import os
import tempfile
import unittest
from unittest import TestCase

from spdx.parsers.rdf import Parser as RDFParser
from spdx.parsers.rdfbuilders import Builder as RDFBuilder
from spdx.parsers.loggers import StandardLogger
from spdx.parsers.tagvalue import Parser as TVParser
from spdx.parsers.tagvaluebuilders import Builder as TVBuilder
import spdx.writers.rdf as rdfwriter
import spdx.writers.tagvalue as tvwriter


def get_temp_file(extension=''):
    """
    Return a unique new temporary file location to a non-existing
    temporary file that can safely be created without a risk of name
    collision.
    """

    if extension and not extension.startswith('.'):
            extension = '.' + extension
    file_name = 'temp_file' + extension
    temp_dir = tempfile.mkdtemp()
    return os.path.join(temp_dir, file_name)


class TestConversions(TestCase):

    def parse_rdf_file(self, file_name):
        """Returns tuple error, document."""
        with open(file_name, mode='rb') as infile:
            rdfparser = RDFParser(RDFBuilder(), StandardLogger())
            return rdfparser.parse(infile)

    def parse_tagvalue_file(self, file_name):
        """Returns tuple error, document."""
        with open(file_name, mode='r') as infile:
            tvparser = TVParser(TVBuilder(), StandardLogger())
            tvparser.build()
            return tvparser.parse(infile.read())

    def write_tagvalue_file(self, document, file_name):
        with codecs.open(file_name, mode='w', encoding='utf-8') as out:
            tvwriter.write_document(document, out)

    def write_rdf_file(self, document, file_name):
        with open(file_name, mode='wb') as out:
            rdfwriter.write_document(document, out)

    def test_tagvalue_rdf(self):
        doc, error = self.parse_tagvalue_file('data/SPDXTagExample.tag')
        assert not error
        assert doc.validate([])
        filename = get_temp_file('.rdf')
        self.write_rdf_file(doc, filename)
        doc, error = self.parse_rdf_file(filename)
        assert not error
        assert doc.validate([])

    def test_rdf_rdf(self):
        doc, error = self.parse_rdf_file('data/SPDXRdfExample.rdf')
        assert not error
        assert doc.validate([])
        filename = get_temp_file('.rdf')
        self.write_rdf_file(doc, filename)
        doc, error = self.parse_rdf_file(filename)
        assert not error
        assert doc.validate([])

    def test_tagvalue_tagvalue(self):
        doc, error = self.parse_tagvalue_file('data/SPDXTagExample.tag')
        assert not error
        assert doc.validate([])
        filename = get_temp_file('.tag')
        self.write_tagvalue_file(doc, filename)
        doc, error = self.parse_tagvalue_file(filename)
        assert not error
        assert doc.validate([])

    def test_rdf_tagvalue(self):
        doc, error = self.parse_rdf_file('data/SPDXRdfExample.rdf')
        assert not error
        assert doc.validate([])
        filename = get_temp_file('.tag')
        self.write_tagvalue_file(doc, filename)
        doc, error = self.parse_tagvalue_file(filename)
        assert not error
        assert doc.validate([])


if __name__ == '__main__':
    unittest.main()
