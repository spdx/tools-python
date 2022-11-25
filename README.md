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

* API to create and manipulate SPDX documents.
* Parse, convert and create Tag/Value, RDF, JSON, YAML, XML format SPDX files


# TODOs

* Update to full SPDX v2.2.1(ISO 5962:2021)
* Update to full SPDX v2.3
* Add full license expression support


# How to use

## Command-line usage:

1. **PARSER** (for parsing any format):
* Use `pyspdxtools_parser --file <filename>` where `<filename>` is the location of the file.              
If you are using a source distribution, try running: `pyspdxtools_parser --file tests/data/formats/SPDXRdfExample.rdf`.

* Or you can use `pyspdxtools_parser` only, and it will automatically prompt/ask for `filename`.

* For help use `pyspdxtools_parser --help`


2. **CONVERTOR** (for converting one format to another):
* If I/O formats are known:

    * Use `pyspdxtools_convertor --infile/-i <input_file> --outfile/-o <output_file>` where `<input_file>` is the location of the file to be converted
    (Note: only RDF and Tag formatted supported) and `<output_file>` is the location of the output file.  
    If you are using a source distribution, try running : `pyspdxtools_convertor --infile tests/data/formats/SPDXRdfExample.rdf --outfile output.json` 

* If I/O formats are not known:

    * Use `pyspdxtools_convertor --from/-f <input_format> <input_file> --to/-t <output_format> <output_file>` where `<input_format>` is the manually entered format of the input file (can be either rdf or tag)
    and `<out_format>` (can be tag, rdf, json, yaml, xml) is the manually entered format of the output file. 
    If you are using a source distribution, try running : `pyspdxtools_convertor --from tag tests/data/formats/SPDXTagExample.in --to yaml output.out` 

* If one of the formats is known and the other is not, you can use a mixture of the above two points.  
Example (if you are using a source distribution): `pyspdxtools_convertor -f rdf tests/data/formats/SPDXRdfExample.xyz -o output.xml`

* For help use `pyspdxtools_convertor --help`


# Installation

As always you should work in a virtualenv or venv. You can install a local clone
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

Contributions are very welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md) for instructions on how to contribute to the codebase.
