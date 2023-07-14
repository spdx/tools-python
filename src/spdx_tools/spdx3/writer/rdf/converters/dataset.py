# SPDX-License-Identifier: Apache-2.0
#
# This file was auto-generated by dev/gen_model_to_rdf.py
# Do not manually edit!
# flake8: noqa
# isort:skip_file

# fmt: off

from rdflib import Graph, URIRef, RDF, Literal, BNode
from rdflib.term import Identifier
from spdx_tools.spdx.casing_tools import snake_case_to_camel_case
from . import expanded_license, core, dataset, licensing, ai, security, build, software


def dataset_to_rdf(obj, graph: Graph) -> Identifier:
    if '_spdx_id' in obj.__dict__:
        element_node = URIRef(obj.spdx_id)
    else:
        element_node = BNode()
    type_node = URIRef("https://spdx.org/rdf/v3/Dataset/Dataset")
    graph.add((element_node, RDF.type, type_node))
    dataset_properties_to_rdf(element_node, obj, graph)
    return element_node


def dataset_properties_to_rdf(node: Identifier, obj, graph: Graph):
    from .converter import model_to_rdf
    for value in obj.dataset_type:
        prop_node = URIRef("https://spdx.org/rdf/v3/Dataset/datasetType")
        graph.add((node, prop_node, model_to_rdf(value, graph)))
    if obj.data_collection_process is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Dataset/dataCollectionProcess")
        value = obj.data_collection_process
        graph.add((node, prop_node, Literal(value, datatype="http://www.w3.org/2001/XMLSchema#string")))
    if obj.intended_use is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Dataset/intendedUse")
        value = obj.intended_use
        graph.add((node, prop_node, Literal(value, datatype="http://www.w3.org/2001/XMLSchema#string")))
    if obj.dataset_size is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Dataset/datasetSize")
        value = obj.dataset_size
        graph.add((node, prop_node, Literal(value, datatype="http://www.w3.org/2001/XMLSchema#nonNegativeInteger")))
    if obj.dataset_noise is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Dataset/datasetNoise")
        value = obj.dataset_noise
        graph.add((node, prop_node, Literal(value, datatype="http://www.w3.org/2001/XMLSchema#string")))
    for value in obj.data_preprocessing:
        prop_node = URIRef("https://spdx.org/rdf/v3/Dataset/dataPreprocessing")
        graph.add((node, prop_node, Literal(value, datatype="http://www.w3.org/2001/XMLSchema#string")))
    for value in obj.sensor:
        prop_node = URIRef("https://spdx.org/rdf/v3/Dataset/sensor")
        graph.add((node, prop_node, model_to_rdf(value, graph)))
    for value in obj.known_bias:
        prop_node = URIRef("https://spdx.org/rdf/v3/Dataset/knownBias")
        graph.add((node, prop_node, Literal(value, datatype="http://www.w3.org/2001/XMLSchema#string")))
    if obj.sensitive_personal_information is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Dataset/sensitivePersonalInformation")
        value = obj.sensitive_personal_information
        graph.add((node, prop_node, Literal(value, datatype="https://spdx.org/rdf/v3/Dataset/PresenceType")))
    for value in obj.anonymization_method_used:
        prop_node = URIRef("https://spdx.org/rdf/v3/Dataset/anonymizationMethodUsed")
        graph.add((node, prop_node, Literal(value, datatype="http://www.w3.org/2001/XMLSchema#string")))
    if obj.confidentiality_level is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Dataset/confidentialityLevel")
        value = obj.confidentiality_level
        graph.add((node, prop_node, model_to_rdf(value, graph)))
    if obj.dataset_update_mechanism is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Dataset/datasetUpdateMechanism")
        value = obj.dataset_update_mechanism
        graph.add((node, prop_node, Literal(value, datatype="http://www.w3.org/2001/XMLSchema#string")))
    if obj.dataset_availability is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Dataset/datasetAvailability")
        value = obj.dataset_availability
        graph.add((node, prop_node, model_to_rdf(value, graph)))
    software.package_properties_to_rdf(node, obj, graph)


def dataset_type_to_rdf(obj, graph: Graph) -> Identifier:
    from .converter import enum_value_to_str
    name = enum_value_to_str(obj)
    return URIRef("https://spdx.org/rdf/v3/Dataset/DatasetType/" + name)


def dataset_availability_type_to_rdf(obj, graph: Graph) -> Identifier:
    from .converter import enum_value_to_str
    name = enum_value_to_str(obj)
    return URIRef("https://spdx.org/rdf/v3/Dataset/DatasetAvailabilityType/" + name)


def confidentiality_level_type_to_rdf(obj, graph: Graph) -> Identifier:
    from .converter import enum_value_to_str
    name = enum_value_to_str(obj)
    return URIRef("https://spdx.org/rdf/v3/Dataset/ConfidentialityLevelType/" + name)


# fmt: on
