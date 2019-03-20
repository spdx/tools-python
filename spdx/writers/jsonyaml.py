from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from spdx import document
from rdflib import Literal

class BaseWriter(object):
    """
    Base class for all Writer classes.
    Provides utility functions and stores shared fields.
    - document: spdx.document class. Source of data to be written
    - document_object: python dictionary representation of the entire spdx.document
    """

    def __init__(self, document):
        self.document = document
        self.document_object = dict()

    def license(self, license_field):
        """
        Returns a string representation of a license or spdx.utils special object
        """
        if isinstance(license_field, document.License):
            return str(license_field.identifier)
        return license_field.__str__()

    def checksum(self, checksum_field):
        """
        Returns a dictionary representation of a spdx.checksum.Algorithm object
        """
        checksum_object = dict()
        checksum_object['algorithm'] = checksum_field.identifier
        checksum_object['value'] = checksum_field.value
        return checksum_object

class CreationInfoWriter(BaseWriter):
    """
    Responsible for representing spdx.creationinfo as json-serializable objects
    """

    def __init__(self, document):
        super(CreationInfoWriter, self).__init__(document)

    def create_creation_info(self):
        creation_info_object = dict()
        creation_info = self.document.creation_info
        creation_info_object['creators'] = map(str, creation_info.creators)
        creation_info_object['created'] = creation_info.created_iso_format

        if creation_info.license_list_version:
            creation_info_object['licenseListVersion'] = creation_info.license_list_version.__str__()

        if creation_info.has_comment:
            creation_info_object['comment'] = creation_info.comment

        return creation_info_object

class PackageWriter(BaseWriter):
    """
    Responsible for representing spdx.package as python objects
    """

    def __init__(self, document):
        super(PackageWriter, self).__init__(document)

    def package_verification_code(self, package):
        """
        Represents the package verification code information as 
        as python dictionary
        """

        package_verification_code_object = dict()

        package_verification_code_object['value'] = package.verif_code

        if package.verif_exc_files:
            package_verification_code_object['excludedFilesNames'] = package.verif_exc_files
        
        return package_verification_code_object

    def create_package_info(self):
        package_object = dict()
        package = self.document.package
        package_object['name'] = package.name
        package_object['id'] = "pseudoID " + package.name # Mandatory field but there's not in package class
        package_object['downloadLocation'] = package.download_location
        package_object['packageVerificationCode'] = self.package_verification_code(package)
        package_object['licenseConcluded'] = self.license(package.conc_lics)
        package_object['licenseInfoFromFiles'] = map(self.license, package.licenses_from_files)
        package_object['licenseDeclared'] = self.license(package.license_declared)
        package_object['copyrightText'] = package.cr_text.__str__()

        if package.has_optional_field('version'):
            package_object['versionInfo'] = package.version

        if package.has_optional_field('summary'):
            package_object['summary'] = package.summary

        if package.has_optional_field('source_info'):
            package_object['sourceInfo'] = package.source_info

        if package.has_optional_field('file_name'):
            package_object['packageFileName'] = package.file_name

        if package.has_optional_field('supplier'):
            package_object['supplier'] = package.supplier.__str__()

        if package.has_optional_field('originator'):
            package_object['originator'] = package.originator.__str__()

        if package.has_optional_field('check_sum'):
            package_object['checksums'] = self.checksum(package.check_sum)
            package_object['sha1'] = package.check_sum.value

        if package.has_optional_field('description'):
            package_object['description'] = package.description

        if package.has_optional_field('license_comment'):
            package_object['licenseComments'] = package.license_comment

        if package.has_optional_field('homepage'):
            package_object['homepage'] = package.homepage.__str__()

        return package_object

class FileWriter(BaseWriter):
    """
    Responsible for representing spdx.file as json-serializable objects
    """

    def __init__(self, document):
        super(FileWriter, self).__init__(document)

    def create_artifact_info(self, file):
        """
        Creates the artifact json-serializable representation from a spdx.file.File object
        """
        artifact_of_objects = []

        for i in range(len(file.artifact_of_project_name)):
            artifact_of_object = dict()
            artifact_of_object['name'] = file.artifact_of_project_name[i].__str__()
            artifact_of_object['homePage'] = file.artifact_of_project_home[i].__str__()
            artifact_of_object['projectUri'] = file.artifact_of_project_uri[i].__str__()
            artifact_of_objects.append(artifact_of_object)

        return artifact_of_objects

    def create_file_info(self):
        file_types = { 1: 'SOURCE', 2: 'BINARY', 3: 'ARCHIVE', 4: 'OTHER'}
        file_objects = []
        files = self.document.files

        for file in files:
            file_object = dict()

            file_object['name'] = file.name
            file_object['id'] = str(file.spdx_id)
            file_object['checksums'] = [self.checksum(file.chk_sum)]
            file_object['licenseConcluded'] = self.license(file.conc_lics)
            file_object['licenseInfoFromFiles'] = map(self.license, file.licenses_in_file)
            file_object['copyrightText'] = file.copyright.__str__()
            file_object['sha1'] = file.chk_sum.value

            if file.has_optional_field('comment'):
                file_object['comment'] = file.comment

            if file.has_optional_field('type'):
                file_object['fileTypes'] = [file_types.get(file.type, 'OTHER')]

            if file.has_optional_field('license_comment'):
                file_object['licenseComments'] = file.license_comment

            if file.has_optional_field('notice'):
                file_object['noticeText'] = file.notice

            if file.contributors:
                file_object['fileContributors'] = file.contributors

            if file.dependencies:
                file_object['fileDependencies'] = file.dependencies

            valid_artifacts = file.artifact_of_project_name and len(file.artifact_of_project_name) == len(file.artifact_of_project_home) and len(file.artifact_of_project_home) == len(file.artifact_of_project_uri)

            if valid_artifacts:
                file_object['artifactOf'] = self.create_artifact_info(file)

            file_objects.append(file_object)

        return file_objects

class ReviewInfoWriter(BaseWriter):
    """
    Responsible for representing spdx.review as json-serializable objects
    """

    def __init__(self, document):
        super(ReviewInfoWriter, self).__init__(document)

    def create_review_info(self):
        review_info_objects = []
        reviews = self.document.reviews

        for review in reviews:
            review_object = dict()
            review_object['reviewer'] = review.reviewer.__str__()
            review_object['reviewDate'] = review.review_date_iso_format
            if review.has_comment:
                review_object['comment'] = review.comment

            review_info_objects.append(review_object)

        return review_info_objects

class AnnotationInfoWriter(BaseWriter):
    """
    Responsible for representing spdx.annotation as json-serializable objects
    """

    def __init__(self, document):
        super(AnnotationInfoWriter, self).__init__(document)

    def create_annotation_info(self):
        """
        The way how tools-python manages its models makes difficult to classify
        annotations (by document, files and packages) and some of them could end up omitted.
        This method sets every annotation as part of the spdx document itself, 
        avoiding them to be omitted.
        """
        annotation_objects = []

        for annotation in self.document.annotations:
            annotation_object = dict()
            annotation_object['id'] = self.spdx_id(annotation.spdx_id)
            annotation_object['annotator'] = annotation.annotator.__str__()
            annotation_object['annotationDate'] = annotation.annotation_date_iso_format
            annotation_object['annotationType'] = annotation.annotation_type
            annotation_object['comment'] = annotation.comment

            annotation_objects.append(annotation_object)

        return annotation_objects


class ExtractedLicenseWriter(BaseWriter):
    """
    Responsible for representing spdx.document.ExtractedLicense as json-serializable objects
    """

    def __init__(self, document):
        super(ExtractedLicenseWriter, self).__init__(document)

    def create_extracted_license(self):
        extracted_license_objects = []
        extracted_licenses = self.document.extracted_licenses
        
        for extracted_license in extracted_licenses:
            extracted_license_object = dict()

            if isinstance(extracted_license.identifier, Literal):
                extracted_license_object['licenseId'] = extracted_license.identifier.n3()
            else:
                extracted_license_object['licenseId'] = extracted_license.identifier

            if isinstance(extracted_license.text, Literal):
                extracted_license_object['extractedText'] = extracted_license.text.n3()
            else:
                extracted_license_object['extractedText'] = extracted_license.text

            if extracted_license.full_name:
                if isinstance(extracted_license.full_name, Literal):
                    extracted_license_object['name'] = extracted_license.full_name.n3()
                else:
                    extracted_license_object['name'] = extracted_license.full_name
            
            if extracted_license.cross_ref:
                if isinstance(extracted_license.cross_ref, Literal):
                    extracted_license_object['seeAlso'] = extracted_license.cross_ref.n3()
                else:
                    extracted_license_object['seeAlso'] = extracted_license.cross_ref

            if extracted_license.comment:
                if isinstance(extracted_license.comment, Literal):
                    extracted_license_object['comment'] = extracted_license.comment.n3()
                else:
                    extracted_license_object['comment'] = extracted_license.comment

            extracted_license_objects.append(extracted_license_object)

        return extracted_license_objects

class Writer(CreationInfoWriter, ReviewInfoWriter, FileWriter, PackageWriter, 
    AnnotationInfoWriter, ExtractedLicenseWriter):
    """
    Wrapper for the other writers.
    Responsible for representing a whole SPDX Document as json-serializable objects to then
    be written as json or yaml files.
    """

    def __init__(self, document):
        super(Writer, self).__init__(document)

    def create_ext_document_references(self):
        """
        Creates the External Document References json-serializable representation
        """
        ext_document_references_field = self.document.ext_document_references
        ext_document_reference_objects = []
        for ext_document_reference in ext_document_references_field:
            ext_document_reference_object = dict()
            ext_document_reference_object['externalDocumentId'] = ext_document_reference.external_document_id
            ext_document_reference_object['spdxDocumentNamespace'] = ext_document_reference.spdx_document_uri

            ext_document_reference_object['checksum'] = self.checksum(ext_document_reference.check_sum)

            ext_document_reference_objects.append(ext_document_reference_object)

        return ext_document_reference_objects

    def create_document(self):
    	self.document_object = dict()

        self.document_object['specVersion'] = self.document.version.__str__()
        self.document_object['spdxVersion'] = self.document.version.__str__()
        self.document_object['creationInfo'] = self.create_creation_info()
        self.document_object['datalicense'] = self.license(self.document.data_license)
        self.document_object['id'] = str(self.document.spdx_id)
        self.document_object['name'] = self.document.name

        package_info_object = self.create_package_info()
        package_info_object['files'] = self.create_file_info()

        self.document_object['documentDescribes'] = [{'Package': package_info_object}]

        if self.document.has_comment:
            self.document_object['comment'] = self.document.comment

        if self.document.ext_document_references:
            self.document_object['externalDocumentRefs'] = self.create_ext_document_references()

        if self.document.extracted_licenses:
            self.document_object['extractedLicenseInfos'] = self.create_extracted_license()

        if self.document.reviews:
            self.document_object['reviewers'] = self.create_review_info()
        
        if self.document.snippet:
            self.document_object['snippets'] = self.create_snippet_info()
        
        if self.document.annotations:
            self.document_object['annotations'] = self.create_annotation_info()

        return {'Document' : self.document_object}