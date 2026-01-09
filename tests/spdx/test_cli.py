# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from importlib import resources

import pytest
from click.testing import CliRunner

from spdx_tools.spdx.clitools.pyspdxtools import main


@pytest.mark.parametrize(
    "options",
    [
        ("--infile", str(resources.files("tests.spdx.data").joinpath("SPDXJSONExample-v2.3.spdx.json"))),
        ("-i", str(resources.files("tests.spdx.data").joinpath("SPDXJSONExample-v2.3.spdx.json")), "--novalidation"),
        (
            "-i",
            str(resources.files("tests.spdx.data").joinpath("SPDXJSONExample-v2.3.spdx.json")),
            "--novalidation",
            "--version",
            "SPDX-2.3",
        ),
        ("-i", str(resources.files("tests.spdx.data").joinpath("SPDXJSONExample-v2.3.spdx.json")), "-o", "-"),
    ],
)
def test_cli_with_system_exit_code_0(options):
    runner = CliRunner()

    result = runner.invoke(main, options)

    assert result.exit_code == 0


@pytest.mark.parametrize(
    "options",
    [
        (
            "-i",
            str(
                resources.files("tests.spdx.data.invalid").joinpath(
                    "spdx-trivy-vmware_log-intelligence-fluentd-"
                    "sha256_086af034f561f343f633be9d9f9e95f65ae6c61b8ddb2c6755ef5bb25b40f53a.json"
                )
            ),
        ),
        ("-i", "non_existent_file.spdx"),
    ],
)
def test_cli_with_system_exit_code_1(options):
    runner = CliRunner()

    result = runner.invoke(main, options)

    assert result.exit_code == 1


@pytest.mark.parametrize(
    "options",
    [
        (),
        ("-i", str(resources.files("tests.spdx.data").joinpath("SPDXJSONExample-v2.3.spdx.json")), "--version"),
        ("-i", str(resources.files("tests.spdx.data").joinpath("SPDXJSONExample-v2.3.spdx.json")), "-o"),
    ],
)
def test_cli_with_system_exit_code_2(options):
    runner = CliRunner()

    result = runner.invoke(main, options)

    assert result.exit_code == 2
