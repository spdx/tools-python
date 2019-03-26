from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import json
import six
import re

from spdx import utils
from spdx import document
from spdx.parsers.builderexceptions import CardinalityError
from spdx.parsers.builderexceptions import SPDXValueError
from spdx.parsers import rdf, tagvalue
from spdx.parsers.json_builders import Builder
from spdx.parsers.loggers import StandardLogger

ERROR_MESSAGES = tagvalue.ERROR_MESSAGES


def get_free_form_text(string):
    """Wraps the input string in a <text></text> tag."""
    if string is not None:
        return "<text>{}</text>".format(string)


class BaseParser(rdf.BaseParser):
    """
    Base class for all parsers.
    Contains logger, doap_namespace, spdx_namespace and model builder.
    Also provides utility functions used by the deriving parsers.
    """

    def __init__(self, builder, logger):
        self.logger = logger
        self.builder = builder

    def to_special_value(self, value):
        """Checks if value is a special SPDX value such as
        NONE, NOASSERTION or UNKNOWN if so returns proper model.
        else returns value"""
        if value is None or value == "None":
            return utils.SPDXNone()
        elif "no_assertion" in value:
            return utils.NoAssert()
        elif "unknown" in value:
            return utils.UnKnown()
        else:
            return value


class AnnotationParser(BaseParser):
    """
    Helper class for parsing annotation information.
    """

    def __init__(self, builder, logger):
        super(AnnotationParser, self).__init__(builder, logger)

    def parse_annotation(self, annotations):
        # getting annotations in a list format if there is only one annotation defined in the file.
        list_annotations = self.get_list_annotations(annotations)

        for annotation in list_annotations:
            # annotator is the person who has created that annotation.
            annotator = self.get_annotator(annotation)

            annotation_date = self.get_annotation_date(annotation)

            # todo: raise a valueError in else part. as there has to be an annotator
            if annotator is not None:
                self.builder.add_annotator(self.doc, annotator)
                if annotation_date is not None:
                    try:
                        self.builder.add_annotation_date(self.doc, annotation_date)
                    except SPDXValueError:
                        self.value_error('ANNOTATION_DATE', annotation_date)

            annotation_type = self.get_annotation_type(annotation)
            if annotation_type is not None:
                self.builder.add_annotation_type(self.doc, annotation_type)

            comment = self.get_annotation_comment(annotation)
            if comment is not None:
                self.builder.add_annotation_comment(self.doc, comment)
            elif annotation_type is not None:
                # as per documentation of Annotation class, annotation type must have comment.
                self.value_error("ANNOTATION_COMMENT", comment)
                raise SPDXValueError("Annotation::AnnotationComment")
            try:
                self.builder.set_annotation_spdx_id(self.doc, annotation)
            except CardinalityError:
                self.more_than_one_error('SPDX Identifier Reference')

    @staticmethod
    def get_list_annotations(annotation_obj):
        """This checks if the annotation_obj is a list or
        just a single instance of annotation so that it can return list of it"""
        if isinstance(annotation_obj, list):
            return annotation_obj
        elif isinstance(annotation_obj, dict):
            return [annotation_obj]

    def get_annotation_type(self, annotation):
        """Returns annotation type or None if found none or more than one.
        Reports errors on failure."""
        try:
            type_annotation = annotation["annotationType"]
            return type_annotation
        except KeyError:
            self.error = True
            msg = 'Annotation must have exactly one annotation type.'
            self.logger.log(msg)

    def get_annotation_comment(self, annotation):
        """Returns annotation comment or None if found none or more than one.
        Reports errors.
        """
        comment = annotation["comment"]
        if isinstance(comment, list):
            self.error = True
            msg = 'Annotation can have at most one comment.'
            self.logger.log(msg)
            return
        else:
            if comment is not None:
                return get_free_form_text(six.text_type(comment))
            else:
                return None

    def get_annotation_date(self, annotation):
        """Returns annotation date or None if not found.
        Reports error on failure.
        Note does not check value format.
        """
        annotation_date = annotation['annotationDate']
        if isinstance(annotation_date, list):
            self.error = True
            msg = 'Annotation must have exactly one annotation date.'
            self.logger.log(msg)
            return
        return six.text_type(annotation_date)
        pass

    def get_annotator(self, annotation):
        """Returns annotator as creator object or None if failed.
        Reports errors on failure.
        """
        annotator = annotation["annotator"]
        if isinstance(annotator, list):
            self.error = True
            msg = 'Annotation must have exactly one annotator'
            return
        try:
            return self.builder.create_entity(self.doc, six.text_type(annotator))
        except SPDXValueError:
            self.value_error('ANNOTATOR_VALUE', annotator)
            self.logger.log("=" * 100)
        self.logger.log("=" * 100)
        pass


class ReviewParser(BaseParser):
    """
    Helper class for parsing review information.
    """

    def __init__(self, builder, logger):
        super(ReviewParser, self).__init__(builder, logger)

    def parse_reviewers(self, reviewers):
        """
        - reviewers : string data
        """
        for reviewer_string in reviewers:
            reviewer = self.get_reviewer(reviewer_string)
            reviewed_date = self.get_review_date(reviewer_string)
            if reviewer is not None:
                self.builder.add_reviewer(self.doc, reviewer)
                if reviewed_date is not None:
                    try:
                        self.builder.add_review_date(self.doc, reviewed_date)
                    except SPDXValueError:
                        self.value_error('REVIEW_DATE', reviewed_date)
                comment = self.get_review_comment(reviewer_string)
                if comment is not None:
                    self.builder.add_review_comment(self.doc, comment)

    def get_review_comment(self, reviewer_string):
        """Returns review comment or None if found none or more than one.
        Reports errors.
        """
        comment = reviewer_string["comment"]
        if isinstance(comment, list):
            self.error = True
            msg = 'Review can have at most one comment'
            self.logger.log(msg)
            return
        else:
            return get_free_form_text(six.text_type(comment))

    def get_review_date(self, reviewer_string):
        """Returns review date or None if not found.
        Reports error on failure.
        Note does not check value format.
        """
        reviewed_date = reviewer_string['reviewDate']
        if isinstance(reviewed_date, list):
            self.error = True
            msg = 'Review must have exactlyone review date'
            self.logger.log(msg)
            return
        return six.text_type(reviewed_date)

    def get_reviewer(self, reviewer_string):
        """Returns reviewer as creator object or None if failed.
        Reports errors on failure.
        """
        reviewer = reviewer_string['reviewer']
        if isinstance(reviewer, list):
            self.error = True
            msg = 'Review must have exactly one reviewer'
            self.logger.log(msg)
            return
        try:
            return self.builder.create_entity(self.doc, six.text_type(reviewer))
        except SPDXValueError:
            self.value_error('REVIEWER_VALUE', reviewer)


class CreationInfoParser(BaseParser):

    def __init__(self, builder, logger):
        super(CreationInfoParser, self).__init__(builder, logger)

    def parse_creation_info(self, creation_info):
        creator_list = creation_info.get("creators")
        for creator_string in creator_list:
            creator = self.get_creator(creator_string)
            self.builder.add_creator(self.doc, creator)
        comment = self.get_comment(creation_info.get("comment"))
        self.builder.set_creation_comment(self.doc, comment)
        created_ts = creation_info.get("created")
        self.builder.set_created_date(self.doc, created_ts)
        license_list_version = creation_info.get("licenseListVersion")
        self.builder.set_lics_list_ver(self.doc, license_list_version)

    def get_comment(self, comment_string):
        return get_free_form_text(comment_string)

    def get_creator(self, creator_string):
        return self.builder.create_entity(self.doc, creator_string)


class LicenseParser(BaseParser):
    """
    Helper class for parsing extracted licenses and license lists.
    """

    LICS_REF_REGEX = re.compile('LicenseRef-.+', re.UNICODE)

    def __init__(self, builder, logger):
        super(LicenseParser, self).__init__(builder, logger)

    def parse_extracted_licenses(self, extracted_lic_info):
        for ext_license in extracted_lic_info:
            license_id = self.get_extr_license_id(ext_license)
            lic_comment = self.get_extr_lics_comment(ext_license)
            lic_see_alsos = self.get_extr_lics_see_also(ext_license)
            lic_name = self.get_extr_lic_name(ext_license)
            lic_text = self.get_extr_license_text(ext_license)

            lic = document.ExtractedLicense(license_id)
            if lic_text is not None:
                lic.text = lic_text
            if lic_name is not None:
                lic.full_name = lic_name
            if lic_comment is not None:
                lic.comment = lic_comment
            lic.cross_ref = lic_see_alsos
            self.doc.add_extr_lic(lic)

    def get_extr_license_id(self, extr_lic):
        """
        Return an a license id from an ExtractedLicense or None.
        """
        license_id = extr_lic.get('licenseId')

        if not license_id:
            self.error = True
            msg = 'Extracted license must have licenseId property.'
            self.logger.log(msg)
            return

        if isinstance(license_id, list):
            self.more_than_one_error('extracted license identifier_tripples')
            return

        return license_id

    def get_extr_license_text(self, extr_lic):
        """
        Return extracted text  from an ExtractedLicense or None.
        """
        extr_text = extr_lic.get("extractedText")
        if extr_text is None:
            self.error = True
            msg = 'Extracted license must have extractedText property'
            self.logger.log(msg)
            return

        if isinstance(extr_text, list):
            self.more_than_one_error('extracted license text')
            return

        return extr_text

    def get_extr_lic_name(self, extr_lic):
        """
        Return the license name from an ExtractedLicense or None
        """
        extr_name = extr_lic.get("name")
        if isinstance(extr_name, list):
            self.more_than_one_error('extracted license name')
            return
        elif extr_name is None:
            return
        return self.to_special_value(extr_name)

    def get_extr_lics_see_also(self, extr_lic):
        """
        Return a list of cross references.
        """
        xrefs = extr_lic.get("seeAlso")
        if isinstance(xrefs, list):
            return [six.text_type(xref) for xref in xrefs]
        elif isinstance(xrefs, str):
            return [six.text_type(xrefs)]
        else:
            return []

    def get_extr_lics_comment(self, extr_lic):
        """
        Return license comment or None.
        """
        comment = extr_lic.get("comment")
        if isinstance(comment, list):
            self.more_than_one_error('extracted license comment')
            return
        elif comment is not None:
            return get_free_form_text(comment)
        else:
            return


class LooseFieldsParser(BaseParser):
    def __init__(self, builder, logger):
        super(LooseFieldsParser, self).__init__(builder, logger)

    def parse_loose_fields(self, data):
        version = data["specVersion"]
        name = data['name']
        data_license = data["dataLicense"]
        doc_id = data["id"]
        doc_comment = data.get("comment")

        self.builder.set_doc_version(self.doc, version)
        self.builder.set_doc_name(self.doc, name)
        self.builder.set_doc_data_lic(self.doc, data_license)
        self.builder.set_doc_spdx_id(self.doc, doc_id)
        self.builder.set_doc_comment(self.doc, doc_comment)


class DocDescribesParser(BaseParser):
    def __init__(self, builder, logger):
        super(DocDescribesParser, self).__init__(builder, logger)

    def get_field_from_dict(self, list_dict, field):
        for _dict in list_dict:
            try:
                return _dict[field]
            except KeyError:
                pass

    def parse_doc_describes(self, data_describes):
        file = self.get_field_from_dict(data_describes, "File")
        package = self.get_field_from_dict(data_describes, "Package")
        self.parse_package(package)
        self.parse_single_file(file)

    def parse_single_file(self, file_obj):
        project_type_mapping = {
            "projectUri": "uri",
            "projectHome": "home",
            "projectName": "name",
            "uri": "uri",
            "name": "name",
            "homePage": "home"
        }
        file_name = file_obj.get("name")
        file_comment = get_free_form_text(file_obj.get("comment"))
        file_id = file_obj.get("id")
        file_notice = get_free_form_text(file_obj.get('noticeText'))
        file_copyright = get_free_form_text(file_obj.get("copyright"))
        file_contributors = file_obj.get("fileContributors")
        file_dependencies = file_obj.get("fileDependencies")
        file_license_comment = file_obj.get("licenseComments")
        concluded_license = file_obj.get('licenseConcluded')
        file_checksums = file_obj.get("checksums")
        file_types = file_obj.get("fileTypes")
        file_artifacts = file_obj.get("artifactOf")
        file_licenses = file_obj.get("licenseInfoFromFiles")

        if file_name is not None:
            self.builder.set_file_name(self.doc, file_name)
        if file_comment is not None:
            self.builder.set_file_comment(self.doc, file_comment)
        if file_id is not None:
            self.builder.set_file_spdx_id(self.doc, file_id)
        if file_notice is not None:
            self.builder.set_file_notice(self.doc, file_notice)
        if file_copyright is not None:
            self.builder.set_file_copyright(self.doc, file_copyright)
        if file_license_comment is not None:
            self.builder.set_file_license_comment(self.doc, get_free_form_text(file_license_comment))
        if concluded_license is not None:
            self.builder.set_concluded_license(self.doc, document.License.from_full_name(concluded_license))

        for contributor in file_contributors or []:
            self.builder.add_file_contribution(self.doc, contributor)
        for dependency in file_dependencies or []:
            self.builder.add_file_dep(self.doc, dependency)
        for checksum_obj in file_checksums or []:
            if "sha1" in checksum_obj["algorithm"].lower():
                self.builder.set_file_chksum(self.doc, checksum_obj)
        for file_type in file_types or []:
            self.builder.set_file_type(self.doc, file_type)
        for artifact in file_artifacts or []:
            for artifact_key in artifact or []:
                self.builder.set_file_atrificat_of_project(self.doc, project_type_mapping[artifact_key],
                                                           artifact[artifact_key])
        for file_license in file_licenses or []:
            self.builder.set_file_license_in_file(self.doc, document.License.from_identifier(file_license))

    def parse_package(self, package):
        self.builder.create_package(self.doc, package["name"])
        self.builder.set_pkg_originator(self.doc, self.get_originator(package))
        self.builder.set_pkg_down_location(self.doc, package["downloadLocation"])
        self.builder.set_pkg_verif_code(self.doc, package["packageVerificationCode"])
        self.builder.set_pkg_summary(self.doc, package['summary'])
        self.builder.set_pkg_home(self.doc, package["homepage"])
        self.builder.set_pkg_source_info(self.doc, package["sourceInfo"])
        self.builder.set_pkg_license_comment(self.doc, package["comment"])
        self.builder.set_pkg_vers(self.doc, package["versionInfo"])
        self.builder.set_pkg_supplier(self.doc, self.builder.create_entity(self.doc, package["supplier"]))
        for file in package["files"]:
            self.parse_single_file(file["File"])

    def get_sha1_chksum(self, checksums):
        # getting only sha1 checksum because, package.py uses sha1 checksum.
        for checksum in checksums:
            if checksum["algorithm"].endswith("sha1"):
                return checksum

    def get_originator(self, package):
        originator = package["originator"]
        if originator is not None:
            return self.builder.create_entity(self.doc, originator)


class ExternalDocRefsParser(BaseParser):
    def __init__(self, builder, logger):
        super(ExternalDocRefsParser, self).__init__(builder, logger)

    def parse_external_doc_refs(self, external_doc_refs):
        for external_doc_ref in external_doc_refs:
            self.builder.add_ext_doc_refs(self.doc, external_doc_ref["externalDocumentId"],
                                          external_doc_ref["spdxDocumentNamespace"], external_doc_ref["checksum"])


class Parser(AnnotationParser, ReviewParser, CreationInfoParser, LooseFieldsParser, DocDescribesParser,
             ExternalDocRefsParser, LicenseParser):
    def __init__(self, builder, logger):
        super(Parser, self).__init__(builder, logger)

    def parse(self, fil):
        """Parses a file and returns a document object.
        File, a file like object.
        """
        self.error = False
        self.doc = document.Document()
        self.parse_annotation(data["annotations"])
        self.parse_reviewers(data["reviewers"])
        self.parse_creation_info(data["creationInfo"])
        self.parse_loose_fields(data)
        self.parse_doc_describes(data["documentDescribes"])
        self.parse_external_doc_refs(data["externalDocumentRefs"])
        self.parse_extracted_licenses(data['extractedLicenseInfos'])
        return self.doc, self.error


if __name__ == "__main__":
    with open("../../data/SPDXRdfExample.json") as json_file:
        # sample implementation of json file from data folder.
        data = json.loads(json_file.read())["Document"]

        a = Parser(Builder(), StandardLogger())
        document, error = a.parse(data)
