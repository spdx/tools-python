# SPDX-FileCopyrightText: 2026 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import os.path
import shutil

import pytest

from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.parser.parse_anything import parse_file

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def test_parse_json_content_saved_with_bare_spdx_extension(tmp_path):
    # Some third-party pipelines (e.g. Yocto/OpenEmbedded SBOM generation followed by
    # post-processing tools) write JSON-format SPDX documents to a file ending in a bare
    # ".spdx" extension instead of ".spdx.json". Before the fix, file_name_to_format()
    # classified any ".spdx" file as TAG_VALUE, so this JSON content was fed into the
    # tag-value parser. Its error recovery silently drops every token it doesn't
    # recognize, so creation info ends up empty and construction fails with a confusing
    # "missing 6 required positional arguments" TypeError instead of parsing correctly
    # (#890).
    source = os.path.join(DATA_DIR, "SPDXJSONExample-v2.3.spdx.json")
    destination = tmp_path / "device.spdx"
    shutil.copyfile(source, destination)

    document = parse_file(str(destination))

    assert document is not None
    assert document.creation_info.spdx_version == "SPDX-2.3"
    assert document.creation_info.name == "SPDX-Tools-v2.0"


def test_json_content_with_bare_spdx_extension_raised_before_fix(tmp_path):
    # Characterization of the pre-fix failure mode: confirms the specific error message
    # reported in #890 (both the field list and phrasing) so a regression back to feeding
    # JSON through the tag-value parser is caught precisely, not just as "some error".
    from spdx_tools.spdx.parser.tagvalue import tagvalue_parser

    source = os.path.join(DATA_DIR, "SPDXJSONExample-v2.3.spdx.json")
    destination = tmp_path / "device.spdx"
    shutil.copyfile(source, destination)

    with pytest.raises(SPDXParsingError) as err:
        tagvalue_parser.parse_from_file(str(destination))

    message = str(err.value.messages)
    assert "Error while constructing CreationInfo" in message
    assert "missing 6 required positional arguments" in message


def test_legitimate_tagvalue_file_with_spdx_extension_is_unaffected(tmp_path):
    # Guard against the fix over-correcting: a real tag-value ".spdx" file (this project's
    # own convention, see tests/spdx/data/SPDXTagExample-v2.3.spdx) must still be routed to
    # the tag-value parser.
    source = os.path.join(DATA_DIR, "SPDXTagExample-v2.3.spdx")
    destination = tmp_path / "example.spdx"
    shutil.copyfile(source, destination)

    document = parse_file(str(destination))

    assert document is not None
    assert document.creation_info.spdx_version == "SPDX-2.3"
