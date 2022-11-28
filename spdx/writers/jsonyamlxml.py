# Copyright (c) Xavier Figueroa
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Dict, List

from rdflib import Literal

from spdx import license, utils
from spdx.checksum import Checksum
from spdx.package import ExternalPackageRef
from spdx.relationship import Relationship
from spdx.utils import update_dict_item_with_new_item


class BaseWriter(object):
    """
    Base class for all Writer classes.
    Provide utility functions and stores shared fields.
    - document: spdx.document class. Source of data to be written
    - document_object: python dictionary representation of the entire spdx.document
    """

    def __init__(self, document):
        self.document = document
        self.document_object = dict()

    def license(self, license_field):
        """
        Return a string representation of a license or spdx.utils special object
        """
        if isinstance(
            license_field, (license.LicenseDisjunction, license.LicenseConjunction)
        ):
            return "({})".format(license_field)

        if isinstance(license_field, license.License):
            license_str = license_field.identifier.__str__()
        else:
            license_str = license_field.__str__()
        return license_str

    def checksum_to_dict(self, checksum_field: Checksum) -> Dict:
        """
        Return a dictionary representation of a checksum.Checksum object
        """
        return {'algorithm': checksum_field.identifier.name, 'checksumValue': checksum_field.value}

    def spdx_id(self, spdx_id_field):
        return spdx_id_field.__str__().split("#")[-1]


class CreationInfoWriter(BaseWriter):
    """
    Represent spdx.creationinfo as json-serializable objects
    """

    def __init__(self, document):
        super(CreationInfoWriter, self).__init__(document)

    def create_creation_info(self):
        creation_info_object = dict()
        creation_info = self.document.creation_info
        creation_info_object["creators"] = list(map(str, creation_info.creators))
        creation_info_object["created"] = creation_info.created_iso_format

        if creation_info.license_list_version:
            creation_info_object["licenseListVersion"] = "{0}.{1}".format(
                creation_info.license_list_version.major,
                creation_info.license_list_version.minor,
            )

        if creation_info.has_comment:
            creation_info_object["comment"] = creation_info.comment

        return creation_info_object


class PackageWriter(BaseWriter):
    """
    Represent spdx.package as python objects
    """

    def __init__(self, document):
        super(PackageWriter, self).__init__(document)

    def package_verification_code(self, package):
        """
        Represent the package verification code information as
        as python dictionary
        """

        package_verification_code_object = dict()

        package_verification_code_object["packageVerificationCodeValue"] = package.verif_code

        if package.verif_exc_files:
            package_verification_code_object[
                "packageVerificationCodeExcludedFiles"
            ] = package.verif_exc_files

        return package_verification_code_object

    @staticmethod
    def external_reference_as_dict(external_ref: ExternalPackageRef) -> dict:
        """
        Create a dictionary representation of the provided external reference, renaming the properties as they should
        appear in a json/yaml/xml document.
        """
        external_ref_dict = dict()
        external_ref_dict["referenceCategory"] = external_ref.category
        external_ref_dict["referenceType"] = external_ref.pkg_ext_ref_type
        external_ref_dict["referenceLocator"] = external_ref.locator
        if external_ref.comment:
            external_ref_dict["comment"] = external_ref.comment
        return external_ref_dict

    def create_package_info(self, package, annotations_by_spdx_id):
        package_object = dict()
        package_object["SPDXID"] = self.spdx_id(package.spdx_id)
        package_object["name"] = package.name
        package_object["downloadLocation"] = package.download_location.__str__()
        if package.files_analyzed is not None:
            package_object["filesAnalyzed"] = package.files_analyzed
        if package.files_analyzed is None or package.files_analyzed is True:
            if package.verif_code:
                package_object["packageVerificationCode"] = self.package_verification_code(
                    package
                )
            if package.has_optional_field("licenses_from_files"):
                package_object["licenseInfoFromFiles"] = list(
                    map(self.license, package.licenses_from_files)
                )
        if package.has_optional_field("conc_lics"):
            package_object["licenseConcluded"] = self.license(package.conc_lics)

        if package.has_optional_field("license_declared"):
            package_object["licenseDeclared"] = self.license(package.license_declared)

        if package.has_optional_field("cr_text"):
            package_object["copyrightText"] = package.cr_text.__str__()

        if package.has_optional_field("version"):
            package_object["versionInfo"] = package.version

        if package.has_optional_field("summary"):
            package_object["summary"] = package.summary

        if package.has_optional_field("attribution_text"):
            package_object["attributionTexts"] = [package.attribution_text]

        if package.has_optional_field("source_info"):
            package_object["sourceInfo"] = package.source_info

        if package.has_optional_field("file_name"):
            package_object["packageFileName"] = package.file_name

        if package.has_optional_field("supplier"):
            package_object["supplier"] = package.supplier.to_value()

        if package.has_optional_field("originator"):
            package_object["originator"] = package.originator.to_value()

        for checksum in package.checksums.values():
            package_object.setdefault("checksums", []).append(self.checksum_to_dict(checksum))

        if package.has_optional_field("description"):
            package_object["description"] = package.description

        if package.has_optional_field("comment"):
            package_object["comment"] = package.comment

        if package.has_optional_field("license_comment"):
            package_object["licenseComments"] = package.license_comment

        if package.has_optional_field("homepage"):
            package_object["homepage"] = package.homepage.__str__()

        if package.has_optional_field("primary_package_purpose"):
            package_object["primaryPackagePurpose"] = package.primary_package_purpose.name.replace("_", "-")

        if package.has_optional_field("release_date"):
            package_object["releaseDate"] = utils.datetime_iso_format(package.release_date)

        if package.has_optional_field("built_date"):
            package_object["builtDate"] = utils.datetime_iso_format(package.built_date)

        if package.has_optional_field("valid_until_date"):
            package_object["validUntilDate"] = utils.datetime_iso_format(package.valid_until_date)

        if package.has_optional_field("pkg_ext_refs"):
            package_object["externalRefs"] = [self.external_reference_as_dict(external_ref) for external_ref in
                                              package.pkg_ext_refs]
        if package.spdx_id in annotations_by_spdx_id:
            package_object["annotations"] = annotations_by_spdx_id[package.spdx_id]

        return package_object


class FileWriter(BaseWriter):
    """
    Represent spdx.file as json-serializable objects
    """

    def __init__(self, document):
        super(FileWriter, self).__init__(document)

    def create_artifact_info(self, file):
        """
        Create the artifact json-serializable representation from a spdx.file.File object
        """
        artifact_of_objects = []

        for i in range(len(file.artifact_of_project_name)):
            artifact_of_object = dict()
            artifact_of_object["name"] = file.artifact_of_project_name[i].__str__()
            artifact_of_object["homePage"] = file.artifact_of_project_home[i].__str__()
            artifact_of_object["projectUri"] = file.artifact_of_project_uri[i].__str__()
            artifact_of_objects.append(artifact_of_object)

        return artifact_of_objects

    def create_file_info(self, file, annotations_by_spdx_id):
        file_object = dict()

        file_object["fileName"] = file.name
        file_object["SPDXID"] = self.spdx_id(file.spdx_id)
        for checksum in file.checksums.values():
            file_object.setdefault("checksums", []).append(self.checksum_to_dict(checksum))
        if file.has_optional_field("conc_lics"):
            file_object["licenseConcluded"] = self.license(file.conc_lics)

        if file.has_optional_field("licenses_in_file"):
            file_object["licenseInfoInFiles"] = list(
                map(self.license, file.licenses_in_file)
            )

        if file.has_optional_field("copyright"):
            file_object["copyrightText"] = file.copyright.__str__()

        if file.has_optional_field("comment"):
            file_object["comment"] = file.comment

        if file.has_optional_field("file_types"):
            types = []
            for file_type in file.file_types:
                types.append(file_type.name)
            file_object["fileTypes"] = types

        if file.has_optional_field("license_comment"):
            file_object["licenseComments"] = file.license_comment

        if file.has_optional_field("attribution_text"):
            file_object["attributionTexts"] = [file.attribution_text]

        if file.has_optional_field("notice"):
            file_object["noticeText"] = file.notice

        if file.contributors:
            file_object["fileContributors"] = file.contributors

        if file.dependencies:
            file_object["fileDependencies"] = file.dependencies

        valid_artifacts = (
            file.artifact_of_project_name
            and len(file.artifact_of_project_name)
            == len(file.artifact_of_project_home)
            and len(file.artifact_of_project_home)
            == len(file.artifact_of_project_uri)
        )

        if valid_artifacts:
            file_object["artifactOf"] = self.create_artifact_info(file)

        if file.spdx_id in annotations_by_spdx_id:
            file_object["annotations"] = annotations_by_spdx_id[file.spdx_id]

        return file_object


class ReviewInfoWriter(BaseWriter):
    """
    Represent spdx.review as json-serializable objects
    """

    def __init__(self, document):
        super(ReviewInfoWriter, self).__init__(document)

    def create_review_info(self):
        review_info_objects = []
        reviews = self.document.reviews

        for review in reviews:
            review_object = dict()
            review_object["reviewer"] = review.reviewer.__str__()
            review_object["reviewDate"] = review.review_date_iso_format
            if review.has_comment:
                review_object["comment"] = review.comment

            review_info_objects.append(review_object)

        return review_info_objects


class AnnotationInfoWriter(BaseWriter):
    """
    Represent spdx.annotation as json-serializable objects
    """

    def __init__(self, document):
        super(AnnotationInfoWriter, self).__init__(document)

    def create_annotations_by_spdx_id(self) -> Dict:
        """
        Create a dict with annotations_by_spdx_id and use the spdx_id of the element that is annotated as key.
        These keys are then used to attach the annotation to the corresponding SPDX element.
        """
        annotations_by_spdx_id = dict()

        if not self.document.annotations:
            return annotations_by_spdx_id

        for annotation in self.document.annotations:
            annotation_object = dict()
            annotation_object["annotator"] = annotation.annotator.__str__()
            annotation_object["annotationDate"] = annotation.annotation_date_iso_format
            annotation_object["annotationType"] = annotation.annotation_type
            annotation_object["comment"] = annotation.comment

            annotation_spdx_id = self.spdx_id(annotation.spdx_id)
            if annotation_spdx_id not in annotations_by_spdx_id:
                annotations_by_spdx_id[annotation_spdx_id] = [annotation_object]
            else:
                annotations_by_spdx_id[annotation_spdx_id].append(annotation_object)

        return annotations_by_spdx_id


class RelationshipInfoWriter(BaseWriter):
    """
    Represent spdx.relationship as json-serializable objects
    """

    def __init__(self, document):
        super(RelationshipInfoWriter, self).__init__(document)

    def create_relationship_info(self, relationship: Relationship):
        relationship_object = dict()
        relationship_object["spdxElementId"] = relationship.spdx_element_id
        relationship_object[
            "relatedSpdxElement"
        ] = relationship.related_spdx_element
        relationship_object["relationshipType"] = relationship.relationship_type
        if relationship.has_comment:
            relationship_object["comment"] = relationship.relationship_comment

        return relationship_object


class SnippetWriter(BaseWriter):
    """
    Represent spdx.snippet as json-serializable objects
    """

    def __init__(self, document):
        super(SnippetWriter, self).__init__(document)

    def create_snippet_info(self, annotations_by_spdx_id):
        snippet_info_objects = []
        snippets = self.document.snippet

        for snippet in snippets:
            snippet_from_file_spdx_id = self.spdx_id(snippet.snip_from_file_spdxid)
            snippet_object = dict()
            snippet_object["SPDXID"] = self.spdx_id(snippet.spdx_id)
            snippet_object["snippetFromFile"] = snippet_from_file_spdx_id

            if snippet.has_optional_field("copyright"):
                snippet_object["copyrightText"] = snippet.copyright

            if snippet.has_optional_field("conc_lics"):
                snippet_object["licenseConcluded"] = self.license(snippet.conc_lics)

            if snippet.has_optional_field("licenses_in_snippet"):
                snippet_object["licenseInfoInSnippets"] = list(
                    map(self.license, snippet.licenses_in_snippet)
                )
            byte_range = {"endPointer": {"offset": snippet.byte_range[1], "reference": snippet_from_file_spdx_id},
                          "startPointer": {"offset": snippet.byte_range[0], "reference": snippet_from_file_spdx_id}}
            snippet_object["ranges"] = [byte_range]

            if snippet.has_optional_field("name"):
                snippet_object["name"] = snippet.name

            if snippet.has_optional_field("comment"):
                snippet_object["comment"] = snippet.comment

            if snippet.has_optional_field("attribution_text"):
                snippet_object["attributionTexts"] = [snippet.attribution_text]

            if snippet.has_optional_field("license_comment"):
                snippet_object["licenseComments"] = snippet.license_comment

            if snippet.spdx_id in annotations_by_spdx_id:
                snippet_object["annotations"] = annotations_by_spdx_id[snippet.spdx_id]

            if snippet.has_optional_field("line_range"):
                line_range = {
                    "endPointer": {"lineNumber": snippet.line_range[1], "reference": snippet_from_file_spdx_id},
                    "startPointer": {"lineNumber": snippet.line_range[0], "reference": snippet_from_file_spdx_id}}
                snippet_object["ranges"].append(line_range)

            snippet_info_objects.append(snippet_object)

        return snippet_info_objects


class ExtractedLicenseWriter(BaseWriter):
    """
    Represent spdx.document.ExtractedLicense as json-serializable objects
    """

    def __init__(self, document):
        super(ExtractedLicenseWriter, self).__init__(document)

    def create_extracted_license(self):
        extracted_license_objects = []
        unique_extracted_licenses = {}
        for lic in self.document.extracted_licenses:
            if lic.identifier not in unique_extracted_licenses.keys():
                unique_extracted_licenses[lic.identifier] = lic

        for extracted_license in unique_extracted_licenses.values():
            extracted_license_object = dict()

            if isinstance(extracted_license.identifier, Literal):
                extracted_license_object[
                    "licenseId"
                ] = extracted_license.identifier.toPython()
            else:
                extracted_license_object["licenseId"] = extracted_license.identifier

            if isinstance(extracted_license.text, Literal):
                extracted_license_object[
                    "extractedText"
                ] = extracted_license.text.toPython()
            else:
                extracted_license_object["extractedText"] = extracted_license.text

            if extracted_license.full_name:
                if isinstance(extracted_license.full_name, Literal):
                    extracted_license_object[
                        "name"
                    ] = extracted_license.full_name.toPython()
                else:
                    extracted_license_object["name"] = extracted_license.full_name

            if extracted_license.cross_ref:
                if isinstance(extracted_license.cross_ref, Literal):
                    extracted_license_object[
                        "seeAlso"
                    ] = extracted_license.cross_ref.toPython()
                else:
                    extracted_license_object["seeAlso"] = extracted_license.cross_ref

            if extracted_license.comment:
                if isinstance(extracted_license.comment, Literal):
                    extracted_license_object[
                        "comment"
                    ] = extracted_license.comment.toPython()
                else:
                    extracted_license_object["comment"] = extracted_license.comment

            extracted_license_objects.append(extracted_license_object)

        return extracted_license_objects


class Writer(
    CreationInfoWriter,
    ReviewInfoWriter,
    FileWriter,
    PackageWriter,
    AnnotationInfoWriter,
    RelationshipInfoWriter,
    SnippetWriter,
    ExtractedLicenseWriter,
):
    """
    Wrapper for the other writers.
    Represent a whole SPDX Document as json-serializable objects to then
    be written as json or yaml files.
    """

    def __init__(self, document):
        self.doc_spdx_id = self.spdx_id(document.spdx_id)
        super(Writer, self).__init__(document)

    def create_ext_document_references(self):
        """
        Create the External Document References json-serializable representation
        """
        ext_document_references_field = self.document.ext_document_references
        ext_document_reference_objects = []
        for ext_document_reference in ext_document_references_field:
            ext_document_reference_object = dict()
            ext_document_reference_object[
                "externalDocumentId"
            ] = ext_document_reference.external_document_id
            ext_document_reference_object[
                "spdxDocument"
            ] = ext_document_reference.spdx_document_uri

            ext_document_reference_object["checksum"] = self.checksum_to_dict(
                ext_document_reference.checksum
            )

            ext_document_reference_objects.append(ext_document_reference_object)

        return ext_document_reference_objects

    def create_relationships(self) -> List[Dict]:
        packages_spdx_ids = [package.spdx_id for package in self.document.packages]
        files_spdx_ids = [file.spdx_id for file in self.document.files]
        # we take the package_objects from document_object if any exist because we will modify them to add
        # jsonyamlxml-specific fields
        if "packages" in self.document_object:
            packages_by_spdx_id = {package["SPDXID"]: package for package in self.document_object["packages"]}
        else:
            packages_by_spdx_id = {}

        relationship_objects = []
        for relationship in self.document.relationships:
            if relationship.relationship_type == "CONTAINS" and relationship.spdx_element_id in packages_spdx_ids \
                    and relationship.related_spdx_element in files_spdx_ids:
                update_dict_item_with_new_item(packages_by_spdx_id[relationship.spdx_element_id], "hasFiles",
                                               relationship.related_spdx_element)
                if relationship.has_comment:
                    relationship_objects.append(self.create_relationship_info(relationship))

            elif relationship.relationship_type == "CONTAINED_BY" and relationship.spdx_element_id in files_spdx_ids \
                    and relationship.related_spdx_element in packages_spdx_ids:
                update_dict_item_with_new_item(packages_by_spdx_id[relationship.related_spdx_element],
                                                    "hasFiles", relationship.spdx_element_id)
                if relationship.has_comment:
                    relationship_objects.append(self.create_relationship_info(relationship))

            elif relationship.relationship_type == "DESCRIBES" and relationship.spdx_element_id == self.document.spdx_id:
                update_dict_item_with_new_item(self.document_object, "documentDescribes",
                                               relationship.related_spdx_element)
                if relationship.has_comment:
                    relationship_objects.append(self.create_relationship_info(relationship))

            elif relationship.relationship_type == "DESCRIBED_BY" and relationship.related_spdx_element == self.document.spdx_id:
                update_dict_item_with_new_item(self.document_object, "documentDescribes",
                                               relationship.spdx_element_id)
                if relationship.has_comment:
                    relationship_objects.append(self.create_relationship_info(relationship))

            else:
                relationship_objects.append(self.create_relationship_info(relationship))

        return relationship_objects

    def create_document(self):
        self.document_object = dict()

        self.document_object["spdxVersion"] = self.document.version.__str__()
        self.document_object["documentNamespace"] = self.document.namespace.__str__()
        self.document_object["creationInfo"] = self.create_creation_info()
        self.document_object["dataLicense"] = self.license(self.document.data_license)
        self.document_object["SPDXID"] = self.doc_spdx_id
        self.document_object["name"] = self.document.name
        annotations_by_spdx_id = self.create_annotations_by_spdx_id()

        unique_doc_packages = {}
        for doc_package in self.document.packages:
            if doc_package.spdx_id not in unique_doc_packages.keys():
                unique_doc_packages[doc_package.spdx_id] = doc_package
        if unique_doc_packages:
            package_objects = []
            for package in unique_doc_packages.values():
                package_info_object = self.create_package_info(package, annotations_by_spdx_id)
                package_objects.append(package_info_object)
            self.document_object["packages"] = package_objects
        if self.document.files:
            file_objects = []
            for file in self.document.files:
                file_object = self.create_file_info(file, annotations_by_spdx_id)
                file_objects.append(file_object)
            self.document_object["files"] = file_objects

        if self.document.has_comment:
            self.document_object["comment"] = self.document.comment

        if self.document.ext_document_references:
            self.document_object[
                "externalDocumentRefs"
            ] = self.create_ext_document_references()

        if self.document.extracted_licenses:
            self.document_object[
                "hasExtractedLicensingInfos"
            ] = self.create_extracted_license()

        if self.document.reviews:
            self.document_object["reviewers"] = self.create_review_info()

        if self.document.snippet:
            self.document_object["snippets"] = self.create_snippet_info(annotations_by_spdx_id)

        if self.doc_spdx_id in annotations_by_spdx_id:
            self.document_object["annotations"] = annotations_by_spdx_id[self.doc_spdx_id]

        if self.document.relationships:
            relationship_objects = self.create_relationships()
            if relationship_objects:
                self.document_object["relationships"] = relationship_objects

        return self.document_object
