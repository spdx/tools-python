# SPDX-FileCopyrightText: 2023 spdx contributors

# SPDX-License-Identifier: Apache-2.0
from unittest import mock

import pytest

from spdx3.model.software.package import Package
from spdx3.model.software.software_purpose import SoftwarePurpose


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_correct_initialization(creation_information):
    package = Package(
        "SPDXRef-Package",
        creation_information,
        content_identifier="https://any.uri",
        package_purpose=[SoftwarePurpose.ARCHIVE, SoftwarePurpose.PATCH],
        package_version="1:23a_bc",
        download_location="https://downloadlocation",
        package_uri="https://package.uri",
        homepage="https://homepage",
    )

    assert package.spdx_id == "SPDXRef-Package"
    assert package.creation_info == creation_information
    assert package.content_identifier == "https://any.uri"
    assert package.package_purpose == [SoftwarePurpose.ARCHIVE, SoftwarePurpose.PATCH]
    assert package.package_version == "1:23a_bc"
    assert package.download_location == "https://downloadlocation"
    assert package.package_uri == "https://package.uri"
    assert package.homepage == "https://homepage"


@mock.patch("spdx3.model.creation_information.CreationInformation", autospec=True)
def test_invalid_initialization(creation_information):
    with pytest.raises(TypeError) as err:
        Package(
            "SPDXRef-Package",
            creation_information,
            content_identifier=3,
            package_purpose=SoftwarePurpose.FILE,
            package_version=42,
            download_location=4,
            package_uri=["uris"],
            homepage=True,
        )

    assert err.value.args[0] == [
        'SetterError Package: type of argument "content_identifier" must be one of '
        "(str, NoneType); got int instead: 3",
        'SetterError Package: type of argument "package_purpose" must be one of '
        "(List[spdx3.model.software.software_purpose.SoftwarePurpose], NoneType); got "
        "spdx3.model.software.software_purpose.SoftwarePurpose instead: "
        "SoftwarePurpose.FILE",
        'SetterError Package: type of argument "package_version" must be one of '
        "(str, NoneType); got int instead: 42",
        'SetterError Package: type of argument "download_location" must be one of '
        "(str, NoneType); got int instead: 4",
        'SetterError Package: type of argument "package_uri" must be one of (str, '
        "NoneType); got list instead: ['uris']",
        'SetterError Package: type of argument "homepage" must be one of (str, ' "NoneType); got bool instead: True",
    ]
