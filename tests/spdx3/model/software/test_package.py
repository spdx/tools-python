# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from unittest import mock

import pytest

from spdx3.model.software.software_purpose import SoftwarePurpose

from spdx3.model.software.package import Package


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_correct_initialization_package(creation_information):
    package = Package("SPDXRef-Package", creation_information, content_identifier="https://any.uri",
                      package_purpose=[SoftwarePurpose.ARCHIVE, SoftwarePurpose.PATCH],
                      download_location="https://downloadlocation", package_uri="https://package.uri",
                      homepage="https://homepage")

    assert package.spdx_id == "SPDXRef-Package"
    assert package.creation_info == creation_information
    assert package.content_identifier == "https://any.uri"
    assert package.package_purpose == [SoftwarePurpose.ARCHIVE, SoftwarePurpose.PATCH]
    assert package.download_location == "https://downloadlocation"
    assert package.package_uri == "https://package.uri"
    assert package.homepage == "https://homepage"


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_invalid_initialization_package(creation_information):
    with pytest.raises(TypeError) as err:
        Package("SPDXRef-Package", creation_information, content_identifier=3, package_purpose=SoftwarePurpose.FILE,
                download_location=4, package_uri=["uris"], homepage=True)

    assert err.value.args[0] == ['SetterError Package: type of argument "content_identifier" must be one of '
                                 '(str, NoneType); got int instead: 3',
                                 'SetterError Package: type of argument "package_purpose" must be one of '
                                 '(List[spdx3.model.software.software_purpose.SoftwarePurpose], NoneType); got '
                                 'spdx3.model.software.software_purpose.SoftwarePurpose instead: '
                                 'SoftwarePurpose.FILE',
                                 'SetterError Package: type of argument "download_location" must be one of '
                                 '(str, NoneType); got int instead: 4',
                                 'SetterError Package: type of argument "package_uri" must be one of (str, '
                                 "NoneType); got list instead: ['uris']",
                                 'SetterError Package: type of argument "homepage" must be one of (str, '
                                 'NoneType); got bool instead: True']
