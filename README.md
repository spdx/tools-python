# Python SPDX Library to parse, validate and create SPDX documents

| Linux | macOS | Windows |
| :---- | :------ | :---- |
[ ![Linux build status][1]][2] | [![macOS build status][3]][4] | [![Windows build status][5]][6] |

[1]: https://travis-ci.org/spdx/tools-python.svg?branch=master
[2]: https://travis-ci.org/spdx/tools-python
[3]: https://circleci.com/gh/spdx/tools-python/tree/master.svg?style=shield&circle-token=36cca2dfa3639886fc34e22d92495a6773bdae6d
[4]: https://circleci.com/gh/spdx/tools-python/tree/master
[5]: https://ci.appveyor.com/api/projects/status/0bf9glha2yg9x8ef/branch/master?svg=true
[6]: https://ci.appveyor.com/project/spdx/tools-python/branch/master

This library implements an SPDX tag/value and RDF parser, validator and handler in Python.
This is the result of an initial GSoC contribution by @ah450 https://github.com/ah450 and 
is maintained by a community of SPDX adopters and enthusiasts.

Home: https://github.com/spdx/tools-python

Issues: https://github.com/spdx/tools-python/issues

Pypi: https://pypi.python.org/pypi/spdx-tools


# License

[Apache-2.0](LICENSE)


# Features

* API to create and manipulate SPDX documents.
* Parse and create Tag/Value format SPDX files
* Parse and create RDF format SPDX files


# TODOs

* Update to full SPDX v2.1
* Add to full license expression support


# How to use

Example tag/value parsing usage:
```Python
    from spdx.parsers.tagvalue import Parser
    from spdx.parsers.tagvaluebuilders import Builder
    from spdx.parsers.loggers import StandardLogger
    p = Parser(Builder(), StandardLogger())
    p.build()
    # data is a string containing the SPDX file.
    document, error = p.parse(data)

```

The `examples` directory contains several code samples:

* `parse_tv.py` is an example tag/value parsing usage.
  Try running `python parse_tv.py '../data/SPDXSimpleTag.tag' `

* `write_tv.py` provides an example of writing tag/value files.
  Run `python write_tv.py sample.tag` to test it.

* `pp_tv.py` demonstrates how to pretty-print a tag/value file.
   To test it run `python pp_tv.py ../data/SPDXTagExample.tag pretty.tag`.

* `parse_rdf.py` demonstrates how to parse an RDF file and print out document 
   information. To test it run `python parse_rdf.py ../data/SPDXRdfExample.rdf`

* `rdf_to_tv.py` demonstrates how to convert an RDF file to a tag/value one.
   To test it run `python rdf_to_tv.py ../data/SPDXRdfExample.rdf converted.tag`

* `pp_rdf.py` demonstrates how to pretty-print an RDF file, to test it run 
  `python pp_rdf.py ../data/SPDXRdfExample.rdf pretty.rdf`


# Installation

Clone or download the repository and run `python setup.py install`. (In a virtualenv, of course)

or install from Pypi with `pip install spdx-tools`


# How to run tests

From the project root directory run: `python setup.py test`.
You can use another test runner such as pytest or nose at your preference.


# Dependencies

* PLY : https://pypi.python.org/pypi/ply/ used for parsing.
* rdflib : https://pypi.python.org/pypi/rdflib/ for for handling RDF. 


# Support

* Submit issues, questions or feedback at: https://github.com/spdx/tools-python/issues
* Join the dicussion on https://lists.spdx.org/mailman/listinfo/spdx-tech and 
  https://spdx.org/WorkgroupTechnical
