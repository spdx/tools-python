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

from rdflib import Graph, RDF

from spdx.parser.rdf.extracted_licensing_info_parser import parse_extracted_licensing_info
from spdx.rdfschema.namespace import SPDX_NAMESPACE


def test_parse_extracted_licensing_info():
    graph = Graph().parse(os.path.join(os.path.dirname(__file__), "data/file_to_test_rdf_parser.rdf.xml"))
    doc_node = graph.value(predicate=RDF.type, object=SPDX_NAMESPACE.SpdxDocument)
    extracted_licensing_info_node = graph.value(subject=doc_node, predicate=SPDX_NAMESPACE.hasExtractedLicensingInfo)

    extracted_licensing_info = parse_extracted_licensing_info(extracted_licensing_info_node, graph)

    assert extracted_licensing_info.license_id == "LicenseRef-1"
    assert extracted_licensing_info.extracted_text == "extractedText"
    assert extracted_licensing_info.comment == "licenseComment"
    assert extracted_licensing_info.license_name == "licenseName"
    assert extracted_licensing_info.cross_references == ["https://see.also"]
