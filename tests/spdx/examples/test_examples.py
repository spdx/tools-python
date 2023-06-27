#  SPDX-FileCopyrightText: 2023 spdx contributors
#
#  SPDX-License-Identifier: Apache-2.0
import os.path
import runpy

import pytest


@pytest.fixture
def cleanup_output_files():
    yield

    files_to_delete = ["spdx2_to_3.jsonld", "my_spdx_document.spdx.json", "converted_format.xml", "graph.png"]
    for file in files_to_delete:
        output_file = os.path.join(os.path.dirname(__file__), file)
        if os.path.exists(output_file):
            os.remove(output_file)


def run_example(example_file: str):
    file_path = os.path.join(os.path.dirname(__file__), "../../../examples/", example_file)
    runpy.run_path(file_path)


def test_spdx2_parse_file():
    run_example("spdx2_parse_file.py")


@pytest.mark.usefixtures("cleanup_output_files")
def test_spdx2_convert_to_spdx3():
    run_example("spdx2_convert_to_spdx3.py")

    output_file = os.path.join(os.path.dirname(__file__), "spdx2_to_3.jsonld")
    assert os.path.exists(output_file)


@pytest.mark.usefixtures("cleanup_output_files")
def test_spdx2_document_from_scratch():
    run_example("spdx2_document_from_scratch.py")

    output_file = os.path.join(os.path.dirname(__file__), "my_spdx_document.spdx.json")
    assert os.path.exists(output_file)


@pytest.mark.usefixtures("cleanup_output_files")
def test_spdx2_convert_format():
    run_example("spdx2_convert_format.py")

    output_file = os.path.join(os.path.dirname(__file__), "converted_format.xml")
    assert os.path.exists(output_file)


@pytest.mark.usefixtures("cleanup_output_files")
def test_spdx2_generate_graph():
    try:
        import networkx  # noqa F401
        import pygraphviz  # noqa F401
    except ImportError:
        pytest.skip("Missing optional dependencies")

    run_example("spdx2_generate_graph.py")

    output_file = os.path.join(os.path.dirname(__file__), "graph.png")
    assert os.path.exists(output_file)
