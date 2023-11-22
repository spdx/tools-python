# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-IdentifiedNode: Apache-2.0
import json
import os
from rdflib import Graph, IdentifiedNode, Literal, IdentifiedNode, URIRef, BNode
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD
from rdflib.term import bind
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
        self.namespace_manager = graph.namespace_manager
        self.__debug_log_graph__()

        # TODO: does that work?
        bind("https://spdx.org/rdf/v3/Core/DateTime", XSD.dateTime)
        bind("https://spdx.org/rdf/v3/Core/SemVer", XSD.string)

    def n3(self, uri: IdentifiedNode) -> str:
        return uri.n3(self.namespace_manager)

    def __debug_log_namespaces__(self):
        for ns, url in self.namespace_manager.namespaces():
            print(f"DEBUG:   namespace: {ns} -> {url}")

    def __debug_log_graph__(self):
        print("DEBUG: graph:")
        print("DEBUG: START graph (serialized)...")
        print(self.graph.serialize(format='n3'))
        print("DEBUG: ...END graph (serialized)")
        self.__debug_log_namespaces__()
        for subject, predicate, object in self.graph:
            print(f"DEBUG:   {self.n3(subject)} {self.n3(predicate)} {self.n3(object)}", )

    def __debug_log_subject__(self, subject: IdentifiedNode):
        print("DEBUG: subject: ", subject)
        for predicate, object in self.graph.predicate_objects(subject=subject, unique=False):
            print(f"DEBUG:     {self.n3(predicate)} {self.n3(object)}")
    
    ####################################################################################################
    # low level functions

    def genSpdxURIRef(self, name: str, namespace: str = "Core"):
        return URIRef(f"https://spdx.org/rdf/v3/{namespace}/{name}")

    def getGraphValueRaw(self, subject: IdentifiedNode, predicate: IdentifiedNode, isMandatory: bool = False) -> str:
        print("DEBUG: get for subject: ", subject, " and predicate: ", predicate)
        value = self.graph.value(subject, predicate)
        if value is None:
            if isMandatory:
                raise Exception(f"no value for subject: {subject} and predicate: {predicate}")
            return None
        return value

    def getGraphValue(self, subject: IdentifiedNode, predicate: IdentifiedNode, isMandatory: bool = False) -> str:
        print("DEBUG: get for subject: ", subject, " and predicate: ", predicate)
        value = self.getGraphValueRaw(subject, predicate, isMandatory=isMandatory)
        if value is None:
            return None
        return value.toPython()

    def getGraphSpdxValue(self, subject: IdentifiedNode, namespace: str, name: str, isMandatory: bool = False) -> str:
        return self.getGraphValue(subject, self.genSpdxURIRef(namespace=namespace, name=name), isMandatory=isMandatory)

    def getGraphSpdxValueAsVersion(self, subject: IdentifiedNode, namespace: str, name: str) -> Version:
        value = self.getGraphSpdxValue(subject, namespace, name, isMandatory=True)
        return Version(value)

    def getGraphSpdxValueAsDatetime(self, subject: IdentifiedNode, namespace: str, name: str) -> Version:
        value = self.getGraphSpdxValue(subject, namespace, name, isMandatory=True)
        return datetime_from_str(value)

    def getGraphValues(self, subject: IdentifiedNode, predicate: IdentifiedNode) -> list[str]:
        return list(self.graph.objects(subject, predicate))

    def getGraphSpdxValues(self, subject: IdentifiedNode, namespace: str, name: str) -> list[str]:
        return self.getGraphValues(subject, URIRef(f"https://spdx.org/rdf/v3/{namespace}/{name}"))

    ####################################################################################################
    # higher level functions

    def getCreationInfo(self, subject: IdentifiedNode) -> CreationInfo:
        self.__debug_log_subject__(subject)
        return CreationInfo(
            spec_version=self.getGraphSpdxValueAsVersion(subject, "Core", "specVersion"),
            created=self.getGraphSpdxValueAsDatetime(subject, "Core", "created"),
            created_by=self.getGraphSpdxValues(subject, "Core", "createdBy"),
            profile=[], # TODO
            data_license=self.getGraphSpdxValue(subject, "Core", "dataLicense"),
            # created_using: List[str] = None,
            # comment: Optional[str] = None,
        )

    def getCreationInfoOfSubject(self, subject: IdentifiedNode) -> CreationInfo:
        subject_of_creation_info = self.getGraphValueRaw(subject, self.genSpdxURIRef(namespace="Core", name="creationInfo"))
        return self.getCreationInfo(BNode(subject_of_creation_info))

    ####################################################################################################
    # element handlers

    def handleSubjectOfTypeSpdxDocument(self, subject: IdentifiedNode) -> Element:
        return SpdxDocument(
            spdx_id=subject.toPython(),
            name=self.getGraphSpdxValue(subject, "Core", "name"),
            element=self.getGraphSpdxValues(subject, "Core", "element"),
            root_element=self.getGraphSpdxValues(subject, "Core", "rootElement"),
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

    def handleSubjectOfTypePackage(self, subject: IdentifiedNode) -> Element:
        return Package(
            spdx_id=subject.toPython(),
            name=self.getGraphSpdxValue(subject, "Core", "name"),
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

    def handleSubjectOfTypeFile(self, subject: IdentifiedNode) -> Element:
        return File(
            spdx_id = subject.toPython(),
            name = self.getGraphSpdxValue(subject, "Core","name"),
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

    def handleSubjectOfTypeRelationship(self, subject: IdentifiedNode) -> Element:
        relationship_type_uri = self.getGraphSpdxValue(subject, "Core", "relationshipType")
        relationship_type = relationship_type_uri.split("/")[-1]
        relationship_type = RelationshipType[relationship_type.upper()]

        return Relationship(
            spdx_id=subject.toPython(),
            from_element=self.getGraphSpdxValue(subject, "Core", "from"),
            relationship_type=relationship_type,
            to=self.getGraphSpdxValues(subject, "Core", "to")
        )

    def getTypeOfSubject(self, subject: IdentifiedNode) -> str:
        key_for_type = RDF.type
        type_of_subject = self.graph.value(subject, key_for_type)
        return type_of_subject.toPython()

    def getSubjectAsElement(self, subject: IdentifiedNode) -> Element:
        self.__debug_log_subject__(subject)
        type_of_subject = self.getTypeOfSubject(subject)

        non_element_types = [
            "https://spdx.org/rdf/v3/Core/CreationInfo"
        ]
        if type_of_subject in non_element_types:
            return None

        match type_of_subject:
            case "https://spdx.org/rdf/v3/Core/SpdxDocument":
                return self.handleSubjectOfTypeSpdxDocument(subject)
            case "https://spdx.org/rdf/v3/Software/Package":
                return self.handleSubjectOfTypePackage(subject)
            case "https://spdx.org/rdf/v3/Software/File":
                return self.handleSubjectOfTypeFile(subject)
            case "https://spdx.org/rdf/v3/Core/Relationship":
                return self.handleSubjectOfTypeRelationship(subject)
            case _:
                self.__debug_log_subject__(subject)
                raise Exception(f"{subject} has unsupported type={type_of_subject}")

    def get_subjects(self) -> list[IdentifiedNode]:
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
