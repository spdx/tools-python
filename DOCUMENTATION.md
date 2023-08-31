# Code architecture documentation

## Package Overview
Beneath the top-level package `spdx_tools` you will find three sub-packages:
- `spdx`, which contains the code to create, parse, write and validate SPDX documents of versions 2.2 and 2.3
- `spdx3`, which will contain the same feature set for versions 3.x once they are released
- `common`, which contains code that is shared between the different versions, such as type-checking and `spdx_licensing`.

## `spdx`
The `spdx` package contains the code dealing with SPDX-2 documents.
The subpackages serve the purpose to divide the code into logically independent chunks. Shared code can be found in the top-level modules here.
`model`, `parser`, `validation` and `writer` constitute the four main components of this library and are further described below.
`clitools` serves as the entrypoint for the command `pyspdxtools`.
`jsonschema` and `rdfschema` contain code specific to the corresponding serialization format.

### `model`
The internal data model closely follows the [official SPDX-2.3 specification](https://spdx.github.io/spdx-spec/v2.3/).

Entrypoint to the model is the `Document` class, which has the following attributes:
- `creation_info`: a single instance of the `CreationInfo` class
- `packages`: a list of `Package` objects
- `files`: a list of `File` objects
- `snippets`: a list of `Snippet` objects
- `relationships`: a list of `Relationship` objects
- `annotations`: a list of `Annotation` objects
- `extracted_licensing_info`: a list of `ExtractedLicensingInfo` objects

For a complete overview of the model classes and their respective attributes, please refer to [the API documentation](https://spdx.github.io/tools-python/spdx_tools/spdx/model.html).

For licensing attributes, i.e. those of type `LicenseExpression`, the `license-expression` library is used.
The function mainly used here is `get_spdx_licensing().parse(some_license_expression_string)`.
While `get_spdx_licensing()` takes very long to call, its return value can be reused across the code, which is why it is centrally provided by the `spdx_licensing` module in the `common` package.

A custom extension of the `@dataclass` annotation is used that is called `@dataclass_with_properties`.
Apart from all the usual `dataclass` functionality, this implements fields of a class as properties with their own getter and setter methods.
This is used in particular to implement type checking when properties are set.
Source of truth for these checks are the attribute definitions at the start of the respective class that must specify the correct type hint.
The `beartype` library is used to check type conformity (`typeguard` was used in the past but has been replaced since due to performance issues).
In case of a type mismatch a `TypeError` is raised. To ensure that all possible type errors are found during the construction of an object,
a custom `__init__()` that calls `check_types_and_set_values()` is part of every class.
This function tries to set all values provided by the constructor and collects all occurrences of `TypeError` into a single error of type `ConstructorTypeErrors`.

For the SPDX values `NONE` and `NOASSERTION` the classes `SpdxNone` and `SpdxNoAssertion` are used, respectively. Both can be instantiated without any arguments.

### `parser`
The parsing and writing modules are split into subpackages according to the serialization formats: `json`, `yaml`, `xml`, `tagvalue` and `rdf`.
As the first three share the same tree structure that can be parsed into a dictionary, their shared logic is contained in the `jsonlikedict` package.
One overarching concept of all parsers is the goal of dealing with parsing errors (like faulty types or missing mandatory fields) as long as possible before failing.
Thus, the `SPDXParsingError` that is finally raised collects as much information as possible about all parsing errors that occurred.

#### `tagvalue`
Since Tag-Value is an SPDX-specific format, there exist no readily available parsers for it.
This library implements its own deserialization code using the `ply` library's `lex` module for lexing and the `yacc` module for parsing. 

#### `rdf`
The `rdflib` library is used to deserialize RDF graphs from XML format.
The graph is then being parsed and translated into the internal data model. 

#### `json`, `yaml`, `xml`
In a first step, all three of JSON, YAML and XML formats are deserialized into a dictionary representing their tree structure.
This is achieved via the `json`, `yaml` and `xmltodict` packages, respectively.
Special note has to be taken in the XML case which does not support lists and numbers.
The logic concerning the translation from these dicts to the internal data model can be found in the `jsonlikedict` package.

### `writer`
For serialization purposes, only non-null fields are written out.
All writers expect a valid SPDX document from the internal model as input.
To ensure this is actually the case, the standard behaviour of every writer function is to call validation before the writing process.
This can be disabled by setting the `validate` boolean to false.
Also by default, all list properties in the model are scanned for duplicates which are being removed.
This can be disabled by setting the `drop_duplicates` boolean to false.

#### `tagvalue`
The ordering of the tags follows the [example in the official specification](https://github.com/spdx/spdx-spec/blob/development/v2.3.1/examples/SPDXTagExample-v2.3.spdx).

#### `rdf`
The RDF graph is constructed from the internal data model and serialized to XML format afterward, using the `rdflib` library.

#### `json`, `yaml`, `xml`
As all three of JSON, YAML and XML formats share the same tree structure, the first step is to generate the dictionary representing that tree.
This is achieved by the `DocumentConverter` class in the `jsonschema` package.
Subsequently, the dictionary is serialized using the `json`, `yaml` and `xmltodict` packages, respectively.


### `validation`
The `validation` package takes care of all nonconformities with the SPDX specification that are not due to incorrect typing.
This mainly includes checks for correctly formatted strings or the actual existence of references SPDXIDs.
Entrypoint is the `document_validator` module with the `validate_full_spdx_document()` function.
This library supports SPDX versions "SPDX-2.2" and "SPDX-2.3", which differ slightly in the validation process so that the version has to be specified here.
This main validator calls subvalidators for all packages, files etc. that are contained in the document.
Validators are split into two parts, where applicable: The first part validates the object on its own while the second validates it in the context of the whole document.
Validation and reference checking of SPDXIDs (and possibly external document references) is done in the `spdx_id_validators` module.
For the validation of license expressions we utilise the `license-expression` library's `validate` and `parse` functions, which take care of checking license symbols against the [SPDX license list](https://spdx.org/licenses/).

Invalidities are captured in instances of a custom `ValidationMessage` class. This has two attributes:
- `validation_message` is a string that describes the actual problem
- `validation_context` is a `ValidationContext` object that helps to pinpoint the source of the problem by providing the faulty element's SPDXID (if it has one), the parent SPDXID (if that is known), the element's type and finally the full element itself.
It is left open to the implementer which of this information to use in the following evaluation of the validation process.

Every validation function returns a list of `ValidationMessage` objects, which are gradually concatenated until the final list is returned.
That is, if an empty list is returned, the document is valid.

## `spdx3`
Due to the SPDX-3 model still being in development, this package is still a work in progress.
However, as the basic building blocks of parsing, writing, creation and validation are still important in the new version,
the `spdx3` package is planned to be structured similarly to the `spdx` package.

Additionally, the `bump_from_spdx2` package takes care of converting SPDX-2 documents to SPDX-3.
Guideline for this is the [migration guide](https://docs.google.com/document/d/1-olHRnX1CssUS67Psv_sAq9Vd-pc81HF8MM0hA7M0hg).
