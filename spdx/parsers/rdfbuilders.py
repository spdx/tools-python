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
from builderexceptions import *
from .. import version
from .. import document

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

class Builder(DocBuilder):
    pass