from unittest import TestCase

import pytest

from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.jsonlikedict.package_parser import PackageParser


# To avoid duplication we use this invalid package as a proxy for the exact comparison of the generated error message.
# For all other classes we only check that a TypeError is raised if an incorrect type is specified.
def test_error_message():
    package_parser = PackageParser()
    package = {"SPDXID": "SPDXRef-Package", "downloadLocation": 5, "attributionTexts": ["text", 5, {"test": "data"}]}

    with pytest.raises(SPDXParsingError) as err:
        package_parser.parse_package(package)

    TestCase().assertCountEqual(
        err.value.get_messages(),
        [
            'Error while constructing Package: [\'SetterError Package: argument "name" '
            "(None) is not an instance of str', 'SetterError Package: argument "
            '"download_location" (int) did not match any element in the union:\\n  str: '
            "is not an instance of str\\n  "
            "spdx_tools.spdx.model.spdx_no_assertion.SpdxNoAssertion: is not an instance "
            "of spdx_tools.spdx.model.spdx_no_assertion.SpdxNoAssertion\\n  "
            "spdx_tools.spdx.model.spdx_none.SpdxNone: is not an instance of "
            "spdx_tools.spdx.model.spdx_none.SpdxNone', 'SetterError Package: item 1 of "
            'argument "attribution_texts" (list) is not an instance of str\']'
        ],
    )
