#  SPDX-FileCopyrightText: 2023 spdx contributors
#
#  SPDX-License-Identifier: Apache-2.0
import logging
from datetime import datetime
from typing import List

from spdx_tools.common.spdx_licensing import spdx_licensing
from spdx_tools.spdx.model import (
    Actor,
    ActorType,
    Checksum,
    ChecksumAlgorithm,
    CreationInfo,
    Document,
    ExternalPackageRef,
    ExternalPackageRefCategory,
    File,
    FileType,
    Package,
    PackagePurpose,
    PackageVerificationCode,
    Relationship,
    RelationshipType,
)
from spdx_tools.spdx.validation.document_validator import validate_full_spdx_document
from spdx_tools.spdx.validation.validation_message import ValidationMessage
from spdx_tools.spdx.writer.write_anything import write_file

# This example shows how to use the spdx-tools to create an SPDX document from scratch,
# validate it and write it to a file.

# First up, we need general information about the creation of the document, summarised by the CreationInfo class.
creation_info = CreationInfo(
    spdx_version="SPDX-2.3",
    spdx_id="SPDXRef-DOCUMENT",
    name="document name",
    data_license="CC0-1.0",
    document_namespace="https://some.namespace",
    creators=[Actor(ActorType.PERSON, "Jane Doe", "jane.doe@example.com")],
    created=datetime(2022, 1, 1),
)

# creation_info is the only required property of the Document class (have a look there!), the rest are optional lists.
# So, we are set up to create a new document instance.
document = Document(creation_info)

# The document currently does not describe anything. Let's create a package that we can add to it.
# The Package class has quite a few properties (have a look there!),
# but only name, spdx_id and download_location are mandatory in SPDX v2.3.
package = Package(
    name="package name",
    spdx_id="SPDXRef-Package",
    download_location="https://download.com",
    version="2.2.1",
    file_name="./foo.bar",
    supplier=Actor(ActorType.PERSON, "Jane Doe", "jane.doe@example.com"),
    originator=Actor(ActorType.ORGANIZATION, "some organization", "contact@example.com"),
    files_analyzed=True,
    verification_code=PackageVerificationCode(
        value="d6a770ba38583ed4bb4525bd96e50461655d2758", excluded_files=["./some.file"]
    ),
    checksums=[
        Checksum(ChecksumAlgorithm.SHA1, "d6a770ba38583ed4bb4525bd96e50461655d2758"),
        Checksum(ChecksumAlgorithm.MD5, "624c1abb3664f4b35547e7c73864ad24"),
    ],
    license_concluded=spdx_licensing.parse("GPL-2.0-only OR MIT"),
    license_info_from_files=[spdx_licensing.parse("GPL-2.0-only"), spdx_licensing.parse("MIT")],
    license_declared=spdx_licensing.parse("GPL-2.0-only AND MIT"),
    license_comment="license comment",
    copyright_text="Copyright 2022 Jane Doe",
    description="package description",
    attribution_texts=["package attribution"],
    primary_package_purpose=PackagePurpose.LIBRARY,
    release_date=datetime(2015, 1, 1),
    external_references=[
        ExternalPackageRef(
            category=ExternalPackageRefCategory.OTHER,
            reference_type="http://reference.type",
            locator="reference/locator",
            comment="external reference comment",
        )
    ],
)

# Now that we have a package defined, we can add it to the document's package property.
document.packages = [package]

# A DESCRIBES relationship asserts that the document indeed describes the package.
describes_relationship = Relationship("SPDXRef-DOCUMENT", RelationshipType.DESCRIBES, "SPDXRef-Package")
document.relationships = [describes_relationship]

# Let's add two files. Have a look at the file class for all possible properties a file can have.
file1 = File(
    name="./package/file1.py",
    spdx_id="SPDXRef-File1",
    file_types=[FileType.SOURCE],
    checksums=[
        Checksum(ChecksumAlgorithm.SHA1, "d6a770ba38583ed4bb4525bd96e50461655d2758"),
        Checksum(ChecksumAlgorithm.MD5, "624c1abb3664f4b35547e7c73864ad24"),
    ],
    license_concluded=spdx_licensing.parse("MIT"),
    license_info_in_file=[spdx_licensing.parse("MIT")],
    copyright_text="Copyright 2022 Jane Doe",
)
file2 = File(
    name="./package/file2.py",
    spdx_id="SPDXRef-File2",
    checksums=[
        Checksum(ChecksumAlgorithm.SHA1, "d6a770ba38583ed4bb4525bd96e50461655d2759"),
    ],
    license_concluded=spdx_licensing.parse("GPL-2.0-only"),
)

# Assuming the package contains those two files, we create two CONTAINS relationships.
contains_relationship1 = Relationship("SPDXRef-Package", RelationshipType.CONTAINS, "SPDXRef-File1")
contains_relationship2 = Relationship("SPDXRef-Package", RelationshipType.CONTAINS, "SPDXRef-File2")

# This library uses run-time type checks when assigning properties.
# Because in-place alterations like .append() circumvent these checks, we don't use them here.
document.relationships += [contains_relationship1, contains_relationship2]
document.files += [file1, file2]

# We now have created a document with basic creation information, describing a package that contains two files.
# You can also add Annotations, Snippets and ExtractedLicensingInfo to the document in an analogous manner to the above.
# Have a look at their respective classes if you are unsure about their properties.


# This library provides comprehensive validation against the SPDX specification.
# Note that details of the validation depend on the SPDX version of the document.
validation_messages: List[ValidationMessage] = validate_full_spdx_document(document)

# You can have a look at each entry's message and context (like spdx_id, parent_id, full_element)
# which will help you pinpoint the location of the invalidity.
for message in validation_messages:
    logging.warning(message.validation_message)
    logging.warning(message.context)

# If the document is valid, validation_messages will be empty.
assert validation_messages == []

# Finally, we can serialize the document to any of the five supported formats.
# Using the write_file() method from the write_anything module,
# the format will be determined by the file ending: .spdx (tag-value), .json, .xml, .yaml. or .rdf (or .rdf.xml)
write_file(document, "my_spdx_document.spdx.json")
