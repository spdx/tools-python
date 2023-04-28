# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from spdx_tools.spdx3.validation.json_ld.shacl_validation import validate_against_shacl_from_file


def test_shacl_validation():
    some_return = validate_against_shacl_from_file(
        data_file="/home/armin/PycharmProjects/tools-python/tests/SPDX3_jsonld_test.json",
        shacl_file="/home/armin/PycharmProjects/tools-python/src/spdx_tools/spdx3/writer/json_ld/model.ttl",
    )

    print(some_return)
