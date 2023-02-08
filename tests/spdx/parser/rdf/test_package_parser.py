# Copyright (c) 2023 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

from rdflib import RDF, Graph

from spdx.model.actor import Actor, ActorType
from spdx.model.checksum import ChecksumAlgorithm, Checksum
from spdx.model.package import PackagePurpose, PackageVerificationCode
from spdx.parser.rdf.package_parser import parse_package
from spdx.rdfschema.namespace import SPDX_NAMESPACE


def test_package_parser():
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/file_to_test_rdf_parser.rdf.xml"))
    package_node = graph.value(predicate=RDF.type, object=SPDX_NAMESPACE.Package)
    doc_namespace = "https://some.namespace"

    package = parse_package(package_node, graph, doc_namespace)

    assert package.spdx_id == "SPDXRef-Package"
    assert package.name == "packageName"
    assert package.download_location == "https://download.com"
    assert package.version == "12.2"
    assert package.file_name == "./packageFileName"
    assert package.homepage == "https://homepage.com"
    assert package.files_analyzed == True
    assert package.checksums == [Checksum(ChecksumAlgorithm.SHA1, "71c4025dd9897b364f3ebbb42c484ff43d00791c")]
    assert package.source_info == "sourceInfo"
    assert package.license_comment == "packageLicenseComment"
    assert package.copyright_text == "packageCopyrightText"
    assert package.verification_code == PackageVerificationCode(value="85ed0817af83a24ad8da68c2b5094de69833983c",
                                                                excluded_files=["./exclude.py"])
    assert package.summary == "packageSummary"
    assert package.description == "packageDescription"
    assert package.comment == "packageComment"
    assert package.attribution_texts == ["packageAttributionText"]
    assert package.primary_package_purpose == PackagePurpose.SOURCE
    assert package.supplier == Actor(ActorType.PERSON, "supplierName", "some@mail.com")
    assert package.originator == Actor(ActorType.PERSON, "originatorName", "some@mail.com")
