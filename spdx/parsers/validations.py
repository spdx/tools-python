
# Copyright (c) 2014 Ahmed H. Ismail
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import re

import rdflib
import six

from spdx import creationinfo
from spdx import utils
from spdx import document


def validate_is_free_form_text(value, optional=False):
    TEXT_RE = re.compile(r'<text>(.|\n)*</text>', re.UNICODE)
    if value is None:
        return optional
    else:
        return TEXT_RE.match(value) is not None


def validate_tool_name(value, optional=False):
    striped_value = value.strip()
    if optional:
        if len(striped_value) == 0:
            return True
        else:
            return False
    else:
        return not (len(striped_value) == 0)


def validate_person_name(value, optional=False):
    return validate_tool_name(value, optional)


def validate_org_name(value, optional=False):
    return validate_tool_name(value, optional)


def validate_data_lics(value):
    return value == 'CC0-1.0'


def validate_pkg_supplier(value, optional=False):
    if optional and value is None:
        return True
    elif isinstance(value, (utils.NoAssert, creationinfo.Person, creationinfo.Organization)):
        return True
    else:
        return False


def validate_pkg_originator(value, optional=False):
    return validate_pkg_supplier(value, optional)


def validate_pkg_homepage(value, optional=False):
    if value is None:
        return optional
    elif type(value) in [six.string_types, utils.NoAssert, utils.SPDXNone]:
        return True
    else:
        return False


def validate_pkg_cr_text(value, optional=False):
    if validate_is_free_form_text(value, optional):
        return True
    elif isinstance(value, (utils.NoAssert, utils.SPDXNone)):
        return True
    elif value is None:
        return optional
    else:
        return False


def validate_pkg_summary(value, optional=False):
    return validate_is_free_form_text(value, optional)


def validate_pkg_desc(value, optional=False):
    return validate_is_free_form_text(value, optional)


def validate_doc_comment(value, optional=False):
    return validate_is_free_form_text(value, optional)


def validate_creator(value, optional=False):
    if value is None:
        return optional
    else:
        return isinstance(value, creationinfo.Creator)


def validate_creation_comment(value, optional=False):
    return validate_is_free_form_text(value, optional)


def validate_reviewer(value, optional=False):
    return validate_creator(value, optional)


def validate_review_comment(value, optional=False):
    return validate_is_free_form_text(value, optional)


def validate_pkg_src_info(value, optional=False):
    return validate_is_free_form_text(value, optional)


def validate_pkg_lics_comment(value, optional=False):
    return validate_is_free_form_text(value, optional)


def validate_file_comment(value, optional=False):
    return validate_is_free_form_text(value, optional)


def validate_file_lics_comment(value, optional=False):
    return validate_is_free_form_text(value, optional)


def validate_file_cpyright(value, optional=False):
    if validate_is_free_form_text(value, optional):
        return True
    elif isinstance(value, (utils.NoAssert, utils.SPDXNone)):
        return True
    else:
        return False


def validate_lics_from_file(value, optional=False):
    if value is None:
        return optional
    elif isinstance(value, (document.License, utils.SPDXNone, utils.NoAssert)):
        return True
    else:
        return False

def validate_file_notice(value, optional=False):
    return validate_is_free_form_text(value, optional)


def validate_lics_conc(value, optional=False):
    if value is None:
        return optional
    elif isinstance(value, (utils.NoAssert, utils.SPDXNone, document.License)):
        return True
    else:
        return False


def validate_file_lics_in_file(value, optional=False):
    if value is None:
        return optional
    elif isinstance(value, (utils.NoAssert, utils.SPDXNone, document.License)):
        return True
    else:
        return False


def validate_extracted_lic_id(value, optional=False):
    if value is None:
        return optional
    else:
        return value.startswith('LicenseRef-')


def validate_extr_lic_name(value, optional=False):
    if value is None:
        return optional
    else:
        return isinstance(value, (six.string_types, utils.NoAssert, rdflib.Literal))
