"""
Rather than representing these individual elements as full classes in the model,
we are using constants to represent them.
This is because they do not have any properties beyond their identifier, so a full class is unneeded.
"""

# Core profile individual elements
NO_ASSERTION_ELEMENT_ID: str = "https://spdx.org/rdf/3.0.1/terms/Core/NoAssertionElement"
NONE_ELEMENT_ID: str = "https://spdx.org/rdf/3.0.1/terms/Core/NoneElement"
SPDX_ORGANIZATION_ID: str = "https://spdx.org/rdf/3.0.1/terms/Core/SpdxOrganization"

# Expanded Licensing profile individual elements
NO_ASSERTION_LICENSE_ID: str = "https://spdx.org/rdf/3.0.1/terms/ExpandedLicensing/NoAssertionLicense"
NONE_LICENSE_ID: str = "https://spdx.org/rdf/3.0.1/terms/ExpandedLicensing/NoneLicense"
