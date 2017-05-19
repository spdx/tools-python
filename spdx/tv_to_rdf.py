#!/usr/bin/env python
# Copyright (C) 2017 BMW AG
#               Author: Thomas Hafner

#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import sys
import codecs
from spdx.parsers.tagvalue import Parser
from spdx.parsers.loggers import StandardLogger
from spdx.parsers.tagvaluebuilders import Builder
from spdx.writers.rdf import write_document

def tv_to_rdf(infile_name, outfile_name):
    """Converts a SPDX file from tag/value format to RDF format."""
    parser = Parser(Builder(), StandardLogger())
    parser.build()
    with open(infile_name) as infile:
        data = infile.read()
        document, error = parser.parse(data)
        if not error:
            with open(outfile_name, mode='w') as outfile:
                write_document(document, outfile)
        else:
            print 'Errors encountered while parsing RDF file.'
            messages = []
            document.validate(messages)
            print '\n'.join(messages)

if __name__ == '__main__':
    tv_to_rdf(*sys.argv[1:])
