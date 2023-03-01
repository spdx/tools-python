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
import pytest

from spdx.parser.tagvalue.parser.tagvalue import Parser
from tests.spdx.parser.tagvalue.test_creation_info_parser import DOCUMENT_STR


@pytest.fixture
def parser():
    spdx_parser = Parser()
    spdx_parser.build()
    return spdx_parser


def test_extracted_licensing_info(parser):
    extracted_licensing_info_str = '\n'.join([
        'LicenseID: LicenseRef-Beerware-4.2',
        'ExtractedText: <text>"THE BEER-WARE LICENSE" (Revision 42): phk@FreeBSD.ORG wrote this file. As long as you retain this notice you can do whatever you want with this stuff. If we meet some day, and you think this stuff is worth it, you can buy me a beer in return Poul-Henning Kamp</text>'
        'LicenseName: Beer-Ware License (Version 42)',
        'LicenseCrossReference:  http://people.freebsd.org/~phk/',
        'LicenseComment: The beerware license has a couple of other standard variants.'
    ])
    document = parser.parse("\n".join([DOCUMENT_STR, extracted_licensing_info_str]))
    assert document is not None
    assert len(document.extracted_licensing_info) == 1
    extracted_licensing_info = document.extracted_licensing_info[0]
    assert extracted_licensing_info.license_id == "LicenseRef-Beerware-4.2"
    assert extracted_licensing_info.extracted_text == '"THE BEER-WARE LICENSE" (Revision 42): phk@FreeBSD.ORG wrote this file. As long as you retain this notice you can do whatever you want with this stuff. If we meet some day, and you think this stuff is worth it, you can buy me a beer in return Poul-Henning Kamp'
    assert extracted_licensing_info.license_name == "Beer-Ware License (Version 42)"
    assert extracted_licensing_info.cross_references == ["http://people.freebsd.org/~phk/"]
    assert extracted_licensing_info.comment == "The beerware license has a couple of other standard variants."
