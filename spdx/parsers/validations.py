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
