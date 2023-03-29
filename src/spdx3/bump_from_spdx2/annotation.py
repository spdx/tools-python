# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from copy import deepcopy

from spdx.model.actor import ActorType
from spdx.model.annotation import Annotation as Spdx2_Annotation
from spdx3.bump_from_spdx2.actor import bump_actor
from spdx3.model.annotation import Annotation, AnnotationType
from spdx3.model.creation_information import CreationInformation
from spdx3.payload import Payload


def bump_annotation(spdx2_annotation: Spdx2_Annotation, payload: Payload, creation_info: CreationInformation,
                    document_namespace: str, counter: int):
    spdx_id: str = "#".join([document_namespace, f"SPDXRef-Annotation-{counter}"])
    creation_info = deepcopy(creation_info)
    creation_info.created = spdx2_annotation.annotation_date

    # caution: the annotator and the annotation will only share the same creation_info if the actor
    #          has not been previously defined
    annotator = spdx2_annotation.annotator
    creator_id: str = bump_actor(annotator, payload, creation_info, document_namespace)
    if annotator.actor_type in [ActorType.PERSON, ActorType.ORGANIZATION]:
        creation_info.created_by = [creator_id]
    else:
        raise NotImplementedError("The SPDX2 annotation is not of Type Person or Organization."
                                  " This case leads to an invalid SPDX3 document and is currently not supported.")
    annotation_type: AnnotationType = AnnotationType[spdx2_annotation.annotation_type.name]
    subject: str = spdx2_annotation.spdx_id
    statement: str = spdx2_annotation.annotation_comment

    payload.add_element(Annotation(spdx_id, creation_info, annotation_type, subject, statement=statement))
