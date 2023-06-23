# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import os

import pytest
from click.testing import CliRunner

from spdx_tools.spdx.clitools.pyspdxtools import main


@pytest.mark.parametrize(
    "options",
    [
        ("--infile", os.path.join(os.path.dirname(__file__), "data/SPDXJSONExample-v2.3.spdx.json")),
        ("-i", os.path.join(os.path.dirname(__file__), "data/SPDXJSONExample-v2.3.spdx.json"), "--novalidation"),
        (
            "-i",
            os.path.join(os.path.dirname(__file__), "data/SPDXJSONExample-v2.3.spdx.json"),
            "--novalidation",
            "--version",
            "SPDX-2.3",
        ),
        ("-i", os.path.join(os.path.dirname(__file__), "data/SPDXJSONExample-v2.3.spdx.json"), "-o", "-"),
    ],
)
def test_cli_with_system_exit_code_0(options):
    runner = CliRunner()

    result = runner.invoke(main, options)

    assert result.exit_code == 0


@pytest.mark.parametrize(
    "options",
    [
        (),
        ("-i", os.path.join(os.path.dirname(__file__), "data/SPDXJSONExample-v2.3.spdx.json"), "--version"),
        ("-i", os.path.join(os.path.dirname(__file__), "data/SPDXJSONExample-v2.3.spdx.json"), "-o"),
    ],
)
def test_cli_with_system_exit_code_2(options):
    runner = CliRunner()

    result = runner.invoke(main, options)

    assert result.exit_code == 2
