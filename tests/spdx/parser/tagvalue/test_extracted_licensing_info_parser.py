# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from unittest import TestCase

import pytest

from spdx.parser.error import SPDXParsingError
from spdx.parser.tagvalue.parser import Parser
from tests.spdx.parser.tagvalue.test_creation_info_parser import DOCUMENT_STR


def test_parse_extracted_licensing_info():
    parser = Parser()
    extracted_licensing_info_str = "\n".join([
        "LicenseID: LicenseRef-Beerware-4.2",
        "ExtractedText: <text>\"THE BEER-WARE LICENSE\" (Revision 42): phk@FreeBSD.ORG wrote this file. As long as you "
        "retain this notice you can do whatever you want with this stuff. If we meet some day, and you think this "
        "stuff is worth it, you can buy me a beer in return Poul-Henning Kamp</text>"
        "LicenseName: Beer-Ware License (Version 42)",
        "LicenseCrossReference:  http://people.freebsd.org/~phk/",
        "LicenseCrossReference:  http://another.cross.reference/",
        "LicenseComment: The beerware license has a couple of other standard variants."
    ])
    document = parser.parse("\n".join([DOCUMENT_STR, extracted_licensing_info_str]))
    assert document is not None
    assert len(document.extracted_licensing_info) == 1
    extracted_licensing_info = document.extracted_licensing_info[0]
    assert extracted_licensing_info.license_id == "LicenseRef-Beerware-4.2"
    assert extracted_licensing_info.extracted_text == "\"THE BEER-WARE LICENSE\" (Revision 42): phk@FreeBSD.ORG wrote this file. " \
                                                      "As long as you retain this notice you can do whatever you want with this stuff. " \
                                                      "If we meet some day, and you think this stuff is worth it, you can buy me a beer in return Poul-Henning Kamp"
    assert extracted_licensing_info.license_name == "Beer-Ware License (Version 42)"
    TestCase().assertCountEqual(extracted_licensing_info.cross_references,
                                ["http://people.freebsd.org/~phk/", "http://another.cross.reference/"])
    assert extracted_licensing_info.comment == "The beerware license has a couple of other standard variants."


def test_parse_invalid_extracted_licensing_info():
    parser = Parser()
    extracted_licensing_info_str = "\n".join([
        "ExtractedText: <text>\"THE BEER-WARE LICENSE\" (Revision 42): phk@FreeBSD.ORG wrote this file. "
        "As long as you retain this notice you can do whatever you want with this stuff. If we meet some day, and you "
        "think this stuff is worth it, you can buy me a beer in return Poul-Henning Kamp</text>",
        "LicenseName: Beer-Ware License (Version 42)",
        "LicenseCrossReference:  http://people.freebsd.org/~phk/",
        "LicenseComment: The beerware license has a couple of other standard variants."])

    with pytest.raises(SPDXParsingError) as err:
        parser.parse(extracted_licensing_info_str)

    assert err.value.get_messages() == ["Element ExtractedLicensingInfo is not the current element in scope, probably "
                                        "the expected tag to start the element (LicenseID) is missing. Line: 1",
                                        "Element ExtractedLicensingInfo is not the current element in scope, probably "
                                        "the expected tag to start the element (LicenseID) is missing. Line: 2",
                                        "Element ExtractedLicensingInfo is not the current element in scope, probably "
                                        "the expected tag to start the element (LicenseID) is missing. Line: 3",
                                        "Element ExtractedLicensingInfo is not the current element in scope, probably "
                                        "the expected tag to start the element (LicenseID) is missing. Line: 4"]
