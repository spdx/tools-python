# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.jsonlikedict.extracted_licensing_info_parser import ExtractedLicensingInfoParser


def test_parse_extracted_licensing_info():
    extracted_licensing_info_parser = ExtractedLicensingInfoParser()

    extracted_licensing_infos_dict = {
        "licenseId": "LicenseRef-Beerware-4.2",
        "comment": "The beerware license has a couple of other standard variants.",
        "extractedText": '"THE BEER-WARE LICENSE" (Revision 42):\nphk@FreeBSD.ORG wrote this file. As long as you '
        "retain this notice you\ncan do whatever you want with this stuff. If we meet some day, and "
        "you think this stuff is worth it, you can buy me a beer in return Poul-Henning Kamp",
        "name": "Beer-Ware License (Version 42)",
        "seeAlsos": ["http://people.freebsd.org/~phk/"],
    }

    extracted_licensing_info = extracted_licensing_info_parser.parse_extracted_licensing_info(
        extracted_licensing_infos_dict
    )

    assert extracted_licensing_info.license_id == "LicenseRef-Beerware-4.2"
    assert extracted_licensing_info.comment == "The beerware license has a couple of other standard variants."
    assert (
        extracted_licensing_info.extracted_text
        == '"THE BEER-WARE LICENSE" (Revision 42):\nphk@FreeBSD.ORG wrote this file. As long as you retain this '
        "notice you\ncan do whatever you want with this stuff. If we meet some day, and you think this stuff is "
        "worth it, you can buy me a beer in return Poul-Henning Kamp"
    )
    assert extracted_licensing_info.license_name == "Beer-Ware License (Version 42)"
    assert extracted_licensing_info.cross_references == ["http://people.freebsd.org/~phk/"]


def test_parse_invalid_extracted_licensing_info():
    extracted_licensing_info_parser = ExtractedLicensingInfoParser()

    extracted_licensing_infos_dict = {
        "licenseId": "LicenseRef-Beerware-4.2",
        "comment": 56,
        "extractedText": '"THE BEER-WARE LICENSE" (Revision 42):\nphk@FreeBSD.ORG wrote this file. As long as you '
        "retain this notice you\ncan do whatever you want with this stuff. If we meet some day, and "
        "you think this stuff is worth it, you can buy me a beer in return Poul-Henning Kamp",
        "name": "Beer-Ware License (Version 42)",
        "seeAlsos": ["http://people.freebsd.org/~phk/"],
    }

    with pytest.raises(SPDXParsingError):
        extracted_licensing_info_parser.parse_extracted_licensing_info(extracted_licensing_infos_dict)
