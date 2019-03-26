from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from spdx import checksum
from spdx.parsers.builderexceptions import CardinalityError
from spdx.parsers.builderexceptions import OrderError
from spdx.parsers.builderexceptions import SPDXValueError
from spdx.parsers import tagvaluebuilders
from spdx.parsers import validations
from spdx.parsers import rdfbuilders
from spdx import file


def checksum_from_sha1(checksum_obj):
    """
    Return an spdx.checksum.Algorithm instance representing the SHA1
    checksum or None if does not ends with sha1.
    """
    match = checksum_obj["algorithm"].endswith("sha1")
    if match:
        return checksum.Algorithm(identifier='SHA1', value=checksum_obj["value"])
    else:
        return None


# defining separate class to have space for addition of new functionality and error handling.
class CreationInfoBuilder(tagvaluebuilders.CreationInfoBuilder):
    pass


class ReviewBuilder(tagvaluebuilders.ReviewBuilder):
    pass


class LicenseBuilder(tagvaluebuilders.LicenseBuilder):
    pass


class DocBuilder(rdfbuilders.DocBuilder):
    pass


class EntityBuilder(rdfbuilders.EntityBuilder):
    pass


class PackageBuilder(rdfbuilders.PackageBuilder):
    pass


class ExternalDocumentRefBuilder(rdfbuilders.ExternalDocumentRefBuilder):
    def set_spdx_doc_namespace(self, doc, spdx_doc_namespace):
        """
        Sets the `spdx_document_uri` attribute of the `ExternalDocumentRef`
        object.
        """
        if validations.validate_doc_namespace(spdx_doc_namespace):
            doc.ext_document_references[-1].spdx_document_uri = spdx_doc_namespace
        else:
            raise SPDXValueError('Document::ExternalDocumentRef')


class FileBuilder(tagvaluebuilders.FileBuilder):

    def __init__(self):
        self.reset_file_stat()

    def set_file_type(self, doc, type_value):
        """
        Raises OrderError if no package or file defined.
        Raises CardinalityError if more than one type set.
        Raises SPDXValueError if type is unknown.
        """
        type_dict = {
            'fileType_source': file.FileType.SOURCE,
            'fileType_binary': file.FileType.BINARY,
            'fileType_archive': file.FileType.ARCHIVE,
            'fileType_other': file.FileType.OTHER
        }
        # for adding a file, there should already be a package set.
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_type_set:
                self.file_type_set = True
                if type_value in type_dict.keys():
                    self.file(doc).type = type_dict[type_value]
                    return True
                else:
                    raise SPDXValueError('File::Type')
            else:
                # There was already a file set earlier.
                raise CardinalityError('File::Type')
        else:
            raise OrderError('File::Type')

    def set_file_chksum(self, doc, chksum):
        """
        Raises OrderError if no package or file defined.
        Raises CardinalityError if more than one chksum set.
        """
        if self.has_package(doc) and self.has_file(doc):
            if not self.file_chksum_set:
                self.file_chksum_set = True
                self.file(doc).chk_sum = checksum_from_sha1(chksum)
                return True
            else:
                raise CardinalityError('File::CheckSum')
        else:
            raise OrderError('File::CheckSum')


class AnnotationBuilder(tagvaluebuilders.AnnotationBuilder):

    def __init__(self):
        super(AnnotationBuilder, self).__init__()

    def add_annotation_comment(self, doc, comment):
        """Sets the annotation comment. Raises CardinalityError if
        already set. OrderError if no annotator defined before.
        """
        if len(doc.annotations) != 0:
            if not self.annotation_comment_set:
                self.annotation_comment_set = True
                doc.annotations[-1].comment = comment
                return True
            else:
                raise CardinalityError('AnnotationComment')
        else:
            raise OrderError('AnnotationComment')

    def add_annotation_type(self, doc, annotation_type):
        """Sets the annotation type. Raises CardinalityError if
        already set. OrderError if no annotator defined before.
        """
        if len(doc.annotations) != 0:
            if not self.annotation_type_set:
                if annotation_type == "OTHER":
                    self.annotation_type_set = True
                    doc.annotations[-1].annotation_type = annotation_type
                    return True
                elif annotation_type == "REVIEW":
                    self.annotation_type_set = True
                    doc.annotations[-1].annotation_type = annotation_type
                    return True
                else:
                    raise SPDXValueError('Annotation::AnnotationType')
            else:
                raise CardinalityError('Annotation::AnnotationType')
        else:
            raise OrderError('Annotation::AnnotationType')


class Builder(DocBuilder, EntityBuilder, CreationInfoBuilder, PackageBuilder,
              FileBuilder, ReviewBuilder, ExternalDocumentRefBuilder,
              AnnotationBuilder, LicenseBuilder, tagvaluebuilders.PackageBuilder):

    def __init__(self):
        super(Builder, self).__init__()
        self.reset()

    def reset(self):
        """Resets builder's state for building new documents.
        Must be called between usage with different documents.
        """
        self.reset_creation_info()
        self.reset_document()
        self.reset_package()
        self.reset_file_stat()
        self.reset_reviews()
        self.reset_annotations()
