# Python library to parse, validate and create SPDX documents

CI status (Linux, macOS and Windows): [![Install and Test][1]][2]

[1]: https://github.com/spdx/tools-python/actions/workflows/install_and_test.yml/badge.svg

[2]: https://github.com/spdx/tools-python/actions/workflows/install_and_test.yml


# Current state

This repository was subject to a major refactoring recently to get ready for the upcoming SPDX v3.0 release.
Therefore, we'd like to encourage you to post any and all issues you find at https://github.com/spdx/tools-python/issues.  
If you prefer a version that has been longer in use, please check out
the [latest release](https://github.com/spdx/tools-python/releases/tag/v0.7.0).
Note, though, that this will only receive bug fixes but no new features.

# Information

This library implements SPDX parsers, convertors, validators and handlers in Python.

- Home: https://github.com/spdx/tools-python
- Issues: https://github.com/spdx/tools-python/issues
- PyPI: https://pypi.python.org/pypi/spdx-tools


# License

[Apache-2.0](LICENSE)

# Features

* API to create and manipulate SPDX v2.2 and v2.3 documents.
* Parse, convert, create and validate SPDX files
* supported formats: Tag/Value, RDF, JSON, YAML, XML

# Planned features

* up-to-date support of SPDX v3.0 as soon as it is released

# Installation

As always you should work in a virtualenv (venv). You can install a local clone
of this repo with `yourenv/bin/pip install .` or install it from PyPI with
`yourenv/bin/pip install spdx-tools`. Note that on Windows it would be `Scripts`
instead of `bin`.

# How to use

## Command-line usage

1. **PARSING/VALIDATING** (for parsing any format):

* Use `pyspdxtools -i <filename>` where `<filename>` is the location of the file. The input format is inferred automatically from the file ending.

* If you are using a source distribution, try running:  
  `pyspdxtools -i tests/data/formats/SPDXJSONExample-v2.3.spdx.json`

2. **CONVERTING** (for converting one format to another):

* Use `pyspdxtools -i <input_file> -o <output_file>` where `<input_file>` is the location of the file to be converted
  and `<output_file>` is the location of the output file. The input and output formats are inferred automatically from the file endings.

* If you are using a source distribution, try running:  
  `pyspdxtools -i tests/data/formats/SPDXJSONExample-v2.3.spdx.json -o output.tag` 

* If you want to skip the validation process, provide the `--novalidation` flag, like so:  
  `pyspdxtools -i tests/data/formats/SPDXJSONExample-v2.3.spdx.json -o output.tag --novalidation`  
  (use this with caution: note that undetected invalid documents may lead to unexpected behavior of the tool)
  
* For help use `pyspdxtools --help`

## Library usage
1. **DATA MODEL**
  * The `src.spdx.model` package constitutes the internal SPDX v2.3 data model (v2.2 is a simply a subset of this).
  * SPDX objects are implemented via `@dataclass_with_properties`, a custom extension of `@dataclass`.
    * Each class starts with a list of its properties and their possible types. When no default value is provided, the property is mandatory and must be set during initialization.
    * Using the type hints, type checking is enforced when initializing a new instance or setting/getting a property on an instance
      (wrong types will raise `ConstructorTypeError` or `TypeError`, respectively). This makes it easy to catch invalid properties early and only construct valid documents.
    * Note: in-place manipulations like `list.append(item)` will circumvent the type checking (a `TypeError` will still be raised when reading `list` again). We recommend using `list = list + [item]` instead.
  * The main entry point of an SPDX document is the `Document` class, which links to all other classes.
  * For license handling, the [license_expression](https://github.com/nexB/license-expression) library is used.
  * Note on `documentDescribes` and `hasFiles`: These fields will be converted to relationships in the internal data model. During serialization, they will be written again where appropriate.
2. **PARSING**
  * Use `parse_file(file_name)` from the `parse_anything.py` module to parse an arbitrary file with one of the supported file endings.
  * Successful parsing will return a `Document` instance. Unsuccessful parsing will raise `SPDXParsingError` with a list of all encountered problems.
3. **VALIDATING**
  * Use `validate_full_spdx_document(document)` to validate an instance of the `Document` class.
  * This will return a list of `ValidationMessage` objects, each consisting of a String describing the invalidity and a `ValidationContext` to pinpoint the source of the validation error.
  * Validation depends on the SPDX version of the document. Note that only versions `SPDX-2.2` and `SPDX-2.3` are supported by this tool.
4. **WRITING**
  * Use `write_file(document, file_name)` from the `write_anything.py` module to write a `Document` instance to the specified file.
    The serialization format is determined from the filename ending.
  * Validation is performed per default prior to the writing process, which is cancelled if the document is invalid. You can skip the validation via `write_file(document, file_name, validate=False)`.
    Caution: Only valid documents can be serialized reliably; serialization of invalid documents is not supported.

## Example
Here are some examples of possible use cases to quickly get you started with the spdx-tools:
```python
# read in an SPDX document from a file
document = parse_file("spdx_document.json")

# change the document's name
document.creation_info.name = "new document name"

# define a file and a DESCRIBES relationship between the file and the document
checksum = Checksum(ChecksumAlgorithm.SHA1, "71c4025dd9897b364f3ebbb42c484ff43d00791c")

file = File(name="./fileName.py", spdx_id="SPDXRef-File", checksums=[checksum], file_types=[FileType.TEXT],
            license_concluded=get_spdx_licensing().parse("MIT and GPL-2.0"),
            license_comment="licenseComment", copyright_text="copyrightText")

relationship = Relationship("SPDXRef-DOCUMENT", RelationshipType.DESCRIBES, "SPDXRef-File")

# add the file and the relationship to the document (note that we do not use "document.files.append(file)" as that would circumvent the type checking)
document.files = document.files + [file]
document.relationships = document.relationships + [relationship]

# validate the edited document and log the validation messages (depending on your use case, you might also want to utilize the provided validation_message.context)
validation_messages = validate_full_spdx_document(document)
for validation_message in validation_messages:
    logging.warning(validation_message.validation_message)

# if there are no validation messages, the document is valid and we can safely serialize it without validating again
if not validation_messages:
    write_file(document, "new_spdx_document.rdf", validate=False)
```

# Dependencies

* PyYAML: https://pypi.org/project/PyYAML/ for handling YAML.
* xmltodict: https://pypi.org/project/xmltodict/ for handling XML.
* rdflib: https://pypi.python.org/pypi/rdflib/ for handling RDF.
* ply: https://pypi.org/project/ply/ for handling tag-value.
* click: https://pypi.org/project/click/ for creating the CLI interface.
* typeguard: https://pypi.org/project/typeguard/ for type checking.
* uritools: https://pypi.org/project/uritools/ for validation of URIs.
* license-expression: https://pypi.org/project/license-expression/ for handling SPDX license expressions.

# Support

* Submit issues, questions or feedback at https://github.com/spdx/tools-python/issues
* Join the chat at https://gitter.im/spdx-org/Lobby
* Join the discussion on https://lists.spdx.org/g/spdx-tech and
  https://spdx.dev/participate/tech/

# Contributing

Contributions are very welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md) for instructions on how to contribute to the
codebase.

# History

This is the result of an initial GSoC contribution by @[ah450](https://github.com/ah450)
(or https://github.com/a-h-i) and is maintained by a community of SPDX adopters and enthusiasts.
In order to prepare for the release of SPDX v3.0, the repository has undergone a major refactoring during the time from 11/2022 to 03/2023.
