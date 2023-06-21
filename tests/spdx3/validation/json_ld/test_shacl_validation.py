# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import os

import pytest

from spdx_tools.spdx3.validation.json_ld.shacl_validation import validate_against_shacl_from_file


@pytest.mark.skip("Currently the validation against SHACL fails, refer to process.md and the known limitations.")
def test_shacl_validation():
    # insert path to example json ld
    conforms, results_graph, results_text = validate_against_shacl_from_file(
        data_file=os.path.join(os.path.dirname(__file__), "../../../SPDX3_jsonld_test.jsonld"),
        shacl_file=os.path.join(
            os.path.dirname(__file__), "../../../../src/spdx_tools/spdx3/writer/json_ld/model.ttl"
        ),
    )
    # results_graph.serialize("validation_result.rdf.xml", format="pretty-xml")
    print(results_text)
    assert conforms
