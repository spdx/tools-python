# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from beartype.typing import Any, Type

from spdx_tools.spdx.datetime_conversions import datetime_to_iso_string
from spdx_tools.spdx.jsonschema.annotation_converter import AnnotationConverter
from spdx_tools.spdx.jsonschema.checksum_converter import ChecksumConverter
from spdx_tools.spdx.jsonschema.converter import TypedConverter
from spdx_tools.spdx.jsonschema.external_package_ref_converter import ExternalPackageRefConverter
from spdx_tools.spdx.jsonschema.json_property import JsonProperty
from spdx_tools.spdx.jsonschema.optional_utils import apply_if_present
from spdx_tools.spdx.jsonschema.package_properties import PackageProperty
from spdx_tools.spdx.jsonschema.package_verification_code_converter import PackageVerificationCodeConverter
from spdx_tools.spdx.model import Actor, Document, Package


class PackageConverter(TypedConverter[Package]):
    annotation_converter: AnnotationConverter
    checksum_converter: ChecksumConverter
    external_package_ref_converter: ExternalPackageRefConverter
    package_verification_code_converter: PackageVerificationCodeConverter

    def __init__(self):
        self.annotation_converter = AnnotationConverter()
        self.checksum_converter = ChecksumConverter()
        self.external_package_ref_converter = ExternalPackageRefConverter()
        self.package_verification_code_converter = PackageVerificationCodeConverter()

    def json_property_name(self, package_property: PackageProperty) -> str:
        if package_property == PackageProperty.SPDX_ID:
            return "SPDXID"
        return super().json_property_name(package_property)

    def _get_property_value(
        self, package: Package, package_property: PackageProperty, document: Document = None
    ) -> Any:
        if package_property == PackageProperty.SPDX_ID:
            return package.spdx_id
        elif package_property == PackageProperty.ANNOTATIONS:
            package_annotations = filter(
                lambda annotation: annotation.spdx_id == package.spdx_id, document.annotations
            )
            return [
                self.annotation_converter.convert(annotation, document) for annotation in package_annotations
            ] or None
        elif package_property == PackageProperty.ATTRIBUTION_TEXTS:
            return package.attribution_texts or None
        elif package_property == PackageProperty.BUILT_DATE:
            return apply_if_present(datetime_to_iso_string, package.built_date)
        elif package_property == PackageProperty.CHECKSUMS:
            return [self.checksum_converter.convert(checksum, document) for checksum in package.checksums] or None
        elif package_property == PackageProperty.COMMENT:
            return package.comment
        elif package_property == PackageProperty.COPYRIGHT_TEXT:
            return apply_if_present(str, package.copyright_text)
        elif package_property == PackageProperty.DESCRIPTION:
            return package.description
        elif package_property == PackageProperty.DOWNLOAD_LOCATION:
            return str(package.download_location)
        elif package_property == PackageProperty.EXTERNAL_REFS:
            return [
                self.external_package_ref_converter.convert(external_ref)
                for external_ref in package.external_references
            ] or None
        elif package_property == PackageProperty.FILES_ANALYZED:
            return package.files_analyzed
        elif package_property == PackageProperty.HOMEPAGE:
            return apply_if_present(str, package.homepage)
        elif package_property == PackageProperty.LICENSE_COMMENTS:
            return package.license_comment
        elif package_property == PackageProperty.LICENSE_CONCLUDED:
            return apply_if_present(str, package.license_concluded)
        elif package_property == PackageProperty.LICENSE_DECLARED:
            return apply_if_present(str, package.license_declared)
        elif package_property == PackageProperty.LICENSE_INFO_FROM_FILES:
            return [str(license_expression) for license_expression in package.license_info_from_files] or None
        elif package_property == PackageProperty.NAME:
            return package.name
        elif package_property == PackageProperty.ORIGINATOR:
            if isinstance(package.originator, Actor):
                return package.originator.to_serialized_string()
            return apply_if_present(str, package.originator)
        elif package_property == PackageProperty.PACKAGE_FILE_NAME:
            return package.file_name
        elif package_property == PackageProperty.PACKAGE_VERIFICATION_CODE:
            return apply_if_present(self.package_verification_code_converter.convert, package.verification_code)
        elif package_property == PackageProperty.PRIMARY_PACKAGE_PURPOSE:
            return package.primary_package_purpose.name if package.primary_package_purpose is not None else None
        elif package_property == PackageProperty.RELEASE_DATE:
            return apply_if_present(datetime_to_iso_string, package.release_date)
        elif package_property == PackageProperty.SOURCE_INFO:
            return package.source_info
        elif package_property == PackageProperty.SUMMARY:
            return package.summary
        elif package_property == PackageProperty.SUPPLIER:
            if isinstance(package.supplier, Actor):
                return package.supplier.to_serialized_string()
            return apply_if_present(str, package.supplier)
        elif package_property == PackageProperty.VALID_UNTIL_DATE:
            return apply_if_present(datetime_to_iso_string, package.valid_until_date)
        elif package_property == PackageProperty.VERSION_INFO:
            return package.version

    def get_json_type(self) -> Type[JsonProperty]:
        return PackageProperty

    def get_data_model_type(self) -> Type[Package]:
        return Package

    def requires_full_document(self) -> bool:
        return True
