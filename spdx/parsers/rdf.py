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
from rdflib import Graph, Namespace, RDF, RDFS
from builderexceptions import *
from .. import document


ERROR_MESSAGES = {
    'DOC_VERS_VALUE' : 'Invalid specVersion \'{0}\' must be SPDX-M.N where M and N are numbers.',
    'DOC_D_LICS' : 'Invalid dataLicense \'{0}\' must be http://spdx.org/licenses/CC0-1.0.',
}



class Parser(object):
    """docstring for Parser"""
    def __init__(self, builder, logger):
        super(Parser, self).__init__()
        self.spdx_namespace = Namespace("http://spdx.org/rdf/terms#")
        self.builder = builder
        self.logger = logger

    def parse(self, file):
        """Parses a file and returns a document object.
        File, a file like object.
        """
        self.error = False
        self.graph = Graph()
        self.graph.parse(file=file, format='xml')
        self.doc = document.Document()
        for s, p, o in self.graph.triples( (None, RDF.type, self.spdx_namespace['SpdxDocument']) ):
            self.parse_doc_fields(s)
        for s, p, o in self.graph.triples( (None, RDF.type, self.spdx_namespace['CreationInfo']) ):
            self.parse_creation_info(s)
        return self.doc, self.error

    def parse_creation_info(self, ci_term):
        """Parses creators, creater and comment."""
        for s, p, o in self.graph.triples( (ci_term, self.spdx_namespace['creator'], None) ):
            try:
                ent = self.builder.create_entity(self.doc, o)
                self.builder.add_creator(self.doc, ent)
            except ValueError:
                msg = ERROR_MESSAGES['CREATOR_VALUE'].format(o)
                self.logger.log(msg)
                self.error = True
        for s, p, o in self.graph.triples( (ci_term, self.spdx_namespace['created'], None) ):
            try:
                self.builder.set_created_date(self.doc, o)
            except ValueError:
                msg = ERROR_MESSAGES['CREATED_VALUE'].format(o)
                self.logger.log(msg)
                self.error = True
            except CardinalityError:
                self.more_than_one_error('created')
        for s, p, o in self.graph.triples( (ci_term, RDFS.comment, None) ):
            try:
                self.builder.set_creation_comment(self.doc, o)
            except CardinalityError:
                self.more_than_one_error('CreationInfo comment')



    def parse_doc_fields(self, doc_term):
        """Parses the version, data license and comment."""
        for s, p, o in self.graph.triples( (doc_term, self.spdx_namespace['specVersion'], None) ):
            try:
                self.builder.set_doc_version(self.doc, o)
            except ValueError:
                msg = ERROR_MESSAGES['DOC_VERS_VALUE'].format(o)
                self.logger.log(msg)
                self.error = True
            except CardinalityError:
                self.more_than_one_error('specVersion')
        for s, p, o in self.graph.triples( (doc_term, self.spdx_namespace['dataLicense'], None) ):
            try:
                self.builder.set_doc_data_lic(self.doc, o)
            except ValueError:
                msg = ERROR_MESSAGES['DOC_D_LICS'].format(o)
                self.logger.log(msg)
                self.error = True
            except CardinalityError:
                self.more_than_one_error('dataLicense')
        for s, p, o in self.graph.triples( (doc_term, RDFS.comment, None) ):
            try:
                self.builder.set_doc_comment(self.doc, o)
            except CardinalityError:
                self.more_than_one_error('Document comment')



    def more_than_one_error(self, t):
        msg = 'More than one {0} defined.'.format(t)
        self.logger.log(msg)
        self.error = True