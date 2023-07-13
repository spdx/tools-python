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


def package_to_rdf(obj, graph: Graph) -> Identifier:
    if '_spdx_id' in obj.__dict__:
        element_node = URIRef(obj.spdx_id)
    else:
        element_node = BNode()
    type_node = URIRef("https://spdx.org/rdf/v3/Software/Package")
    graph.add((element_node, RDF.type, type_node))
    package_properties_to_rdf(element_node, obj, graph)
    return element_node


def package_properties_to_rdf(node: Identifier, obj, graph: Graph):
    from .converter import model_to_rdf
    if obj.package_version is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Software/packageVersion")
        graph.add((node, prop_node, model_to_rdf(obj.package_version, graph)))
    if obj.download_location is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Software/downloadLocation")
        graph.add((node, prop_node, model_to_rdf(obj.download_location, graph)))
    if obj.package_url is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Software/packageUrl")
        graph.add((node, prop_node, model_to_rdf(obj.package_url, graph)))
    if obj.homepage is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Software/homePage")
        graph.add((node, prop_node, model_to_rdf(obj.homepage, graph)))
    if obj.source_info is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Software/sourceInfo")
        graph.add((node, prop_node, model_to_rdf(obj.source_info, graph)))
    software.software_artifact_properties_to_rdf(node, obj, graph)


def file_to_rdf(obj, graph: Graph) -> Identifier:
    if '_spdx_id' in obj.__dict__:
        element_node = URIRef(obj.spdx_id)
    else:
        element_node = BNode()
    type_node = URIRef("https://spdx.org/rdf/v3/Software/File")
    graph.add((element_node, RDF.type, type_node))
    file_properties_to_rdf(element_node, obj, graph)
    return element_node


def file_properties_to_rdf(node: Identifier, obj, graph: Graph):
    from .converter import model_to_rdf
    if obj.content_type is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Software/contentType")
        graph.add((node, prop_node, model_to_rdf(obj.content_type, graph)))
    software.software_artifact_properties_to_rdf(node, obj, graph)


def snippet_to_rdf(obj, graph: Graph) -> Identifier:
    if '_spdx_id' in obj.__dict__:
        element_node = URIRef(obj.spdx_id)
    else:
        element_node = BNode()
    type_node = URIRef("https://spdx.org/rdf/v3/Software/Snippet")
    graph.add((element_node, RDF.type, type_node))
    snippet_properties_to_rdf(element_node, obj, graph)
    return element_node


def snippet_properties_to_rdf(node: Identifier, obj, graph: Graph):
    from .converter import model_to_rdf
    if obj.byte_range is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Software/byteRange")
        graph.add((node, prop_node, model_to_rdf(obj.byte_range, graph)))
    if obj.line_range is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Software/lineRange")
        graph.add((node, prop_node, model_to_rdf(obj.line_range, graph)))
    software.software_artifact_properties_to_rdf(node, obj, graph)


def sbom_to_rdf(obj, graph: Graph) -> Identifier:
    if '_spdx_id' in obj.__dict__:
        element_node = URIRef(obj.spdx_id)
    else:
        element_node = BNode()
    type_node = URIRef("https://spdx.org/rdf/v3/Software/Sbom")
    graph.add((element_node, RDF.type, type_node))
    sbom_properties_to_rdf(element_node, obj, graph)
    return element_node


def sbom_properties_to_rdf(node: Identifier, obj, graph: Graph):
    from .converter import model_to_rdf
    for value in obj.sbom_type:
        prop_node = URIRef("https://spdx.org/rdf/v3/Software/sbomType")
        graph.add((node, prop_node, model_to_rdf(value, graph)))
    core.bom_properties_to_rdf(node, obj, graph)


def software_artifact_to_rdf(obj, graph: Graph) -> Identifier:
    if '_spdx_id' in obj.__dict__:
        element_node = URIRef(obj.spdx_id)
    else:
        element_node = BNode()
    type_node = URIRef("https://spdx.org/rdf/v3/Software/SoftwareArtifact")
    graph.add((element_node, RDF.type, type_node))
    software_artifact_properties_to_rdf(element_node, obj, graph)
    return element_node


def software_artifact_properties_to_rdf(node: Identifier, obj, graph: Graph):
    from .converter import model_to_rdf
    if obj.content_identifier is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Software/contentIdentifier")
        graph.add((node, prop_node, model_to_rdf(obj.content_identifier, graph)))
    if obj.primary_purpose is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Software/primaryPurpose")
        graph.add((node, prop_node, model_to_rdf(obj.primary_purpose, graph)))
    for value in obj.additional_purpose:
        prop_node = URIRef("https://spdx.org/rdf/v3/Software/additionalPurpose")
        graph.add((node, prop_node, model_to_rdf(value, graph)))
    if obj.concluded_license is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Software/concludedLicense")
        graph.add((node, prop_node, model_to_rdf(obj.concluded_license, graph)))
    if obj.declared_license is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Software/declaredLicense")
        graph.add((node, prop_node, model_to_rdf(obj.declared_license, graph)))
    if obj.copyright_text is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Software/copyrightText")
        graph.add((node, prop_node, model_to_rdf(obj.copyright_text, graph)))
    if obj.attribution_text is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Software/attributionText")
        graph.add((node, prop_node, model_to_rdf(obj.attribution_text, graph)))
    core.artifact_properties_to_rdf(node, obj, graph)


def software_dependency_relationship_to_rdf(obj, graph: Graph) -> Identifier:
    if '_spdx_id' in obj.__dict__:
        element_node = URIRef(obj.spdx_id)
    else:
        element_node = BNode()
    type_node = URIRef("https://spdx.org/rdf/v3/Software/SoftwareDependencyRelationship")
    graph.add((element_node, RDF.type, type_node))
    software_dependency_relationship_properties_to_rdf(element_node, obj, graph)
    return element_node


def software_dependency_relationship_properties_to_rdf(node: Identifier, obj, graph: Graph):
    from .converter import model_to_rdf
    if obj.software_linkage is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Software/softwareLinkage")
        graph.add((node, prop_node, model_to_rdf(obj.software_linkage, graph)))
    if obj.conditionality is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Software/conditionality")
        graph.add((node, prop_node, model_to_rdf(obj.conditionality, graph)))
    core.lifecycle_scoped_relationship_properties_to_rdf(node, obj, graph)


def dependency_conditionality_type_to_rdf(obj, graph: Graph) -> Identifier:
    from .converter import enum_value_to_str
    name = enum_value_to_str(obj)
    return URIRef("https://spdx.org/rdf/v3/Software/DependencyConditionalityType/" + name)


def software_purpose_to_rdf(obj, graph: Graph) -> Identifier:
    from .converter import enum_value_to_str
    name = enum_value_to_str(obj)
    return URIRef("https://spdx.org/rdf/v3/Software/SoftwarePurpose/" + name)


def software_dependency_link_type_to_rdf(obj, graph: Graph) -> Identifier:
    from .converter import enum_value_to_str
    name = enum_value_to_str(obj)
    return URIRef("https://spdx.org/rdf/v3/Software/SoftwareDependencyLinkType/" + name)


def sbom_type_to_rdf(obj, graph: Graph) -> Identifier:
    from .converter import enum_value_to_str
    name = enum_value_to_str(obj)
    return URIRef("https://spdx.org/rdf/v3/Software/SbomType/" + name)


# fmt: on