# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-IdentifiedNode: Apache-2.0
import json
import os
from rdflib import Graph, IdentifiedNode, Literal, IdentifiedNode, URIRef, BNode, Variable
from rdflib.namespace import DC, DCTERMS, DOAP, FOAF, SKOS, OWL, RDF, RDFS, VOID, XMLNS, XSD
from rdflib.term import Node, Identifier, bind
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
    Hash,
    HashAlgorithm,
)
from spdx_tools.spdx3.model.spdx_document import SpdxDocument
from spdx_tools.spdx.datetime_conversions import datetime_from_str
from spdx_tools.spdx3.model.software.file import File
from spdx_tools.spdx3.model.software.package import Package

def camel_to_snake(s):
    return ''.join(['_'+c.lower() if c.isupper() else c for c in s]).lstrip('_')

def parse_from_file(file_name: str, encoding: str = "utf-8") -> Payload:
    return JsonLDParser().parseFile(file_name, encoding)

def parse_from_string(file_name: str) -> Payload:
    return JsonLDParser().parseString(file_name)

class GraphToElementConverter:
    type_to_constructor = {
        "https://spdx.org/rdf/v3/Core/CreationInfo": CreationInfo,
        "https://spdx.org/rdf/v3/Core/Hash": Hash,
        "https://spdx.org/rdf/v3/Core/ExternalIdentifier": ExternalIdentifier,
        "https://spdx.org/rdf/v3/Core/ExternalReference": ExternalReference,
        "https://spdx.org/rdf/v3/Core/ExternalMap": ExternalMap,
        "https://spdx.org/rdf/v3/Core/SpdxDocument": SpdxDocument,
        "https://spdx.org/rdf/v3/Software/Package": Package,
        "https://spdx.org/rdf/v3/Software/File": File,
        "https://spdx.org/rdf/v3/Core/Relationship": Relationship,
        "https://spdx.org/rdf/v3/Core/Person": Relationship,
    }
    non_element_types = [
        "https://spdx.org/rdf/v3/Core/CreationInfo",
        "https://spdx.org/rdf/v3/Core/Hash",
        "https://spdx.org/rdf/v3/Core/ExternalIdentifier",
        "https://spdx.org/rdf/v3/Core/ExternalReference",
        "https://spdx.org/rdf/v3/Core/ExternalMap",
    ]

    cache = dict()

    def get_element_types(self) -> list[str]:
        return [type for type in self.type_to_constructor.keys() if type not in self.non_element_types]

    def __init__(self, graph: Graph, debug: bool = True):
        self.graph = graph
        self.namespace_manager = graph.namespace_manager
        self.debug = debug
        self.__debug_log_graph__()

    def n3(self, uri: IdentifiedNode) -> str:
        return uri.n3(self.namespace_manager)
    
    def __debug_log_namespaces__(self):
        if not self.debug:
            return
        for ns, url in self.namespace_manager.namespaces():
            print(f"DEBUG:   namespace: {ns} -> {url}")

    def __debug_log_graph__(self):
        if not self.debug:
            return
        print("DEBUG: graph:")
        print("DEBUG: START graph (serialized)...")
        print(self.graph.serialize(format='n3'))
        print("DEBUG: ...END graph (serialized)")
        self.__debug_log_namespaces__()
        for subject, predicate, object in self.graph:
            print(f"DEBUG:   {self.n3(subject)} {self.n3(predicate)} {self.n3(object)}", )

    def __debug_log_subject__(self, subject: IdentifiedNode):
        if not self.debug:
            return
        print("DEBUG: subject: ", subject)
        for predicate, object in self.graph.predicate_objects(subject=subject, unique=False):
            print(f"DEBUG:     {self.n3(predicate)} {self.n3(object)}")
    
    ####################################################################################################
    # low level functions

    def genSpdxURIRef(self, name: str, namespace: str = "Core") -> URIRef:
        return URIRef(f"https://spdx.org/rdf/v3/{namespace}/{name}")

    def getGraphValueRaw(self, subject: IdentifiedNode, predicate: IdentifiedNode, isMandatory: bool = False) -> str:
        value = self.graph.value(subject, predicate)
        if value is None:
            if isMandatory:
                raise Exception(f"no value for subject: {subject} and predicate: {predicate}")
            return None
        return value

    def getGraphValue(self, subject: IdentifiedNode, predicate: IdentifiedNode, isMandatory: bool = False) -> str:
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

    def getTypeOfSubject(self, subject: IdentifiedNode) -> str:
        predicate_for_type = RDF.type
        return self.getGraphValue(subject, predicate_for_type)

    def predicateToPythonArgsKey(self, predicate: IdentifiedNode) -> str:
        return camel_to_snake(predicate.split("/")[-1])
    
    def literalToPython(self, literal: Literal) -> any:
        datatype = literal.datatype
        if datatype == XSD.string:
            return literal.toPython()
        elif datatype == self.genSpdxURIRef("SemVer"):
            return Version(literal.toPython())
        elif datatype == self.genSpdxURIRef("DateTime"):
            return datetime_from_str(literal.toPython())
        else:
            self.__debug_log_subject__(subject)
            raise Exception(f"{self.n3(literal)} has unsupported datatype={literal.datatype}")

    def get_uriRef_as_enum(self, uriRef: URIRef) -> any:
        # TODO: upper snakecase
        uppercase_last_part = uriRef.split("/")[-1].upper()
        uriRefPython = uriRef.toPython()
        if uriRefPython.startswith(self.genSpdxURIRef("RelationshipType").toPython()):
            return RelationshipType(uppercase_last_part)
        # elif uriRef.toPython().startswith(self.genSpdxURIRef("HashAlgorithm").toPython()):
        #     return HashAlgorithm(uriRef.toPython())
        # elif uriRef.toPython().startswith(self.genSpdxURIRef("ProfileIdentifierType").toPython()):
        #     return ProfileIdentifierType(uriRef.toPython())
        else:
            return None

    def objectToPython(self, object: Identifier) -> any:
        if object == None:
            return None
        elif type(object) == None:
            raise Exception(f"{self.n3(object)} of has unsupported type=Enum?")
        elif isinstance(object, Literal):
            value = self.literalToPython(object)
            return value
        elif isinstance(object, URIRef):
            print("DEBUG:   URIRef:", object)
            maybe_enum = self.get_uriRef_as_enum(object)
            if maybe_enum is not None:
                return maybe_enum
            else:
                return self.getSubjectAsPythonObject(object)
        elif isinstance(object, BNode):
            print("DEBUG:   BNode:", object)
            return self.getSubjectAsPythonObject(object)
        elif isinstance(object, IdentifiedNode):
            print("DEBUG:   IdentifiedNode:", object)
            return self.getSubjectAsPythonObject(object)
        elif  isinstance(object, Variable):
            raise Exception(f"{self.n3(object)} of has unsupported type=Variable")
        elif  isinstance(object, Identifier):
            raise Exception(f"{self.n3(object)} of has unsupported type=Identifier")
        elif  isinstance(object, Node):
            raise Exception(f"{self.n3(object)} of has unsupported type=Node")
        else:
            raise Exception(f"{self.n3(object)} of has unsupported type={type(object)}")

    def key_of_type_is_list(self, type_of_subject: str, key: str) -> bool:
        if key in ["element", "root_element", "profile", "created_by"]:
            return True
        return False

    def values_of_key_of_type_are_refs(self, type_of_subject: str, key: str) -> bool:
        if self.key_of_type_is_list(type_of_subject, key):
            return True
        elif key in ["data_license", "from"]:
            return True
        return False

    def getArgsForSubject(self, subject: IdentifiedNode) -> dict:
        type_of_subject = self.getTypeOfSubject(subject)
        args = dict()
        for predicate, object in self.graph.predicate_objects(subject=subject, unique=False):
            if predicate == RDF.type:
                continue
            print("DEBUG:   parse:", predicate, object)

            key = self.predicateToPythonArgsKey(predicate)
            print(f"DEBUG:   {predicate} -> {key}") #   &&   {self.n3(object)} -> {value}")

            if self.values_of_key_of_type_are_refs(type_of_subject, key):
                value = object.toPython()
            else:
                value = self.objectToPython(object)

            if self.key_of_type_is_list(type_of_subject, key):
                if key not in args:
                    args[key] = []
                args[key].append(value)
            else:
                args[key] = value

        return args

    def applyArgsToConstructor(self, subject: IdentifiedNode, constructor, hasSpdxId: bool = False):
        args = self.getArgsForSubject(subject)
        if hasSpdxId:
            args["spdx_id"] = subject.toPython()
        print("DEBUG:   args:", args)
        return constructor(**args)

    def getSubjectAsPythonObject(self, subject: IdentifiedNode) -> any:
        if self.debug:
            print("\n")
            print("#"*80)
            print("DEBUG: subject:", subject)
        if subject in self.cache:
            if self.debug:
                print("DEBUG:   cache hit")
            return self.cache[subject]
        type_of_subject = self.getTypeOfSubject(subject)
        if self.debug:
            print("DEBUG: type_of_subject:", type_of_subject)
            self.__debug_log_subject__(subject)
        if type_of_subject is None:
            raise Exception(f"{subject} is not present as an object in the graph")
        if type_of_subject in self.type_to_constructor:
            hasSpdxId = type_of_subject not in self.non_element_types
            obj = self.applyArgsToConstructor(subject, self.type_to_constructor[type_of_subject], hasSpdxId=hasSpdxId)
            self.cache[subject] = obj
            return obj
        else:
            self.__debug_log_subject__(subject)
            raise Exception(f"{subject} has unsupported constructor type={type_of_subject}")

    def get_subjects(self, only_elements: bool = True) -> list[IdentifiedNode]:
        subjects = list(self.graph.subjects(unique=True))
        if only_elements:
            return [subject for subject in subjects if self.getTypeOfSubject(subject) in self.get_element_types()]
        else:
            return subjects

    def get_elements(self) -> list[Element]:
        return [self.getSubjectAsPythonObject(subject) for subject in self.get_subjects(only_elements=True)]

class JsonLDParser:
    def graphToPayload(self, graph: Graph) -> Payload:
        payload = Payload()

        converter = GraphToElementConverter(graph, True)
        for element in converter.get_elements():
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
