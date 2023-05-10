# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import sys

from spdx_tools.spdx3.bump_from_spdx2.spdx_document import bump_spdx_document
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx3.writer.console.payload_writer import write_payload
from spdx_tools.spdx.model.actor import ActorType
from spdx_tools.spdx.model.document import Document as Spdx2_Document
from tests.spdx.fixtures import actor_fixture, annotation_fixture, creation_info_fixture, document_fixture


def test_bump_spdx_document():
    spdx2_document: Spdx2_Document = document_fixture()
    spdx2_document.creation_info.creators.append(actor_fixture(ActorType.TOOL, "tool_name", None))
    document_namespace = document_fixture().creation_info.document_namespace

    payload: Payload = bump_spdx_document(spdx2_document)

    write_payload(payload, sys.stdout)

    assert f"{document_namespace}#SPDXRef-Package" in payload.get_full_map()
    assert len(payload.get_full_map()) == 11

    # this is more of a temporary test to make sure the dates don't get messed up again
    assert (
        payload.get_element("#".join([document_namespace, "SPDXRef-DOCUMENT"])).creation_info.created
        == creation_info_fixture().created
    )
    assert (
        payload.get_element("#".join([document_namespace, "SPDXRef-Annotation-0"])).creation_info.created
        == annotation_fixture().annotation_date
    )
