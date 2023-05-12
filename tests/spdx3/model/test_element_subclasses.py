# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from typing import Any, Type

import pytest

from spdx_tools.spdx3.model import (
    Agent,
    Annotation,
    Bom,
    Bundle,
    LifecycleScopedRelationship,
    Organization,
    Person,
    Relationship,
    SoftwareAgent,
    SpdxDocument,
)
from spdx_tools.spdx3.model.security import (
    CvssV2VulnAssessmentRelationship,
    CvssV3VulnAssessmentRelationship,
    EpssVulnAssessmentRelationship,
    ExploitCatalogVulnAssessmentRelationship,
    SsvcVulnAssessmentRelationship,
    VexAffectedVulnAssessmentRelationship,
    VexFixedVulnAssessmentRelationship,
    VexNotAffectedVulnAssessmentRelationship,
    VexUnderInvestigationVulnAssessmentRelationship,
    Vulnerability,
)
from tests.spdx3.fixtures import element_fixture_factory, get_fixture_dict


def get_property_names(clazz: Type[Any]):
    return [
        attribute
        for attribute in dir(clazz)
        if not attribute.startswith("_") and not callable(getattr(clazz, attribute))
    ]


CLASS_LIST = [
    Agent,
    Person,
    Organization,
    SoftwareAgent,
    Annotation,
    Relationship,
    LifecycleScopedRelationship,
    Bundle,
    Bom,
    SpdxDocument,
    CvssV2VulnAssessmentRelationship,
    CvssV3VulnAssessmentRelationship,
    EpssVulnAssessmentRelationship,
    ExploitCatalogVulnAssessmentRelationship,
    SsvcVulnAssessmentRelationship,
    VexAffectedVulnAssessmentRelationship,
    VexFixedVulnAssessmentRelationship,
    VexNotAffectedVulnAssessmentRelationship,
    VexUnderInvestigationVulnAssessmentRelationship,
    Vulnerability,
]


@pytest.mark.parametrize(
    "clazz",
    CLASS_LIST,
)
def test_correct_initialization(clazz):
    clazz_instance = element_fixture_factory(clazz)
    fixture_dict = get_fixture_dict(clazz)

    property_names = get_property_names(clazz)

    for property_name in property_names:
        assert getattr(clazz_instance, property_name) is not None
        assert getattr(clazz_instance, property_name) == fixture_dict[property_name]


@pytest.mark.parametrize(
    "clazz",
    CLASS_LIST,
)
def test_invalid_initialization(clazz):
    property_names = get_property_names(clazz)
    false_properties_dict = {}
    for property_name in property_names:
        false_properties_dict[property_name] = InvalidTypeClass()

    with pytest.raises(TypeError) as err:
        element_fixture_factory(clazz, **false_properties_dict)

    assert len(err.value.args[0]) == len(property_names)
    for error in err.value.args[0]:
        assert error.startswith(f"SetterError {clazz.__name__}")


class InvalidTypeClass:
    pass
