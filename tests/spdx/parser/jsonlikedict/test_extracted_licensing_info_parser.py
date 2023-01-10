# Copyright (c) 2022 spdx contributors
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
from spdx.parser.jsonlikedict.extracted_licensing_info_parser import ExtractedLicensingInfoParser


def test_parse_extracted_licensing_info():
    extracted_licensing_info_parser = ExtractedLicensingInfoParser()

    extracted_licensing_infos_dict = {

        "licenseId": "LicenseRef-Beerware-4.2",
        "comment": "The beerware license has a couple of other standard variants.",
        "extractedText": "\"THE BEER-WARE LICENSE\" (Revision 42):\nphk@FreeBSD.ORG wrote this file. As long as you retain this notice you\ncan do whatever you want with this stuff. If we meet some day, and you think this stuff is worth it, you can buy me a beer in return Poul-Henning Kamp",
        "name": "Beer-Ware License (Version 42)",
        "seeAlsos": ["http://people.freebsd.org/~phk/"]

    }

    extracted_licensing_info = extracted_licensing_info_parser.parse_extracted_licensing_info(
        extracted_licensing_infos_dict)

    assert extracted_licensing_info.license_id == "LicenseRef-Beerware-4.2"
    assert extracted_licensing_info.comment == "The beerware license has a couple of other standard variants."
    assert extracted_licensing_info.extracted_text == "\"THE BEER-WARE LICENSE\" (Revision 42):\nphk@FreeBSD.ORG wrote this file. As long as you retain this notice you\ncan do whatever you want with this stuff. If we meet some day, and you think this stuff is worth it, you can buy me a beer in return Poul-Henning Kamp"
    assert extracted_licensing_info.license_name == "Beer-Ware License (Version 42)"
    assert extracted_licensing_info.cross_references == ["http://people.freebsd.org/~phk/"]


def test_parse_invalid_extracted_licensing_info():
    extracted_licensing_info_parser = ExtractedLicensingInfoParser()

    extracted_licensing_infos_dict = {
        "licenseId": "LicenseRef-Beerware-4.2",
        "comment": 56,
        "extractedText": "\"THE BEER-WARE LICENSE\" (Revision 42):\nphk@FreeBSD.ORG wrote this file. As long as you retain this notice you\ncan do whatever you want with this stuff. If we meet some day, and you think this stuff is worth it, you can buy me a beer in return Poul-Henning Kamp",
        "name": "Beer-Ware License (Version 42)",
        "seeAlsos": ["http://people.freebsd.org/~phk/"]

    }

    with pytest.raises(SPDXParsingError) as err:
        extracted_licensing_info_parser.parse_extracted_licensing_info(extracted_licensing_infos_dict)

    TestCase().assertCountEqual(err.value.get_messages(), [
        "Error while constructing ExtractedLicensingInfo: ['SetterError " 'ExtractedLicensingInfo: type of argument "comment" must be one of (str, ' "NoneType); got int instead: 56']"])

