# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from copy import deepcopy

from spdx_tools.spdx3.bump_from_spdx2.actor import bump_actor
from spdx_tools.spdx3.bump_from_spdx2.message import print_missing_conversion
from spdx_tools.spdx3.model import Annotation, AnnotationType, CreationInfo
from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx.model.actor import ActorType
from spdx_tools.spdx.model.annotation import Annotation as Spdx2_Annotation


def bump_annotation(
    spdx2_annotation: Spdx2_Annotation,
    payload: Payload,
    creation_info: CreationInfo,
    document_namespace: str,
    counter: int,
):
    spdx_id: str = "#".join([document_namespace, f"SPDXRef-Annotation-{counter}"])
    creation_info = deepcopy(creation_info)
    creation_info.created = spdx2_annotation.annotation_date

    # caution: the annotator and the annotation will only share the same creation_info if the actor
    #          has not been previously defined
    annotator = spdx2_annotation.annotator
    creator_id: str = bump_actor(annotator, payload, document_namespace, creation_info)
    if annotator.actor_type in [ActorType.PERSON, ActorType.ORGANIZATION]:
        creation_info.created_by = [creator_id]
    else:
        print_missing_conversion(
            "Annotator",
            0,
            "The SPDX2 annotation is not of Type Person or Organization."
            " This case leads to an invalid SPDX3 document and is currently not supported."
            "https://github.com/spdx/spdx-3-model/issues/180",
        )
    annotation_type: AnnotationType = AnnotationType[spdx2_annotation.annotation_type.name]

    payload.add_element(
        Annotation(
            spdx_id,
            annotation_type,
            creation_info=creation_info,
            subject=f"{document_namespace}#{spdx2_annotation.spdx_id}",
            statement=spdx2_annotation.annotation_comment,
        )
    )
