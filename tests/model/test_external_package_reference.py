import pytest

from src.model.package import ExternalPackageReference, ExternalPackageReferenceCategory


def test_correct_initialization():
    external_package_reference = ExternalPackageReference(ExternalPackageReferenceCategory.OTHER, "type", "locator",
                                                          "comment")
    assert external_package_reference.category == ExternalPackageReferenceCategory.OTHER
    assert external_package_reference.reference_type == "type"
    assert external_package_reference.locator == "locator"
    assert external_package_reference.comment == "comment"


def test_wrong_type_in_category():
    with pytest.raises(TypeError):
        ExternalPackageReference([ExternalPackageReferenceCategory.OTHER], 42, "locator", "comment")


def test_wrong_type_in_reference_type():
    with pytest.raises(TypeError):
        ExternalPackageReference(ExternalPackageReferenceCategory.OTHER, 42, "locator", "comment")


def test_wrong_type_in_locator():
    with pytest.raises(TypeError):
        ExternalPackageReference(ExternalPackageReferenceCategory.OTHER, "type", 42, "comment")


def test_wrong_type_in_comment():
    with pytest.raises(TypeError):
        ExternalPackageReference(ExternalPackageReferenceCategory.OTHER, "type", "locator", [])
