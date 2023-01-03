# Python library to parse, validate and create SPDX documents

| Linux                          | macOS                         | Windows                         |
|:-------------------------------|:------------------------------|:--------------------------------|
| [ ![Linux build status][1]][2] | [![macOS build status][3]][4] | [![Windows build status][5]][6] |

[1]: https://travis-ci.org/spdx/tools-python.svg?branch=master

[2]: https://travis-ci.org/spdx/tools-python

[3]: https://circleci.com/gh/spdx/tools-python/tree/master.svg?style=shield&circle-token=36cca2dfa3639886fc34e22d92495a6773bdae6d

[4]: https://circleci.com/gh/spdx/tools-python/tree/master

[5]: https://ci.appveyor.com/api/projects/status/0bf9glha2yg9x8ef/branch/master?svg=true

[6]: https://ci.appveyor.com/project/spdx/tools-python/branch/master

# CURRENT STATE

A major refactoring of large parts of the codebase is currently in progress. It is expected that functionality on `main`
is severely limited during this process. Please check out
the [latest release](https://github.com/spdx/tools-python/releases/tag/v0.7.0) if you are looking for a working version.

# Information

This library implements SPDX parsers, convertors, validators and handlers in Python.

- Home: https://github.com/spdx/tools-python
- Issues: https://github.com/spdx/tools-python/issues
- PyPI: https://pypi.python.org/pypi/spdx-tools

# History

This is the result of an initial GSoC contribution by @[ah450](https://github.com/ah450)
(or https://github.com/a-h-i) and is maintained by a community of SPDX adopters and enthusiasts.

# License

[Apache-2.0](LICENSE)

# Features

* API to create and manipulate SPDX v2.3 documents.
* Parse, convert, create and validate Tag/Value, RDF, JSON, YAML, XML format SPDX files

### Known Limitations

* No full 2.3 support for RDF format [#295](https://github.com/spdx/tools-python/issues/295)
* No full license expression support [#10](https://github.com/spdx/tools-python/issues/10)
* Output of the CLI parser is incomplete [#268](https://github.com/spdx/tools-python/issues/268)

# TODOs

* Include specialized validation for SPDX v2.2.1(ISO 5962:2021)

# How to use

## Command-line usage:

1. **PARSING/VALIDATING** (for parsing any format):

* Use `pyspdxtools -i <filename>` where `<filename>` is the location of the file.              
  If you are using a source distribution, try running: `pyspdxtools -i tests/data/formats/SPDXJSONExample-v2.3.spdx.json`.

* Or you can use `pyspdxtools` only, and it will automatically prompt/ask for the `input file path`.

2. **CONVERTING** (for converting one format to another):

* Use `pyspdxtools -i <input_file> -o <output_file>` where `<input_file>` is the location of the file to be converted
  and `<output_file>` is the location of the output file. The output format is inferred automatically from the file ending.
  If you are using a source distribution, try running : `pyspdxtools -i tests/data/formats/SPDXJSONExample-v2.3.spdx.json -o output.tag` 

* If you want to skip the validation process, provide the `--novalidation` flag, like so:  
  `pyspdxtools -i tests/data/formats/SPDXJSONExample-v2.3.spdx.json -o output.tag --novalidation`
* For help use `pyspdxtools --help`

# Installation

As always you should work in a virtualenv (venv). You can install a local clone
of this repo with `yourenv/bin/pip install .` or install it from PyPI with
`yourenv/bin/pip install spdx-tools`. Note that on Windows it would be `Scripts`
instead of `bin`.

# Dependencies

* PLY: https://pypi.python.org/pypi/ply/ used for parsing.
* rdflib: https://pypi.python.org/pypi/rdflib/ for handling RDF.
* PyYAML: https://pypi.org/project/PyYAML/ for handling YAML.
* xmltodict: https://pypi.org/project/xmltodict/ for handling XML.
* click: https://pypi.org/project/click/ for creating the CLI interface.

# Support

* Submit issues, questions or feedback at https://github.com/spdx/tools-python/issues
* Join the chat at https://gitter.im/spdx-org/Lobby
* Join the discussion on https://lists.spdx.org/g/spdx-tech and
  https://spdx.dev/participate/tech/

# Contributing

Contributions are very welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md) for instructions on how to contribute to the
codebase.
