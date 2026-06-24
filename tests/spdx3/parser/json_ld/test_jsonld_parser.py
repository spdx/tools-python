import os
import typing
from datetime import datetime

from semantic_version import Version

from spdx_tools.spdx3.model import CreationInfo, ExternalIdentifierType, Person, ProfileIdentifierType
from spdx_tools.spdx3.model.extension.cdx_properties_extension import CdxPropertiesExtension
from spdx_tools.spdx3.model.simplelicensing.license_expression import LicenseExpression
from spdx_tools.spdx3.model.software import Sbom
from spdx_tools.spdx3.model.spdx_document import SpdxDocument
from spdx_tools.spdx3.parser.jsonld.jsonld_parser import parse_from_file


def test_parse_from_file():
    file_path = os.path.join(os.path.dirname(__file__), "../../data/spdxV3-example.json")
    payload = parse_from_file(file_path)

    # Test SpdxDocument
    spdx_document = payload.get_element("http://spdx.example.com/Document1")
    assert spdx_document is not None
    assert isinstance(spdx_document, SpdxDocument)
    assert spdx_document.spdx_id == "http://spdx.example.com/Document1"
    assert spdx_document.profile_conformance == [ProfileIdentifierType.CORE, ProfileIdentifierType.SOFTWARE]
    assert spdx_document.root_element == ["urn:example13-sbom.com-4fe40e24-20e3-11ee-be56-0242ac120002"]

    assert spdx_document.creation_info is not None
    assert isinstance(spdx_document.creation_info, CreationInfo)
    assert spdx_document.creation_info.spec_version == Version("3.0.1")
    assert spdx_document.creation_info.created == datetime.fromisoformat("2024-05-02T00:00:00+00:00")

    # Test sbom
    sbom = payload.get_element("urn:example13-sbom.com-4fe40e24-20e3-11ee-be56-0242ac120002")
    assert sbom is not None
    assert isinstance(sbom, Sbom)
    assert sbom.spdx_id == "urn:example13-sbom.com-4fe40e24-20e3-11ee-be56-0242ac120002"
    assert sbom.profile_conformance == [ProfileIdentifierType.CORE, ProfileIdentifierType.SOFTWARE]
    assert sbom.root_element == ["urn:product-acme-application-1.3-4fe40e24-20e3-11ee-be56-0242ac120002"]

    # Test Person - Jane Doe
    jane_doe = payload.get_element("urn:jane-doe-1@acme.com-4fe40e24-20e3-11ee-be56-0242ac120002")
    assert jane_doe is not None
    assert isinstance(jane_doe, Person)
    assert jane_doe.spdx_id == "urn:jane-doe-1@acme.com-4fe40e24-20e3-11ee-be56-0242ac120002"
    assert jane_doe.name == "Application Owner Jane Doe"
    assert len(jane_doe.external_identifier) == 1
    assert jane_doe.external_identifier[0].external_identifier_type == ExternalIdentifierType.EMAIL
    assert jane_doe.external_identifier[0].identifier == "jane-doe-1@acme.com"

    # Test Organization - Acme Company
    acme_company = payload.get_element("urn:acme.com-4fe40e24-20e3-11ee-be56-0242ac120002")
    assert acme_company is not None
    # Import Organization class to use in isinstance check
    from spdx_tools.spdx3.model import Organization

    assert isinstance(acme_company, Organization)
    assert acme_company.spdx_id == "urn:acme.com-4fe40e24-20e3-11ee-be56-0242ac120002"
    assert acme_company.name == "Acme Company"

    # Test Person - Fedor Indutny
    fedor_indutny = payload.get_element("urn:github.com-indutny-c4fe40e24-20e3-11ee-be56-0242ac120002")
    assert fedor_indutny is not None
    assert isinstance(fedor_indutny, Person)
    assert fedor_indutny.spdx_id == "urn:github.com-indutny-c4fe40e24-20e3-11ee-be56-0242ac120002"
    assert fedor_indutny.name == "Fedor Indutny"
    assert len(fedor_indutny.external_identifier) == 1
    assert fedor_indutny.external_identifier[0].external_identifier_type == ExternalIdentifierType.OTHER
    assert fedor_indutny.external_identifier[0].identifier == "https://github.com/indutny"

    # Test Organization - Alpine Linux
    alpine_linux = payload.get_element("urn:github.com-alpinelinux-4fe40e24-20e3-11ee-be56-0242ac120002")
    assert alpine_linux is not None
    assert isinstance(alpine_linux, Organization)
    assert alpine_linux.spdx_id == "urn:github.com-alpinelinux-4fe40e24-20e3-11ee-be56-0242ac120002"
    assert alpine_linux.name == "Alpine Linux"

    # Test Package - Acme Application
    acme_app = payload.get_element("urn:product-acme-application-1.3-4fe40e24-20e3-11ee-be56-0242ac120002")
    assert acme_app is not None
    from spdx_tools.spdx3.model.software import Package

    assert isinstance(acme_app, Package)
    assert acme_app.spdx_id == "urn:product-acme-application-1.3-4fe40e24-20e3-11ee-be56-0242ac120002"
    assert acme_app.name == "Acme Application"
    assert acme_app.package_version == "1.3"
    assert acme_app.supplied_by == "urn:acme.com-4fe40e24-20e3-11ee-be56-0242ac120002"
    assert len(acme_app.extension) == 1
    extension = acme_app.extension[0]
    assert type(extension) is CdxPropertiesExtension
    assert len(extension.cdx_property) == 1
    assert extension.cdx_property[0].cdx_prop_name == "example name"
    assert extension.cdx_property[0].cdx_prop_value == "example value"

    # Test external identifiers
    assert len(acme_app.external_identifier) == 2
    cpe_identifier = next(
        (ei for ei in acme_app.external_identifier if ei.external_identifier_type == ExternalIdentifierType.CPE23),
        None,
    )
    assert cpe_identifier is not None
    assert cpe_identifier.identifier == "cpe:2.3:a:*:acme-application:1.3:*:*:*:*:*:*:*"
    purl_identifier = next(
        (
            ei
            for ei in acme_app.external_identifier
            if ei.external_identifier_type == ExternalIdentifierType.PACKAGE_URL
        ),
        None,
    )
    assert purl_identifier is not None
    assert purl_identifier.identifier == "pkg:generic/acme-application@1.3"
    # Test external references
    assert len(acme_app.external_reference) == 3
    external_reference = next((er for er in acme_app.external_reference if er.comment == "comment1"), None)
    assert external_reference is not None
    assert external_reference.locator == ["locator1"]

    # Test Package - npm-elliptic
    elliptic_package = payload.get_element("urn:npm-elliptic-6.5.2-4fe40e24-20e3-11ee-be56-0242ac120002")
    assert elliptic_package is not None
    assert isinstance(elliptic_package, Package)
    assert elliptic_package.spdx_id == "urn:npm-elliptic-6.5.2-4fe40e24-20e3-11ee-be56-0242ac120002"
    assert elliptic_package.name == "npm-elliptic"
    assert elliptic_package.package_version == "6.5.2"
    assert elliptic_package.supplied_by == "urn:github.com-indutny-c4fe40e24-20e3-11ee-be56-0242ac120002"
    assert len(elliptic_package.external_identifier) == 1
    assert elliptic_package.external_identifier[0].external_identifier_type == ExternalIdentifierType.OTHER
    assert (
        elliptic_package.external_identifier[0].identifier == "https://github.com/indutny/elliptic/releases/tag/v6.5.2"
    )

    # Test Package - Alpine Container
    alpine_container = payload.get_element(
        (
            "urn:container-alpine-latest-sha256:"
            "69665d02cb32192e52e07644d76bc6f25abeb5410edc1c7a81a10ba3f0efb90a-4fe40e24-20e3-11ee-be56-0242ac120002"
        )
    )
    assert alpine_container is not None
    assert isinstance(alpine_container, Package)
    assert alpine_container.spdx_id == (
        "urn:container-alpine-latest-sha256:"
        "69665d02cb32192e52e07644d76bc6f25abeb5410edc1c7a81a10ba3f0efb90a-4fe40e24-20e3-11ee-be56-0242ac120002"
    )
    assert alpine_container.name == "alpine:latest"
    assert alpine_container.package_version == "69665d02cb32192e52e07644d76bc6f25abeb5410edc1c7a81a10ba3f0efb90a"
    assert alpine_container.supplied_by == "urn:github.com-alpinelinux-4fe40e24-20e3-11ee-be56-0242ac120002"

    # Test Package - OpenSSL
    openssl_package = payload.get_element("urn:openssl-3.0.4-4fe40e24-20e3-11ee-be56-0242ac120002")
    assert openssl_package is not None
    assert isinstance(openssl_package, Package)
    assert openssl_package.spdx_id == "urn:openssl-3.0.4-4fe40e24-20e3-11ee-be56-0242ac120002"
    assert openssl_package.name == "openssl"
    assert openssl_package.package_version == "3.0.4"


def test_parse_from_file_2():
    file_path = os.path.join(os.path.dirname(__file__), "../../data/example6-bin.json")
    payload = parse_from_file(file_path)

    # Test SpdxDocument
    spdx_document = payload.get_element("https://swinslow.net/spdx-examples/example6/hello-go-bin-v2-specv3/document0")
    assert spdx_document is not None
    assert isinstance(spdx_document, SpdxDocument)
    assert spdx_document.spdx_id == "https://swinslow.net/spdx-examples/example6/hello-go-bin-v2-specv3/document0"
    assert spdx_document.root_element == [
        "https://swinslow.net/spdx-examples/example6/hello-go-bin-v2-specv3/SPDXRef-gnrtd4"
    ]
    assert (
        spdx_document.data_license
        == "https://swinslow.net/spdx-examples/example6/hello-go-bin-v2-specv3/SPDXRef-gnrtd16"
    )

    assert spdx_document.creation_info is not None
    assert isinstance(spdx_document.creation_info, CreationInfo)
    assert spdx_document.creation_info.spec_version == Version("3.0.1")
    assert spdx_document.creation_info.created == datetime.fromisoformat("2021-08-26T01:56:00+00:00")

    license_expression: LicenseExpression = typing.cast(
        LicenseExpression,
        payload.get_element("https://swinslow.net/spdx-examples/example6/hello-go-bin-v2-specv3/SPDXRef-gnrtd16"),
    )
    assert license_expression is not None
    assert license_expression.license_expression == "CC0-1.0"

    person: Person = typing.cast(
        Person,
        payload.get_element("https://swinslow.net/spdx-examples/example6/hello-go-bin-v2-specv3/SPDXRef-gnrtd0"),
    )
    assert person is not None
    assert isinstance(person, Person)
    assert person.name == "Steve Winslow"
    assert len(person.external_identifier) == 1
    person_external_id = person.external_identifier[0]
    assert person_external_id.external_identifier_type == ExternalIdentifierType.EMAIL
    assert person_external_id.identifier == "steve@swinslow.net"
