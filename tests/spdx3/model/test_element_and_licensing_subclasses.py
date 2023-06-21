# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
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
from spdx_tools.spdx3.model.ai import AIPackage
from spdx_tools.spdx3.model.build import Build
from spdx_tools.spdx3.model.dataset import Dataset
from spdx_tools.spdx3.model.licensing import (
    CustomLicense,
    CustomLicenseAddition,
    ListedLicense,
    ListedLicenseException,
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
from spdx_tools.spdx3.model.software import File, Package, Sbom, Snippet, SoftwareDependencyRelationship
from tests.spdx3.fixtures import fixture_factory, get_fixture_dict
from tests.spdx3.model.model_test_utils import InvalidTypeClass, get_property_names

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
    ListedLicense,
    CustomLicense,
    ListedLicenseException,
    CustomLicenseAddition,
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
    File,
    Package,
    Snippet,
    Sbom,
    SoftwareDependencyRelationship,
    Dataset,
    AIPackage,
    Build,
]


@pytest.mark.parametrize(
    "clazz",
    CLASS_LIST,
)
def test_correct_initialization(clazz):
    clazz_instance = fixture_factory(clazz)
    fixture_dict = get_fixture_dict(clazz)

    for property_name in get_property_names(clazz):
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
        fixture_factory(clazz, **false_properties_dict)

    assert len(err.value.args[0]) == len(property_names)
    for error in err.value.args[0]:
        assert error.startswith(f"SetterError {clazz.__name__}")
