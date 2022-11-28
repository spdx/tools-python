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

import datetime
import hashlib
import re
from typing import Dict, List, TYPE_CHECKING

from ply import lex
from ply import yacc

from spdx.checksum import ChecksumAlgorithm

if TYPE_CHECKING:
    from spdx.file import File
    from spdx.package import Package
from spdx.relationship import Relationship
from spdx import license


def datetime_iso_format(date):
    """
    Return an ISO-8601 representation of a datetime object.
    """
    return date.isoformat() + "Z"


# Matches an iso 8601 date representation
DATE_ISO_REGEX = re.compile(
    r"(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)Z", re.UNICODE
)

# Groups for retrieving values from DATE_ISO_REGEX matches.
DATE_ISO_YEAR_GRP = 1
DATE_ISO_MONTH_GRP = 2
DATE_ISO_DAY_GRP = 3
DATE_ISO_HOUR_GRP = 4
DATE_ISO_MIN_GRP = 5
DATE_ISO_SEC_GRP = 6


def datetime_from_iso_format(string):
    """
    Return a datetime object from an iso 8601 representation.
    Return None if string is non conforming.
    """
    match = DATE_ISO_REGEX.match(string)
    if match:
        date = datetime.datetime(
            year=int(match.group(DATE_ISO_YEAR_GRP)),
            month=int(match.group(DATE_ISO_MONTH_GRP)),
            day=int(match.group(DATE_ISO_DAY_GRP)),
            hour=int(match.group(DATE_ISO_HOUR_GRP)),
            second=int(match.group(DATE_ISO_SEC_GRP)),
            minute=int(match.group(DATE_ISO_MIN_GRP)),
        )
        return date
    else:
        return None


class NoAssert(object):
    """
    Represent SPDX NOASSERTION value.
    """

    def to_value(self):
        return "NOASSERTION"

    def __str__(self):
        return self.to_value()

    def __repr__(self):
        return self.to_value()


class UnKnown(object):
    """
    Represent SPDX UNKNOWN value.
    """

    def to_value(self):
        return "UNKNOWN"

    def __str__(self):
        return self.to_value()

    def __repr__(self):
        return self.to_value()

    def __eq__(self, other):
        return self.to_value() == other.to_value()


class SPDXNone(object):
    """
    Represent SPDX None value.
    """

    def to_value(self):
        return "NONE"

    def __str__(self):
        return self.to_value()


class LicenseListLexer(object):
    tokens = ["LP", "RP", "AND", "OR", "LICENSE"]

    def t_LP(self, t):
        r"\("
        return t

    def t_RP(self, t):
        r"\)"
        return t

    def t_AND(self, t):
        r"\s(and|AND)\s"
        t.value = t.value.strip()
        return t

    def t_OR(self, t):
        r"\s(or|OR)\s"
        t.value = t.value.strip()
        return t

    def t_whitespace(self, t):
        r"\s+"
        pass

    def t_LICENSE(self, t):
        r"[A-Za-z.0-9\-+]+"
        t.value = t.value.strip()
        return t

    def t_error(self, t):
        pass

    def input(self, data):
        """Set input, data - str."""
        self.lexer.input(data)

    def token(self):
        """Get the next token or None if exhausted input."""
        return self.lexer.token()

    def build(self, **kwargs):
        """Build lexer, must be called before input or token methods.
        Only need to build once.
        """
        self.lexer = lex.lex(module=self, **kwargs)


class LicenseListParser(object):
    def __init__(self):
        self.lex = LicenseListLexer()
        self.lex.build(reflags=re.UNICODE)
        self.tokens = self.lex.tokens

    def p_disjunction_1(self, p):
        """disjunction : disjunction OR conjunction
        """
        p[0] = license.LicenseDisjunction(p[1], p[3])

    def p_disjunction_2(self, p):
        """disjunction : conjunction
        """
        p[0] = p[1]

    def p_conjunction_1(self, p):
        """conjunction : conjunction AND license_atom
        """
        p[0] = license.LicenseConjunction(p[1], p[3])

    def p_conjunction_2(self, p):
        """conjunction : license_atom
        """
        p[0] = p[1]

    def p_license_atom_1(self, p):
        """license_atom : LICENSE
        """
        p[0] = license.License.from_identifier(p[1])

    def p_license_atom_2(self, p):
        """license_atom : LP disjunction RP
        """
        p[0] = p[2]

    def p_error(self, p):
        pass

    def build(self, **kwargs):
        """Must be called before parse."""
        self.yacc = yacc.yacc(module=self, **kwargs)

    def parse(self, data):
        """Parses a license list and returns a License or None if it failed."""
        try:
            return self.yacc.parse(data, lexer=self.lex)
        except:
            return None


def calc_verif_code(files: List['File']) -> str:
    list_of_file_hashes = []
    hash_algorithm_name = ChecksumAlgorithm.SHA1
    for file in files:
        file_checksum = file.get_checksum(hash_algorithm_name)
        if file_checksum is not None:
            file_checksum_value = file_checksum.value
        else:
            file_checksum_value = file.calculate_checksum(hash_algorithm_name)
        list_of_file_hashes.append(file_checksum_value)

    list_of_file_hashes.sort()

    hasher = hashlib.new(hash_algorithm_name.name.lower())
    hasher.update("".join(list_of_file_hashes).encode("utf-8"))
    return hasher.hexdigest()


def get_files_in_package(package: 'Package', files: List['File'], relationships: List[Relationship]) -> List['File']:
    files_in_package = []
    for file in files:
        if file.spdx_id in [relationship.related_spdx_element for relationship in relationships
                            if relationship.relationship_type == "CONTAINS" and relationship.spdx_element_id == package.spdx_id] \
            or file.spdx_id in [relationship.spdx_element_id for relationship in relationships
                                if relationship.relationship_type == "CONTAINED_BY" and relationship.related_spdx_element == package.spdx_id]:
            files_in_package.append(file)

    return files_in_package


def update_dict_item_with_new_item(current_state: Dict, key: str, item_to_add: str) -> None:
    if key not in current_state:
        current_state[key] = [item_to_add]
    elif item_to_add not in current_state[key]:
        current_state[key].append(item_to_add)
