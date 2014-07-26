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
import tagvaluebuilders
from builderexceptions import *
from validations import validate_creator
from .. import version
from .. import document
from .. import creationinfo

class DocBuilder(object):
    VERS_STR_REGEX = re.compile(r'SPDX-(\d+)\.(\d+)', re.UNICODE)
    def __init__(self):
        super(DocBuilder, self).__init__()
        self.reset_document()

    def set_doc_version(self, doc, value):
        """Sets the document version. 
        Raises value error if malformed value, CardinalityError
        if already defined, IncompatibleVersionError if not 1.2.
        """
        if not self.doc_version_set:
            self.doc_version_set = True
            m = self.VERS_STR_REGEX.match(value)
            if m is None:
                raise ValueError('Document::Version')
            else:
                vers = version.Version(major=int(m.group(1)),
                                       minor=int(m.group(2)))
                if vers == version.Version(major=1, minor=2):
                    doc.version = vers
                    return True
                else:
                    raise IncompatibleVersionError(value)
        else:
            raise CardinalityError('Document::Version')

    def set_doc_data_lic(self, doc, res):
        """Sets the document data license. 
        Raises value error if malformed value, CardinalityError
        if already defined.
        """
        if not self.doc_data_lics_set:
            self.doc_data_lics_set = True
            res_parts = res.split('/')
            if len(res_parts) != 0:
                identifier = res_parts[-1]
                doc.data_license = document.License.from_identifier(identifier)
            else:
                raise ValueError('Document::License')
        else:
            raise CardinalityError('Document::License')

    def set_doc_comment(self, doc, comment):
        """Sets document comment, Raises CardinalityError if
        comment already set.
        """
        if not self.doc_comment_set:
            self.doc_comment_set = True
            doc.comment = comment
        else:
            raise CardinalityError('Document::Comment')


    def reset_document(self):
        """Resets the state to allow building new documents"""
        self.doc_version_set = False
        self.doc_comment_set = False
        self.doc_data_lics_set = False


class EntityBuilder(tagvaluebuilders.EntityBuilder):

    def create_entity(self, doc, value):
        if self.tool_re.match(value):
            return self.build_tool(doc, value)
        elif self.person_re.match(value):
            return self.build_person(doc, value)
        elif self.org_re.match(value):
            return self.build_org(doc, value)
        else:
            raise ValueError('Entity')


class CreationInfoBuilder(tagvaluebuilders.CreationInfoBuilder):

    def set_creation_comment(self, doc, comment):
        """Sets creation comment, Raises CardinalityError if
        comment already set.
        Raises ValueError if not free form text.
        """
        if not self.creation_comment_set:
            self.creation_comment_set = True
            doc.creation_info.comment = comment
            return True
        else:
            raise CardinalityError('CreationInfo::Comment')

class PackageBuilder(tagvaluebuilders.PackageBuilder):
    pass
        

class Builder(DocBuilder, EntityBuilder, CreationInfoBuilder, PackageBuilder):
    
    def reset(self):
        """Resets builder's state for building new documents.
        Must be called between usage with different documents.
        """
        self.reset_document()
        self.reset_package()
        self.reset_file_stat()
        self.reset_reviews()