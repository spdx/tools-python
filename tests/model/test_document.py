from unittest import mock

import pytest

from src.model.document import Document


@mock.patch('src.model.document.CreationInfo', autospec=True)
@mock.patch('src.model.external_document_ref.ExternalDocumentRef', autospec=True)
@mock.patch('src.model.package.Package', autospec=True)
@mock.patch('src.model.file.File', autospec=True)
@mock.patch('src.model.snippet.Snippet', autospec=True)
@mock.patch('src.model.annotation.Annotation', autospec=True)
@mock.patch('src.model.relationship.Relationship', autospec=True)
@mock.patch('src.model.extracted_licensing_info.ExtractedLicensingInfo', autospec=True)
def test_correct_initialization(creation_info, ext_ref, package, file, snippet, annotation, relationship,
                                extracted_lic):
    document = Document("version", "id", "name", "namespace", creation_info, "data_license", [ext_ref, ext_ref],
                        "comment", [package, package], [file, file], [snippet, snippet], [annotation, annotation],
                        [relationship, relationship], [extracted_lic, extracted_lic])
    assert document.spdx_version == "version"
    assert document.spdx_id == "id"
    assert document.name == "name"
    assert document.document_namespace == "namespace"
    assert document.creation_info == creation_info
    assert document.data_license == "data_license"
    assert document.external_document_refs == [ext_ref, ext_ref]
    assert document.comment == "comment"
    assert document.packages == [package, package]
    assert document.files == [file, file]
    assert document.snippets == [snippet, snippet]
    assert document.annotations == [annotation, annotation]
    assert document.relationships == [relationship, relationship]
    assert document.extracted_licensing_info == [extracted_lic, extracted_lic]


@mock.patch('src.model.document.CreationInfo', autospec=True)
def test_correct_initialization_with_default_values(creation_info):
    document = Document("version", "id", "name", "namespace", creation_info, "data_license")
    assert document.spdx_version == "version"
    assert document.spdx_id == "id"
    assert document.name == "name"
    assert document.document_namespace == "namespace"
    assert document.creation_info == creation_info
    assert document.data_license == "data_license"
    assert document.external_document_refs == []
    assert document.comment is None
    assert document.packages == []
    assert document.files == []
    assert document.snippets == []
    assert document.annotations == []
    assert document.relationships == []
    assert document.extracted_licensing_info == []


@mock.patch('src.model.document.CreationInfo', autospec=True)
def test_wrong_type_in_spdx_version(creation_info):
    with pytest.raises(TypeError):
        Document(2.3, "id", "name", "namespace", creation_info, "data_license")


@mock.patch('src.model.document.CreationInfo', autospec=True)
def test_wrong_type_in_spdx_id(creation_info):
    with pytest.raises(TypeError):
        Document("version", 42, "name", "namespace", creation_info, "data_license")


@mock.patch('src.model.document.CreationInfo', autospec=True)
def test_wrong_type_in_name(creation_info):
    with pytest.raises(TypeError):
        Document("version", "id", ["name"], "namespace", creation_info, "data_license")


@mock.patch('src.model.document.CreationInfo', autospec=True)
def test_wrong_type_in_document_namespace(creation_info):
    with pytest.raises(TypeError):
        Document("version", "id", "name", {}, creation_info, "data_license")


def test_wrong_type_in_creation_info():
    with pytest.raises(TypeError):
        Document("version", "id", "name", "namespace", "string", "data_license")


@mock.patch('src.model.document.CreationInfo', autospec=True)
def test_wrong_type_in_data_license(creation_info):
    with pytest.raises(TypeError):
        Document("version", "id", "name", "namespace", creation_info, ["data_license"])


@mock.patch('src.model.document.CreationInfo', autospec=True)
def test_wrong_type_in_external_document_refs(creation_info):
    with pytest.raises(TypeError):
        Document("version", "id", "name", "namespace", creation_info, "data_license", external_document_refs=["string"])


@mock.patch('src.model.document.CreationInfo', autospec=True)
def test_wrong_type_in_comment(creation_info):
    with pytest.raises(TypeError):
        Document("version", "id", "name", "namespace", creation_info, "data_license", comment=42)


@mock.patch('src.model.document.CreationInfo', autospec=True)
def test_wrong_type_in_packages(creation_info):
    with pytest.raises(TypeError):
        Document("version", "id", "name", "namespace", creation_info, "data_license", packages=["string"])


@mock.patch('src.model.document.CreationInfo', autospec=True)
def test_wrong_type_in_files(creation_info):
    with pytest.raises(TypeError):
        Document("version", "id", "name", "namespace", creation_info, "data_license", files={})


@mock.patch('src.model.document.CreationInfo', autospec=True)
def test_wrong_type_in_snippets(creation_info):
    with pytest.raises(TypeError):
        Document("version", "id", "name", "namespace", creation_info, "data_license", snippets=())


@mock.patch('src.model.document.CreationInfo', autospec=True)
def test_wrong_type_in_annotations(creation_info):
    with pytest.raises(TypeError):
        Document("version", "id", "name", "namespace", creation_info, "data_license", annotations=["string"])


@mock.patch('src.model.document.CreationInfo', autospec=True)
def test_wrong_type_in_relationships(creation_info):
    with pytest.raises(TypeError):
        Document("version", "id", "name", "namespace", creation_info, "data_license", relationships="string")


@mock.patch('src.model.document.CreationInfo', autospec=True)
def test_wrong_type_in_extracted_licensing_info(creation_info):
    with pytest.raises(TypeError):
        Document("version", "id", "name", "namespace", creation_info, "data_license", extracted_licensing_info=42)
