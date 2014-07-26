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
from .. import utils


ERROR_MESSAGES = {
    'DOC_VERS_VALUE': 'Invalid specVersion \'{0}\' must be SPDX-M.N where M and N are numbers.',
    'DOC_D_LICS': 'Invalid dataLicense \'{0}\' must be http://spdx.org/licenses/CC0-1.0.',
    'LL_VALUE': 'Invalid licenseListVersion \'{0}\' must be of the format N.N where N is a number',
    'CREATED_VALUE': 'Invalid created value \'{0}\' must be date in ISO 8601 format.',
    'CREATOR_VALUE': 'Invalid creator value \'{0}\' must be Organization, Tool or Person.',
    'PKG_SUPPL_VALUE': 'Invalid package supplier value \'{0}\' must be Organization, Person or NOASSERTION.',
    'PKG_ORIGINATOR_VALUE': 'Invalid package supplier value \'{0}\'  must be Organization, Person or NOASSERTION.',
    'PKG_DOWN_LOC': 'Invalid package download location value \'{0}\'  must be a url or NONE or NOASSERTION',

}


class BaseParser(object):

    def __init__(self, logger):
        super(BaseParser, self).__init__()
        self.logger = logger

    def more_than_one_error(self, t):
        msg = 'More than one {0} defined.'.format(t)
        self.logger.log(msg)
        self.error = True

    def value_error(self, key, bad_value):
        msg = ERROR_MESSAGES[key].format(bad_value)
        self.logger.log(msg)
        self.error = True


class PackageParser(BaseParser):

    """Helper class for parsing packages."""

    def __init__(self, builder, logger):
        super(PackageParser, self).__init__(logger)
        self.builder = builder

    def parse_package(self, p_term, spdx_namespace):
        """Parses package fields."""
        # Check there is a pacakge name
        if not (p_term, spdx_namespace['name'], None) in self.graph:
            self.error = True
            self.logger.log('Package must have a name.')
            # Create dummy package so that we may continue parsing the rest of
            # the package fields.
            self.builder.create_package(self.doc, 'dummy_package')
        else:
            for s, p, o in self.graph.triples((p_term, spdx_namespace['name'], None)):
                try:
                    self.builder.create_package(self.doc, o)
                except CardinalityError:
                    self.more_than_one_error('Package name')
        self.p_pkg_vinfo(p_term, spdx_namespace['versionInfo'])
        self.p_pkg_fname(p_term, spdx_namespace['packageFileName'])
        self.p_pkg_suppl(p_term, spdx_namespace['supplier'])
        self.p_pkg_originator(p_term, spdx_namespace['originator'])
        self.p_pkg_down_loc(p_term, spdx_namespace['downloadLocation'])

    def p_pkg_down_loc(self, p_term, predicate):
        for s, p, o in self.graph.triples((p_term, predicate, None)):
            try:
                if o == 'NONE':
                    self.builder.set_pkg_down_location(
                        self.doc, utils.SPDXNone())
                elif o == 'NOASSERTION':
                    self.builder.set_pkg_down_location(
                        self.doc, utils.NoAssert())
                else:
                    self.builder.set_pkg_down_location(self.doc, o)
                break
            except CardinalityError:
                self.more_than_one_error('Package download location')
            except ValueError:
                self.value_error('PKG_DOWN_LOC', o)

    def p_pkg_originator(self, p_term, predicate):
        for s, p, o in self.graph.triples((p_term, predicate, None)):
            try:
                if o == "NOASSERTION":
                    self.builder.set_pkg_originator(self.doc, utils.NoAssert())
                else:
                    ent = self.builder.create_entity(self.doc, o)
                    self.builder.set_pkg_originator(self.doc, ent)
            except CardinalityError:
                self.more_than_one_error('Package originator')
            except ValueError:
                self.value_error('PKG_ORIGINATOR_VALUE', o)

    def p_pkg_suppl(self, p_term, predicate):
        for s, p, o in self.graph.triples((p_term, predicate, None)):
            try:
                if o == "NOASSERTION":
                    self.builder.set_pkg_supplier(self.doc, utils.NoAssert())
                else:
                    ent = self.builder.create_entity(self.doc, o)
                    self.builder.set_pkg_supplier(self.doc, ent)
            except CardinalityError:
                self.more_than_one_error('Package supplier')
            except ValueError:
                self.value_error('PKG_SUPPL_VALUE', o)

    def p_pkg_fname(self, p_term, predicate):
        for s, p, o in self.graph.triples((p_term, predicate, None)):
            try:
                self.builder.set_pkg_file_name(self.doc, o)
            except CardinalityError:
                self.more_than_one_error('Package file name')

    def p_pkg_vinfo(self, p_term, predicate):
        for s, p, o in self.graph.triples((p_term, predicate, None)):
            try:
                self.builder.set_pkg_vers(self.doc, o)
            except CardinalityError:
                self.more_than_one_error('Package version info')


class Parser(PackageParser):

    """RDF/XML file parser."""

    def __init__(self, builder, logger):
        super(Parser, self).__init__(builder, logger)
        self.spdx_namespace = Namespace("http://spdx.org/rdf/terms#")

    def parse(self, file):
        """Parses a file and returns a document object.
        File, a file like object.
        """
        self.error = False
        self.graph = Graph()
        self.graph.parse(file=file, format='xml')
        self.doc = document.Document()
        for s, p, o in self.graph.triples((None, RDF.type, self.spdx_namespace['SpdxDocument'])):
            self.parse_doc_fields(s)
        for s, p, o in self.graph.triples((None, RDF.type, self.spdx_namespace['CreationInfo'])):
            self.parse_creation_info(s)
        for s, p, o in self.graph.triples((None, RDF.type, self.spdx_namespace['Package'])):
            self.parse_package(s, self.spdx_namespace)
        return self.doc, self.error

    def parse_creation_info(self, ci_term):
        """Parses creators, creater and comment."""
        for s, p, o in self.graph.triples((ci_term, self.spdx_namespace['creator'], None)):
            try:
                ent = self.builder.create_entity(self.doc, o)
                self.builder.add_creator(self.doc, ent)
            except ValueError:
                self.value_error('CREATOR_VALUE', o)
        for s, p, o in self.graph.triples((ci_term, self.spdx_namespace['created'], None)):
            try:
                self.builder.set_created_date(self.doc, o)
            except ValueError:
                self.value_error('CREATED_VALUE', o)
            except CardinalityError:
                self.more_than_one_error('created')
        for s, p, o in self.graph.triples((ci_term, RDFS.comment, None)):
            try:
                self.builder.set_creation_comment(self.doc, o)
            except CardinalityError:
                self.more_than_one_error('CreationInfo comment')
        for s, p, o in self.graph.triples((ci_term, self.spdx_namespace['licenseListVersion'], None)):
            try:
                self.builder.set_lics_list_ver(self.doc, o)
            except CardinalityError:
                self.more_than_one_error('licenseListVersion')
            except ValueError:
                self.value_error('LL_VALUE', o)

    def parse_doc_fields(self, doc_term):
        """Parses the version, data license and comment."""
        for s, p, o in self.graph.triples((doc_term, self.spdx_namespace['specVersion'], None)):
            try:
                self.builder.set_doc_version(self.doc, o)
            except ValueError:
                self.value_error('DOC_VERS_VALUE', o)
            except CardinalityError:
                self.more_than_one_error('specVersion')
        for s, p, o in self.graph.triples((doc_term, self.spdx_namespace['dataLicense'], None)):
            try:
                self.builder.set_doc_data_lic(self.doc, o)
            except ValueError:
                self.value_error('DOC_D_LICS', o)
            except CardinalityError:
                self.more_than_one_error('dataLicense')
        for s, p, o in self.graph.triples((doc_term, RDFS.comment, None)):
            try:
                self.builder.set_doc_comment(self.doc, o)
            except CardinalityError:
                self.more_than_one_error('Document comment')
