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
from .. import creationinfo
from .. import utils

def validate_is_free_form_text(value, optional=False):
    TEXT_RE = re.compile(r'<text>(.|\n)+</text>', re.UNICODE)
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
    elif type(value) is creationinfo.Organization:
        return True
    elif type(value) is creationinfo.Person:
        return True
    elif type(value) is utils.NoAssert:
        return True
    else:
        return False

def validate_pkg_originator(value, optional=False):
    return validate_pkg_supplier(value, optional)

def validate_pkg_homepage(value, optional=False):
    if optional or value is None:
        return True
    elif type(value) is str:
        return True
    elif type(value) is utils.NoAssert:
        return True
    else:
        return False

def validate_pkg_cr_text(value, optional=False):
    assert False

def validate_pkg_summary(value, optional=False):
    return validate_is_free_form_text(value, optional)

def validate_pkg_desc(value, optional=False):
    return validate_is_free_form_text(value, optional)