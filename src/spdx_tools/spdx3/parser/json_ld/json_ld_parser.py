# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import json
import os
from rdflib import Graph, URIRef, Literal
from semantic_version import Version

from spdx_tools.spdx3.payload import Payload
from spdx_tools.spdx3.model.relationship import Relationship, RelationshipType
from spdx_tools.spdx3.model import (
    Element,
    Bundle,
    CreationInfo,
    ExternalIdentifier,
    ExternalMap,
    ExternalReference,
    IntegrityMethod,
    NamespaceMap,
)
from spdx_tools.spdx3.model.spdx_document import SpdxDocument
from spdx_tools.spdx.datetime_conversions import datetime_from_str
from spdx_tools.spdx3.model.software.file import File
from spdx_tools.spdx3.model.software.package import Package


def parse_from_file(file_name: str, encoding: str = "utf-8") -> Payload:
    return JsonLDParser().parseFile(file_name, encoding)

def parse_from_string(file_name: str) -> Payload:
    return JsonLDParser().parseString(file_name)

class GraphToElementConverter:
    def __init__(self, graph: Graph):
        self.graph = graph

    def __debug_log_subject__(self, subject: URIRef):
        print("subject: ", subject)
        for predicate, object in self.graph.predicate_objects(subject=subject, unique=False):
            print("    ", predicate, object)

    def getGraphValue(self, subject: URIRef, predicate: URIRef) -> str:
        value = self.graph.value(subject, predicate)
        if value is None:
            return None
        return value.toPython()

    def getGraphValues(self, subject: URIRef, predicate: URIRef) -> list[str]:
        return list(self.graph.objects(subject, predicate))

    def getCreationInfo(self, subject: URIRef) -> CreationInfo:
        # self.__debug_log_subject__(subject)
        return CreationInfo(
            spec_version=Version(self.getGraphValue(subject, URIRef("https://spdx.org/rdf/v3/Core/specVersion"))),
            created=datetime_from_str(self.getGraphValue(subject, URIRef("https://spdx.org/rdf/v3/Core/created"))),
            created_by=self.getGraphValues(subject, URIRef("https://spdx.org/rdf/v3/Core/createdBy")),
            profile=[], # TODO
            data_license=self.getGraphValue(subject, URIRef("https://spdx.org/rdf/v3/Core/dataLicense")),
            # created_using: List[str] = None,
            # comment: Optional[str] = None,
        )

    def getCreationInfoOfSubject(self, subject: URIRef) -> CreationInfo:
        subject_of_creation_info = self.graph.value(subject, URIRef("https://spdx.org/rdf/v3/Core/creationInfo"))
        return self.getCreationInfo(subject_of_creation_info)

    def handleSubjectOfTypeSpdxDocument(self, subject: URIRef) -> Element:
        return SpdxDocument(
            spdx_id=subject.toPython(),
            name=self.getGraphValue(subject, URIRef("https://spdx.org/rdf/v3/Core/name")),
            element=self.getGraphValues(subject, URIRef("https://spdx.org/rdf/v3/Core/element")),
            root_element=self.getGraphValues(subject, URIRef("https://spdx.org/rdf/v3/Core/rootElement")),
            creation_info=self.getCreationInfoOfSubject(subject),
            # summary: Optional[str] = None,
            # description: Optional[str] = None,
            # comment: Optional[str] = None,
            # verified_using: List[IntegrityMethod] = None,
            # external_reference: List[ExternalReference] = None,
            # external_identifier: List[ExternalIdentifier] = None,
            # extension: Optional[str] = None,
            # namespaces: List[NamespaceMap] = None,
            # imports: List[ExternalMap] = None,
            # context: Optional[str] = None,
        )

    def handleSubjectOfTypePackage(self, subject: URIRef) -> Element:
        return Package(
            spdx_id=subject.toPython(),
            name=self.getGraphValue(subject, URIRef("https://spdx.org/rdf/v3/Core/name")),
            creation_info=self.getCreationInfoOfSubject(subject),
            # summary: Optional[str] = None,
            # description: Optional[str] = None,
            # comment: Optional[str] = None,
            # verified_using: List[IntegrityMethod] = None,
            # external_reference: List[ExternalReference] = None,
            # external_identifier: List[ExternalIdentifier] = None,
            # extension: Optional[str] = None,
            # originated_by: List[str] = None,
            # supplied_by: List[str] = None,
            # built_time: Optional[datetime] = None,
            # release_time: Optional[datetime] = None,
            # valid_until_time: Optional[datetime] = None,
            # standard: List[str] = None,
            # content_identifier: Optional[str] = None,
            # primary_purpose: Optional[SoftwarePurpose] = None,
            # additional_purpose: List[SoftwarePurpose] = None,
            # concluded_license: Optional[LicenseField] = None,
            # declared_license: Optional[LicenseField] = None,
            # copyright_text: Optional[str] = None,
            # attribution_text: Optional[str] = None,
            # package_version: Optional[str] = None,
            # download_location: Optional[str] = None,
            # package_url: Optional[str] = None,
            # homepage: Optional[str] = None,
            # source_info: Optional[str] = None,
        )

    def handleSubjectOfTypeFile(self, subject: URIRef) -> Element:
        return File(
            spdx_id = subject.toPython(),
            name = self.getGraphValue(subject, URIRef("https://spdx.org/rdf/v3/Core/name")),
            creation_info = self.getCreationInfoOfSubject(subject),
            # summary: Optional[str] = None,
            # description: Optional[str] = None,
            # comment: Optional[str] = None,
            # verified_using: List[IntegrityMethod] = None,
            # external_reference: List[ExternalReference] = None,
            # external_identifier: List[ExternalIdentifier] = None,
            # extension: Optional[str] = None,
            # originated_by: List[str] = None,
            # supplied_by: List[str] = None,
            # built_time: Optional[datetime] = None,
            # release_time: Optional[datetime] = None,
            # valid_until_time: Optional[datetime] = None,
            # standard: List[str] = None,
            # content_identifier: Optional[str] = None,
            # primary_purpose: Optional[SoftwarePurpose] = None,
            # additional_purpose: List[SoftwarePurpose] = None,
            # concluded_license: Optional[LicenseField] = None,
            # declared_license: Optional[LicenseField] = None,
            # copyright_text: Optional[str] = None,
            # attribution_text: Optional[str] = None,
            # content_type: Optional[str] = None,
        )

    def handleSubjectOfTypeRelationship(self, subject: URIRef) -> Element:
        relationship_type_uri = self.graph.value(subject, URIRef("https://spdx.org/rdf/v3/Core/relationshipType"))
        relationship_type = relationship_type_uri.split("/")[-1]
        relationship_type = RelationshipType[relationship_type.upper()]

        return Relationship(
            spdx_id=subject.toPython(),
            from_element=self.graph.value(subject, URIRef("https://spdx.org/rdf/v3/Core/from")),
            relationship_type=relationship_type,
            to=list(self.graph.objects(subject, URIRef("https://spdx.org/rdf/v3/Core/to"))),
        )

    def getTypeOfSubject(self, subject: URIRef) -> str:
        key_for_type = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
        type_of_subject = self.graph.value(subject, key_for_type)
        return type_of_subject.toPython()

    def getSubjectAsElement(self, subject: URIRef) -> Element:
        type_of_subject = self.getTypeOfSubject(subject)
        # self.__debug_log_subject__(subject)
        match type_of_subject:
            case "https://spdx.org/rdf/v3/Core/SpdxDocument":
                return self.handleSubjectOfTypeSpdxDocument(subject)
            case "https://spdx.org/rdf/v3/Software/Package":
                return self.handleSubjectOfTypePackage(subject)
            case "https://spdx.org/rdf/v3/Software/File":
                return self.handleSubjectOfTypeFile(subject)
            case "https://spdx.org/rdf/v3/Core/Relationship":
                return self.handleSubjectOfTypeRelationship(subject)
            case "https://spdx.org/rdf/v3/Core/CreationInfo":
                return None
            case _:
                print("ERR: unsupported type: ", type_of_subject)
                self.__debug_log_subject__(subject)

    def get_subjects(self) -> list[URIRef]:
        return list(self.graph.subjects(unique=True))

class JsonLDParser:
    def graphToPayload(self, graph: Graph) -> Payload:
        converter = GraphToElementConverter(graph)
        payload = Payload()


        for subject in converter.get_subjects():
            element = converter.getSubjectAsElement(subject)
            if element is not None:
                payload.add_element(element)

        return payload

    def parseString(self, data: str) -> Payload:
        graph = Graph().parse(data=data, format='json-ld')
        return self.graphToPayload(graph)

    def parseFile(self, file_name: str, encoding: str = "utf-8") -> Payload:
        with open(file_name, "r", encoding=encoding) as file:
            data = file.read()
            return self.parseString(data)
