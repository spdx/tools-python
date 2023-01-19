from typing import List

from spdx3.bump_from_spdx2.message import print_missing_conversion

from spdx3.model.annotation import Annotation, AnnotationType

from spdx.model.annotation import Annotation as Spdx2_Annotation
from spdx3.model.creation_information import CreationInformation


def bump_annotation(spdx2_annotation: Spdx2_Annotation, creation_info: CreationInformation, counter: int) -> Annotation:
    spdx_id: str = f"SPDXRef-Annotation-{counter}"
    creation_info.created = spdx2_annotation.annotation_date
    # creation_info.created_by = bump_actor(spdx2_annotation.annotator)   waiting for entity implementation
    print("\n")
    print_missing_conversion("annotation.annotator", 1, "of Entity")
    annotation_type: AnnotationType = AnnotationType[spdx2_annotation.annotation_type.name]
    subject: List[str] = [spdx2_annotation.spdx_id]
    statement: str = spdx2_annotation.annotation_comment

    return Annotation(spdx_id, creation_info, annotation_type, subject, statement=statement)
