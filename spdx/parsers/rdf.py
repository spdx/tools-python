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
import re
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
    'PKG_CONC_LIST': 'Package concluded license list must have more than one member',
    'PKG_MEMBER_CONC' : 'Package concluded license list member must be a license url or identifier',
    'PKG_SINGLE_LICS' : 'Package concluded license must be a license url or spdx:noassertion or spdx:none.',
    'PKG_LICS_INFO_FILES' : 'Package licenseInfoFromFiles must be a license or spdx:none or spdx:noassertion',
    'FILE_TYPE' : 'File type must be binary, other, source or archive term.',

}


class BaseParser(object):

    def __init__(self, builder, logger):
        super(BaseParser, self).__init__()
        self.logger = logger
        self.doap_namespace = Namespace('http://usefulinc.com/ns/doap#')
        self.spdx_namespace = Namespace("http://spdx.org/rdf/terms#")
        self.builder = builder

    def more_than_one_error(self, t):
        msg = 'More than one {0} defined.'.format(t)
        self.logger.log(msg)
        self.error = True

    def value_error(self, key, bad_value):
        msg = ERROR_MESSAGES[key].format(bad_value)
        self.logger.log(msg)
        self.error = True

    def to_special_value(self, value):
        """Checks if value is a special SPDX value such as 
        NONE, NOASSERTION or UNKNOWN if so returns proper model.
        else returns value"""
        if value == 'spdx:none':
            return utils.SPDXNone()
        elif value == 'spdx:noassertion':
            return utils.NoAssert()
        elif value == 'spdx:unknown':
            return utils.UnKnown()
        else:
            return value

class LicenseParser(BaseParser):
    """Helper class for parsing extracted licenses and license lists"""
    LICS_REF_REGEX = re.compile('LicenseRef-.+', re.UNICODE)
    def __init__(self, builder, logger):
        super(LicenseParser, self).__init__(builder, logger)

    def handle_lics(self, lics):
        """Takes a license resource and returns a license object."""
        ident_start = lics.rfind('/') + 1
        if ident_start == 0:
            special = self.to_special_value(lics)
            if special == lics:
                if self.LICS_REF_REGEX.match(lics):
                    return document.License.from_identifier(lics)
                else:
                    raise ValueError('License')
            else:
                return special
        else:
            return document.License.from_identifier(lics[ident_start:])

    def get_extr_license_ident(self, extr_lic):
        """Returns identifier or None if failed"""
        ident_list = list(self.graph.triples(
             (extr_lic, self.spdx_namespace['licenseId'], None)))
        if len(ident_list) > 1:
            self.more_than_one_error('extracted license identifier')
            return None
        elif len(ident_list) == 0:
            self.error = True
            msg = 'Extracted license must have licenseId property.'
            self.logger.log(msg)
            return None
        return ident_list[0][2]

    def get_extr_license_text(self, extr_lic):
        """Returns extracted text or None if failed"""
        extr_text_list = list(self.graph.triples(
            (extr_lic, self.spdx_namespace['extractedText'], None)))
        if len(extr_text_list) > 1:
            self.more_than_one_error('extracted license text')
            return None
        elif len(extr_text_list) == 0:
            self.error = True
            msg = 'Extracted license must have extractedText property'
            self.logger.log(msg)
            return None
        return extr_text_list[0][2]
                
    def get_extr_lic_name(self, extr_lic):
        """Returns extracted license name or None if failed"""
        extr_name_list = list(self.graph.triples((
            extr_lic, self.spdx_namespace['licenseName'], None)))
        if len(extr_name_list) > 1:
            self.more_than_one_error('extracted license name')
            return None
        elif len(extr_name_list) == 0:
            return None
        return self.to_special_value(extr_name_list[0][2])

    def get_extr_lics_xref(self, extr_lic):
        """Returns list of cross references"""
        xrefs =  list(self.graph.triples(
            (extr_lic, RDFS.seeAlso, None)))
        return filter(lambda xref_triple: xref_triple[2], xrefs)

    def get_extr_lics_comment(self, extr_lics):
        """Returns license comment or None if failed or none exists"""
        comment_list = list(self.graph.triples(
            (extr_lics, RDFS.comment, None)))
        if len(comment_list) > 1 :
            self.more_than_one_error('extracted license comment')
            return None
        elif len(comment_list) == 1:
            return comment_list[0][2]
        else:
            return None

    def parse_only_extr_license(self, extr_lic):
        """Returns a License object to represent a license object.
        But does not add it to the SPDXDocument model.
        Returns None if failed
        """
        ident = self.get_extr_license_ident(extr_lic)
        text = self.get_extr_license_text(extr_lic)
        comment = self.get_extr_lics_comment(extr_lic)
        xrefs = self.get_extr_lics_xref(extr_lic)
        name = self.get_extr_lic_name(extr_lic)
        if ident is None:
            return None
        else:
            license = document.ExtractedLicense(ident)
            if text is not None:
                license.text = text
            if name is not None:
                license.full_name = name
            if comment is not None:
                license.comment = comment
            license.cross_ref = xrefs
            return license


    def handle_extracted_license(self, extr_lic):
        """Builds an extracted license and returns it.
        returns None if failed.
        """
        license = self.parse_only_extr_license(extr_lic)
        self.doc.add_extr_lic(license)
        return license


    def handle_conjunctive_list(self, lics_set):
        """Returns a license representing the conjunction or None if encountered errors"""
        licenses = []
        for _, _, lics_member in self.graph.triples(
            (lics_set, self.spdx_namespace['member'], None)):
            try:
                if (lics_member, RDF.type, self.spdx_namespace['ExtractedLicensingInfo']) in self.graph:
                    lics = self.handle_extracted_license(lics_member)
                    if lics is not None:
                        licenses.append(lics)
                else:
                    licenses.append(self.handle_lics(lics_member))
            except CardinalityError:
                self.value_error('PKG_MEMBER_CONC', lics_member)
                break
        if len(licenses) > 1:
            return reduce(lambda a, b: document.LicenseConjuction(a, b), licenses)
        else:
            self.value_error('PKG_CONC_LIST', '')
            return None

    def handle_disjunctive_list(self, lics_set):
        """Returns a license representing the disjunction or None if encountered errors"""
        licenses = []
        for _, _, lics_member in self.graph.triples(
            (lics_set, self.spdx_namespace['member'], None)):
            try:
                if (lics_member, RDF.type, self.spdx_namespace['ExtractedLicensingInfo']) in self.graph:
                    lics = self.handle_extracted_license(lics_member)
                    if lics is not None:
                        licenses.append(lics)
                else:
                    licenses.append(self.handle_lics(lics_member))
            except ValueError:
                self.value_error('PKG_MEMBER_CONC', lics_member)
        if len(licenses) > 1:
            return reduce(lambda a, b: document.LicenseDisjunction(a, b), licenses)
        else:
            self.value_error('PKG_CONC_LIST', '')
            return None


class PackageParser(LicenseParser):

    """Helper class for parsing packages."""

    def __init__(self, builder, logger):
        super(PackageParser, self).__init__(builder, logger)

    def parse_package(self, p_term):
        """Parses package fields."""
        # Check there is a pacakge name
        if not (p_term, self.spdx_namespace['name'], None) in self.graph:
            self.error = True
            self.logger.log('Package must have a name.')
            # Create dummy package so that we may continue parsing the rest of
            # the package fields.
            self.builder.create_package(self.doc, 'dummy_package')
        else:
            for s, p, o in self.graph.triples((p_term, self.spdx_namespace['name'], None)):
                try:
                    self.builder.create_package(self.doc, o)
                except CardinalityError:
                    self.more_than_one_error('Package name')
                    break
        self.p_pkg_vinfo(p_term, self.spdx_namespace['versionInfo'])
        self.p_pkg_fname(p_term, self.spdx_namespace['packageFileName'])
        self.p_pkg_suppl(p_term, self.spdx_namespace['supplier'])
        self.p_pkg_originator(p_term, self.spdx_namespace['originator'])
        self.p_pkg_down_loc(p_term, self.spdx_namespace['downloadLocation'])
        self.p_pkg_homepg(p_term, self.doap_namespace['homepage'])
        self.p_pkg_chk_sum(p_term, self.spdx_namespace['checksum'])
        self.p_pkg_src_info(p_term, self.spdx_namespace['sourceInfo'])
        self.p_pkg_verif_code(p_term, self.spdx_namespace['packageVerificationCode'])
        self.p_pkg_lic_conc(p_term, self.spdx_namespace['licenseConcluded'])
        self.p_pkg_lic_decl(p_term, self.spdx_namespace['licenseDeclared'])
        self.p_pkg_lics_info_from_files(p_term, self.spdx_namespace['licenseInfoFromFiles'])
        self.p_pkg_comments_on_lics(p_term, self.spdx_namespace['licenseComments'])
        self.p_pkg_cr_text(p_term, self.spdx_namespace['copyrightText'])
        self.p_pkg_summary(p_term, self.spdx_namespace['summary'])
        self.p_pkg_descr(p_term, self.spdx_namespace['description'])

    def p_pkg_cr_text(self, p_term, predicate):
        try:
            for _, _, text in self.graph.triples(
                (p_term, predicate, None)):
                self.builder.set_pkg_cr_text(self.doc, self.to_special_value(text))
        except CardinalityError:
            self.more_than_one_error('package copyright text')

    def p_pkg_summary(self, p_term, predicate):
        try:
            for _, _, summary in self.graph.triples(
                (p_term, predicate, None)):
                self.builder.set_pkg_summary(self.doc, summary)
        except CardinalityError:
            self.more_than_one_error('package summary')

    def p_pkg_descr(self, p_term, predicate):
        try:
            for _, _, desc in self.graph.triples(
                (p_term, predicate, None)):
                self.builder.set_pkg_desc(self.doc, desc)
        except CardinalityError:
            self.more_than_one_error('package description')


    def p_pkg_comments_on_lics(self, p_term, predicate):
        for _, _, comment in self.graph.triples(
            (p_term, predicate, None)):
            try:
                self.builder.set_pkg_license_comment(self.doc, comment)
            except CardinalityError:
                self.more_than_one_error('package comments on license')
                break

    def p_pkg_lics_info_from_files(self, p_term, predicate):
        for _, _, lics in self.graph.triples(
            (p_term, predicate, None)):
            try:
                if  (lics, RDF.type,
                    self.spdx_namespace['ExtractedLicensingInfo'])  in self.graph:
                    self.builder.set_pkg_license_from_file(self.doc, 
                        self.parse_only_extr_license(lics))
                else:
                    self.builder.set_pkg_license_from_file(self.doc, self.handle_lics(lics))
            except ValueError:
                self.value_error('PKG_LICS_INFO_FILES', lics)

    def p_pkg_lic_decl(self, p_term, predicate):
        self.handle_pkg_lic(p_term, predicate, self.builder.set_pkg_license_declared)

    def handle_pkg_lic(self, p_term, predicate, builder_func):
        """Handles package lics concluded or declared."""
        try:
            for _, _, licenses in self.graph.triples(
                (p_term, predicate, None)):
                if (licenses, RDF.type, 
                    self.spdx_namespace['ConjunctiveLicenseSet']) in self.graph:
                    lics = self.handle_conjunctive_list(licenses)
                    builder_func(self.doc, lics)
                elif (licenses, RDF.type, 
                    self.spdx_namespace['DisjunctiveLicenseSet']) in self.graph:
                    lics = self.handle_disjunctive_list(licenses)
                    builder_func(self.doc, lics) 
                else:
                    try:
                        lics = self.handle_lics(licenses)
                        builder_func(self.doc, lics)
                    except ValueError:
                        self.value_error('PKG_SINGLE_LICS', licenses)
        except CardinalityError:
            self.more_than_one_error('package {0}'.format(predicate))

    def p_pkg_lic_conc(self, p_term, predicate):
        self.handle_pkg_lic(p_term, predicate, self.builder.set_pkg_licenses_concluded)

    def p_pkg_verif_code(self, p_term, predicate):
        for _,_,verifcode in self.graph.triples((p_term, predicate, None)):
            # Parse verification code
            for _, _, code in self.graph.triples((verifcode, 
                self.spdx_namespace['packageVerificationCodeValue'], None)):
                try:
                    self.builder.set_pkg_verif_code(self.doc, code)
                except CardinalityError:
                    self.more_than_one_error('package verificaton code')
                    break
            # Parse excluded file
            for _, _, filename in self.graph.triples((verifcode, 
                self.spdx_namespace['packageVerificationCodeExcludedFile'], None)):
                try:
                    self.builder.set_pkg_excl_file(self.doc, filename)
                except CardinalityError:
                    self.more_than_one_error('package verificaton code excluded file')
                    break



    def p_pkg_src_info(self, p_term, predicate):
        for _, _, o in self.graph.triples((p_term, predicate, None)):
            try:
                self.builder.set_pkg_source_info(self.doc, o)
            except CardinalityError:
                self.more_than_one_error('package source info')
                break

    def p_pkg_chk_sum(self, p_term, predicate):
        for s, p, checksum in self.graph.triples((p_term, predicate, None)):
            for _, _, value in self.graph.triples((checksum, self.spdx_namespace['checksumValue'], None)):
                try:
                    self.builder.set_pkg_chk_sum(self.doc, value)
                except CardinalityError:
                    self.more_than_one_error('Package checksum')
                    break


    def p_pkg_homepg(self, p_term, predicate):
        for s, p, o in self.graph.triples((p_term, predicate, None)):
            try:
                self.builder.set_pkg_home(self.doc, self.to_special_value(o))
            except CardinalityError:
                self.more_than_one_error('Package home page')
                break
            except ValueError:
                self.value_error('PKG_HOME_PAGE', o)                

    def p_pkg_down_loc(self, p_term, predicate):
        for s, p, o in self.graph.triples((p_term, predicate, None)):
            try:
                self.builder.set_pkg_down_location(self.doc, self.to_special_value(o))
            except CardinalityError:
                self.more_than_one_error('Package download location')
                break
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
                break
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
                break
            except ValueError:
                self.value_error('PKG_SUPPL_VALUE', o)

    def p_pkg_fname(self, p_term, predicate):
        for s, p, o in self.graph.triples((p_term, predicate, None)):
            try:
                self.builder.set_pkg_file_name(self.doc, o)
            except CardinalityError:
                self.more_than_one_error('Package file name')
                break

    def p_pkg_vinfo(self, p_term, predicate):
        for s, p, o in self.graph.triples((p_term, predicate, None)):
            try:
                self.builder.set_pkg_vers(self.doc, o)
            except CardinalityError:
                self.more_than_one_error('Package version info')
                break


class FileParser(LicenseParser):
    """Helper class for parsing files."""
    def __init__(self, builder, logger):
        super(FileParser, self).__init__(builder, logger)

    def parse_file(self, f_term):
        if not (f_term, self.spdx_namespace['fileName'], None) in self.graph:
            self.error = True
            self.logger.log('File must have a name.')
            # Dummy name to continue
            self.builder.set_file_name(self.doc, 'Dummy file')
        else:
            for _, _, name in self.graph.triples(
                (f_term, self.spdx_namespace['fileName'], None)):
                self.builder.set_file_name(self.doc, name)
        self.p_file_type(f_term, self.spdx_namespace['fileType'])
        self.p_file_chk_sum(f_term, self.spdx_namespace['checksum'])

    def p_file_type(self, f_term, predicate):
        try:
            for _, _, ftype in self.graph.triples(
                (f_term, predicate, None)):
                try:
                    if ftype.endswith('binary'):
                        ftype = 'BINARY'
                    elif ftype.endswith('source'):
                        ftype = 'SOURCE'
                    elif ftype.endswith('other'):
                        ftype = 'OTHER'
                    elif ftype.endswith('archive'):
                        ftype = 'ARCHIVE'
                    self.builder.set_file_type(self.doc, ftype)
                except ValueError:
                    self.value_error('FILE_TYPE', ftype)    
        except CardinalityError:
            self.more_than_one_error('file type')

    def p_file_chk_sum(self, f_term, predicate):
        try:
            for s, p, checksum in self.graph.triples((f_term, predicate, None)):
                for _, _, value in self.graph.triples((checksum, self.spdx_namespace['checksumValue'], None)):                   
                    self.builder.set_file_chksum(self.doc, value)
        except CardinalityError:
            self.more_than_one_error('File checksum')      

        

class Parser(PackageParser, FileParser):

    """RDF/XML file parser."""

    def __init__(self, builder, logger):
        super(Parser, self).__init__(builder, logger)

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
            self.parse_package(s)
        for s, p, o in self.graph.triples((None, self.spdx_namespace['referencesFile'], None)):
            self.parse_file(o)
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
                break
        for s, p, o in self.graph.triples((ci_term, RDFS.comment, None)):
            try:
                self.builder.set_creation_comment(self.doc, o)
            except CardinalityError:
                self.more_than_one_error('CreationInfo comment')
                break
        for s, p, o in self.graph.triples((ci_term, self.spdx_namespace['licenseListVersion'], None)):
            try:
                self.builder.set_lics_list_ver(self.doc, o)
            except CardinalityError:
                self.more_than_one_error('licenseListVersion')
                break
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
                break
        for s, p, o in self.graph.triples((doc_term, self.spdx_namespace['dataLicense'], None)):
            try:
                self.builder.set_doc_data_lic(self.doc, o)
            except ValueError:
                self.value_error('DOC_D_LICS', o)
            except CardinalityError:
                self.more_than_one_error('dataLicense')
                break
        for s, p, o in self.graph.triples((doc_term, RDFS.comment, None)):
            try:
                self.builder.set_doc_comment(self.doc, o)
            except CardinalityError:
                self.more_than_one_error('Document comment')
                break
