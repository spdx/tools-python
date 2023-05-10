# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from datetime import datetime
from unittest import mock

import pytest

from spdx_tools.spdx3.model.software import Package, SoftwarePurpose


@mock.patch("spdx_tools.spdx3.model.CreationInformation", autospec=True)
def test_correct_initialization(creation_information):
    package = Package(
        "SPDXRef-Package",
        creation_information,
        "Test package",
        content_identifier="https://any.uri",
        originated_by=["https://namespace.test#originator"],
        supplied_by=["https://namespace.test#supplier"],
        built_time=datetime(2022, 1, 1),
        release_time=datetime(2022, 1, 2),
        valid_until_time=datetime(2022, 1, 3),
        standard=["ISO"],
        purpose=[SoftwarePurpose.ARCHIVE, SoftwarePurpose.PATCH],
        package_version="1:23a_bc",
        download_location="https://downloadlocation",
        package_url="https://package.uri",
        homepage="https://homepage",
        source_info="some info",
    )

    assert package.spdx_id == "SPDXRef-Package"
    assert package.creation_info == creation_information
    assert package.name == "Test package"
    assert package.content_identifier == "https://any.uri"
    assert package.originated_by == ["https://namespace.test#originator"]
    assert package.supplied_by == ["https://namespace.test#supplier"]
    assert package.built_time == datetime(2022, 1, 1)
    assert package.release_time == datetime(2022, 1, 2)
    assert package.valid_until_time == datetime(2022, 1, 3)
    assert package.standard == ["ISO"]
    assert package.purpose == [SoftwarePurpose.ARCHIVE, SoftwarePurpose.PATCH]
    assert package.package_version == "1:23a_bc"
    assert package.download_location == "https://downloadlocation"
    assert package.package_url == "https://package.uri"
    assert package.homepage == "https://homepage"
    assert package.source_info == "some info"


@mock.patch("spdx_tools.spdx3.model.CreationInformation", autospec=True)
def test_invalid_initialization(creation_information):
    with pytest.raises(TypeError) as err:
        Package(
            "SPDXRef-Package",
            creation_information,
            "Test package",
            built_time="2022-03-04T00:00:00Z",
            content_identifier=3,
            purpose=SoftwarePurpose.FILE,
            package_version=42,
            download_location=4,
            package_url=["uris"],
            homepage=True,
            source_info=["some info"],
        )

    assert err.value.args[0] == [
        'SetterError Package: type of argument "built_time" must be one of '
        "(datetime.datetime, NoneType); got str instead: 2022-03-04T00:00:00Z",
        'SetterError Package: type of argument "content_identifier" must be one of '
        "(str, NoneType); got int instead: 3",
        'SetterError Package: type of argument "purpose" must be a list; got '
        "spdx_tools.spdx3.model.software.software_purpose.SoftwarePurpose instead: "
        "SoftwarePurpose.FILE",
        'SetterError Package: type of argument "package_version" must be one of '
        "(str, NoneType); got int instead: 42",
        'SetterError Package: type of argument "download_location" must be one of '
        "(str, NoneType); got int instead: 4",
        'SetterError Package: type of argument "package_url" must be one of (str, '
        "NoneType); got list instead: ['uris']",
        'SetterError Package: type of argument "homepage" must be one of (str, ' "NoneType); got bool instead: True",
        'SetterError Package: type of argument "source_info" must be one of (str, '
        "NoneType); got list instead: ['some info']",
    ]
