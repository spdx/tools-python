from spdx_python_model import v3_0_1 as spdx_3_0

from spdx_tools.spdx3.binding import helpers
from spdx_tools.spdx3.model import Element
from spdx_tools.spdx3.model.creation_info import CreationInfo
from spdx_tools.spdx3.model.external_reference import ExternalReference
from spdx_tools.spdx3.model.software import Package
from spdx_tools.spdx3.model.software.software_artifact import SoftwareArtifact
from spdx_tools.spdx3.model.spdx_document import SpdxDocument
from tests.spdx3.helpers import domain_enum_to_binding_name


def test_get_binding_attribute_names():
    expected_names = {
        "_id",
        "creationInfo",
        "name",
        "summary",
        "description",
        "comment",
        "verifiedUsing",
        "externalRef",
        "externalIdentifier",
        "extension",
        "element",
        "rootElement",
        "import_",
        "profileConformance",
        "namespaceMap",
        "dataLicense",
    }

    actual_names = helpers.get_binding_attribute_names(spdx_3_0.SpdxDocument)
    assert actual_names == expected_names


def test_convert_binding_iri_to_domain_class():
    assert helpers.convert_binding_iri_to_domain_class(spdx_3_0.SpdxDocument().get_type()) is SpdxDocument
    assert helpers.convert_binding_iri_to_domain_class(spdx_3_0.CreationInfo().get_type()) is CreationInfo
    assert helpers.convert_binding_iri_to_domain_class(spdx_3_0.software_Package().get_type()) is Package
    assert helpers.convert_binding_iri_to_domain_class(spdx_3_0.ExternalRef().get_type()) is ExternalReference


def test_get_attributes_by_domain_class_hierarchy():
    result = helpers.get_attributes_by_domain_class_hierarchy(Package)

    # Check that the result contains expected classes and attributes
    assert Package in result
    assert "package_version" in result[Package]
    assert "home_page" in result[Package]
    assert "spdx_id" not in result[Package]  # Inherited attribute should not be here

    assert SoftwareArtifact in result
    assert "primary_purpose" in result[SoftwareArtifact]
    assert "additional_purpose" in result[SoftwareArtifact]

    assert Element in result
    assert "spdx_id" in result[Element]
    assert "name" in result[Element]


def test_domain_enum_to_binding_name():
    assert domain_enum_to_binding_name("BLAKE2B512") == "blake2b512"
    assert domain_enum_to_binding_name("CRYSTALS_DILITHIUM") == "crystalsDilithium"
    assert domain_enum_to_binding_name("ALT_DOWNLOAD_LOCATION") == "altDownloadLocation"
    assert domain_enum_to_binding_name("SHA3_512") == "sha3_512"
