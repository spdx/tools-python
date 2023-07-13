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


def vex_not_affected_vuln_assessment_relationship_to_rdf(obj, graph: Graph) -> Identifier:
    if '_spdx_id' in obj.__dict__:
        element_node = URIRef(obj.spdx_id)
    else:
        element_node = BNode()
    type_node = URIRef("https://spdx.org/rdf/v3/Security/VexNotAffectedVulnAssessmentRelationship")
    graph.add((element_node, RDF.type, type_node))
    vex_not_affected_vuln_assessment_relationship_properties_to_rdf(element_node, obj, graph)
    return element_node


def vex_not_affected_vuln_assessment_relationship_properties_to_rdf(node: Identifier, obj, graph: Graph):
    from .converter import model_to_rdf
    if obj.justification_type is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/justificationType")
        value = obj.justification_type
        graph.add((node, prop_node, model_to_rdf(value, graph)))
    if obj.impact_statement is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/impactStatement")
        value = obj.impact_statement
        graph.add((node, prop_node, Literal(value, datatype="http://www.w3.org/2001/XMLSchema#string")))
    if obj.impact_statement_time is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/impactStatementTime")
        value = obj.impact_statement_time
        graph.add((node, prop_node, Literal(value, datatype="https://spdx.org/rdf/v3//Core/DateTime")))
    security.vex_vuln_assessment_relationship_properties_to_rdf(node, obj, graph)


def ssvc_vuln_assessment_relationship_to_rdf(obj, graph: Graph) -> Identifier:
    if '_spdx_id' in obj.__dict__:
        element_node = URIRef(obj.spdx_id)
    else:
        element_node = BNode()
    type_node = URIRef("https://spdx.org/rdf/v3/Security/SsvcVulnAssessmentRelationship")
    graph.add((element_node, RDF.type, type_node))
    ssvc_vuln_assessment_relationship_properties_to_rdf(element_node, obj, graph)
    return element_node


def ssvc_vuln_assessment_relationship_properties_to_rdf(node: Identifier, obj, graph: Graph):
    from .converter import model_to_rdf
    if obj.decision_type is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/decisionType")
        value = obj.decision_type
        graph.add((node, prop_node, model_to_rdf(value, graph)))
    security.vuln_assessment_relationship_properties_to_rdf(node, obj, graph)


def vex_fixed_vuln_assessment_relationship_to_rdf(obj, graph: Graph) -> Identifier:
    if '_spdx_id' in obj.__dict__:
        element_node = URIRef(obj.spdx_id)
    else:
        element_node = BNode()
    type_node = URIRef("https://spdx.org/rdf/v3/Security/VexFixedVulnAssessmentRelationship")
    graph.add((element_node, RDF.type, type_node))
    vex_fixed_vuln_assessment_relationship_properties_to_rdf(element_node, obj, graph)
    return element_node


def vex_fixed_vuln_assessment_relationship_properties_to_rdf(node: Identifier, obj, graph: Graph):
    from .converter import model_to_rdf
    security.vex_vuln_assessment_relationship_properties_to_rdf(node, obj, graph)


def vex_vuln_assessment_relationship_to_rdf(obj, graph: Graph) -> Identifier:
    if '_spdx_id' in obj.__dict__:
        element_node = URIRef(obj.spdx_id)
    else:
        element_node = BNode()
    type_node = URIRef("https://spdx.org/rdf/v3/Security/VexVulnAssessmentRelationship")
    graph.add((element_node, RDF.type, type_node))
    vex_vuln_assessment_relationship_properties_to_rdf(element_node, obj, graph)
    return element_node


def vex_vuln_assessment_relationship_properties_to_rdf(node: Identifier, obj, graph: Graph):
    from .converter import model_to_rdf
    if obj.vex_version is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/vexVersion")
        value = obj.vex_version
        graph.add((node, prop_node, Literal(value, datatype="http://www.w3.org/2001/XMLSchema#string")))
    if obj.status_notes is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/statusNotes")
        value = obj.status_notes
        graph.add((node, prop_node, Literal(value, datatype="http://www.w3.org/2001/XMLSchema#string")))
    security.vuln_assessment_relationship_properties_to_rdf(node, obj, graph)


def cvss_v3_vuln_assessment_relationship_to_rdf(obj, graph: Graph) -> Identifier:
    if '_spdx_id' in obj.__dict__:
        element_node = URIRef(obj.spdx_id)
    else:
        element_node = BNode()
    type_node = URIRef("https://spdx.org/rdf/v3/Security/CvssV3VulnAssessmentRelationship")
    graph.add((element_node, RDF.type, type_node))
    cvss_v3_vuln_assessment_relationship_properties_to_rdf(element_node, obj, graph)
    return element_node


def cvss_v3_vuln_assessment_relationship_properties_to_rdf(node: Identifier, obj, graph: Graph):
    from .converter import model_to_rdf
    if obj.score is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/score")
        value = obj.score
        graph.add((node, prop_node, Literal(value, datatype="http://www.w3.org/2001/XMLSchema#decimal")))
    if obj.severity is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/severity")
        value = obj.severity
        graph.add((node, prop_node, Literal(value, datatype="http://www.w3.org/2001/XMLSchema#string")))
    if obj.vector is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/vector")
        value = obj.vector
        graph.add((node, prop_node, Literal(value, datatype="http://www.w3.org/2001/XMLSchema#string")))
    security.vuln_assessment_relationship_properties_to_rdf(node, obj, graph)


def vuln_assessment_relationship_to_rdf(obj, graph: Graph) -> Identifier:
    if '_spdx_id' in obj.__dict__:
        element_node = URIRef(obj.spdx_id)
    else:
        element_node = BNode()
    type_node = URIRef("https://spdx.org/rdf/v3/Security/VulnAssessmentRelationship")
    graph.add((element_node, RDF.type, type_node))
    vuln_assessment_relationship_properties_to_rdf(element_node, obj, graph)
    return element_node


def vuln_assessment_relationship_properties_to_rdf(node: Identifier, obj, graph: Graph):
    from .converter import model_to_rdf
    if obj.assessed_element is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/assessedElement")
        value = obj.assessed_element
        graph.add((node, prop_node, Literal(value, datatype="https://spdx.org/rdf/v3//Core/Element")))
    if obj.published_time is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/publishedTime")
        value = obj.published_time
        graph.add((node, prop_node, Literal(value, datatype="https://spdx.org/rdf/v3//Core/DateTime")))
    if obj.supplied_by is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/suppliedBy")
        value = obj.supplied_by
        graph.add((node, prop_node, Literal(value, datatype="https://spdx.org/rdf/v3//Core/Agent")))
    if obj.modified_time is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/modifiedTime")
        value = obj.modified_time
        graph.add((node, prop_node, Literal(value, datatype="https://spdx.org/rdf/v3//Core/DateTime")))
    if obj.withdrawn_time is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/withdrawnTime")
        value = obj.withdrawn_time
        graph.add((node, prop_node, Literal(value, datatype="https://spdx.org/rdf/v3//Core/DateTime")))
    core.relationship_properties_to_rdf(node, obj, graph)


def vulnerability_to_rdf(obj, graph: Graph) -> Identifier:
    if '_spdx_id' in obj.__dict__:
        element_node = URIRef(obj.spdx_id)
    else:
        element_node = BNode()
    type_node = URIRef("https://spdx.org/rdf/v3/Security/Vulnerability")
    graph.add((element_node, RDF.type, type_node))
    vulnerability_properties_to_rdf(element_node, obj, graph)
    return element_node


def vulnerability_properties_to_rdf(node: Identifier, obj, graph: Graph):
    from .converter import model_to_rdf
    if obj.published_time is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/publishedTime")
        value = obj.published_time
        graph.add((node, prop_node, Literal(value, datatype="https://spdx.org/rdf/v3//Core/DateTime")))
    if obj.modified_time is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/modifiedTime")
        value = obj.modified_time
        graph.add((node, prop_node, Literal(value, datatype="https://spdx.org/rdf/v3//Core/DateTime")))
    if obj.withdrawn_time is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/withdrawnTime")
        value = obj.withdrawn_time
        graph.add((node, prop_node, Literal(value, datatype="https://spdx.org/rdf/v3//Core/DateTime")))
    core.element_properties_to_rdf(node, obj, graph)


def cvss_v2_vuln_assessment_relationship_to_rdf(obj, graph: Graph) -> Identifier:
    if '_spdx_id' in obj.__dict__:
        element_node = URIRef(obj.spdx_id)
    else:
        element_node = BNode()
    type_node = URIRef("https://spdx.org/rdf/v3/Security/CvssV2VulnAssessmentRelationship")
    graph.add((element_node, RDF.type, type_node))
    cvss_v2_vuln_assessment_relationship_properties_to_rdf(element_node, obj, graph)
    return element_node


def cvss_v2_vuln_assessment_relationship_properties_to_rdf(node: Identifier, obj, graph: Graph):
    from .converter import model_to_rdf
    if obj.score is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/score")
        value = obj.score
        graph.add((node, prop_node, Literal(value, datatype="http://www.w3.org/2001/XMLSchema#decimal")))
    if obj.severity is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/severity")
        value = obj.severity
        graph.add((node, prop_node, Literal(value, datatype="http://www.w3.org/2001/XMLSchema#string")))
    if obj.vector is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/vector")
        value = obj.vector
        graph.add((node, prop_node, Literal(value, datatype="http://www.w3.org/2001/XMLSchema#string")))
    security.vuln_assessment_relationship_properties_to_rdf(node, obj, graph)


def vex_affected_vuln_assessment_relationship_to_rdf(obj, graph: Graph) -> Identifier:
    if '_spdx_id' in obj.__dict__:
        element_node = URIRef(obj.spdx_id)
    else:
        element_node = BNode()
    type_node = URIRef("https://spdx.org/rdf/v3/Security/VexAffectedVulnAssessmentRelationship")
    graph.add((element_node, RDF.type, type_node))
    vex_affected_vuln_assessment_relationship_properties_to_rdf(element_node, obj, graph)
    return element_node


def vex_affected_vuln_assessment_relationship_properties_to_rdf(node: Identifier, obj, graph: Graph):
    from .converter import model_to_rdf
    if obj.action_statement is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/actionStatement")
        value = obj.action_statement
        graph.add((node, prop_node, Literal(value, datatype="http://www.w3.org/2001/XMLSchema#string")))
    for value in obj.action_statement_time:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/actionStatementTime")
        graph.add((node, prop_node, Literal(value, datatype="https://spdx.org/rdf/v3//Core/DateTime")))
    security.vex_vuln_assessment_relationship_properties_to_rdf(node, obj, graph)


def exploit_catalog_vuln_assessment_relationship_to_rdf(obj, graph: Graph) -> Identifier:
    if '_spdx_id' in obj.__dict__:
        element_node = URIRef(obj.spdx_id)
    else:
        element_node = BNode()
    type_node = URIRef("https://spdx.org/rdf/v3/Security/ExploitCatalogVulnAssessmentRelationship")
    graph.add((element_node, RDF.type, type_node))
    exploit_catalog_vuln_assessment_relationship_properties_to_rdf(element_node, obj, graph)
    return element_node


def exploit_catalog_vuln_assessment_relationship_properties_to_rdf(node: Identifier, obj, graph: Graph):
    from .converter import model_to_rdf
    if obj.catalog_type is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/catalogType")
        value = obj.catalog_type
        graph.add((node, prop_node, model_to_rdf(value, graph)))
    if obj.exploited is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/exploited")
        value = obj.exploited
        graph.add((node, prop_node, Literal(value, datatype="http://www.w3.org/2001/XMLSchema#boolean")))
    if obj.locator is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/locator")
        value = obj.locator
        graph.add((node, prop_node, Literal(value, datatype="http://www.w3.org/2001/XMLSchema#anyURI")))
    security.vuln_assessment_relationship_properties_to_rdf(node, obj, graph)


def epss_vuln_assessment_relationship_to_rdf(obj, graph: Graph) -> Identifier:
    if '_spdx_id' in obj.__dict__:
        element_node = URIRef(obj.spdx_id)
    else:
        element_node = BNode()
    type_node = URIRef("https://spdx.org/rdf/v3/Security/EpssVulnAssessmentRelationship")
    graph.add((element_node, RDF.type, type_node))
    epss_vuln_assessment_relationship_properties_to_rdf(element_node, obj, graph)
    return element_node


def epss_vuln_assessment_relationship_properties_to_rdf(node: Identifier, obj, graph: Graph):
    from .converter import model_to_rdf
    if obj.probability is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/probability")
        value = obj.probability
        graph.add((node, prop_node, Literal(value, datatype="http://www.w3.org/2001/XMLSchema#nonNegativeInteger")))
    if obj.severity is not None:
        prop_node = URIRef("https://spdx.org/rdf/v3/Security/severity")
        value = obj.severity
        graph.add((node, prop_node, Literal(value, datatype="http://www.w3.org/2001/XMLSchema#string")))
    security.vuln_assessment_relationship_properties_to_rdf(node, obj, graph)


def vex_under_investigation_vuln_assessment_relationship_to_rdf(obj, graph: Graph) -> Identifier:
    if '_spdx_id' in obj.__dict__:
        element_node = URIRef(obj.spdx_id)
    else:
        element_node = BNode()
    type_node = URIRef("https://spdx.org/rdf/v3/Security/VexUnderInvestigationVulnAssessmentRelationship")
    graph.add((element_node, RDF.type, type_node))
    vex_under_investigation_vuln_assessment_relationship_properties_to_rdf(element_node, obj, graph)
    return element_node


def vex_under_investigation_vuln_assessment_relationship_properties_to_rdf(node: Identifier, obj, graph: Graph):
    from .converter import model_to_rdf
    security.vex_vuln_assessment_relationship_properties_to_rdf(node, obj, graph)


def vex_justification_type_to_rdf(obj, graph: Graph) -> Identifier:
    from .converter import enum_value_to_str
    name = enum_value_to_str(obj)
    return URIRef("https://spdx.org/rdf/v3/Security/VexJustificationType/" + name)


def exploit_catalog_type_to_rdf(obj, graph: Graph) -> Identifier:
    from .converter import enum_value_to_str
    name = enum_value_to_str(obj)
    return URIRef("https://spdx.org/rdf/v3/Security/ExploitCatalogType/" + name)


def ssvc_decision_type_to_rdf(obj, graph: Graph) -> Identifier:
    from .converter import enum_value_to_str
    name = enum_value_to_str(obj)
    return URIRef("https://spdx.org/rdf/v3/Security/SsvcDecisionType/" + name)


# fmt: on
