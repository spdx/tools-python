Python SPDX Parser Library
==========================

This library provides an implementation of a tag/value and RDF SPDX  v1.2 parser in python.

Official repository: http://git.spdx.org/?p=spdx-tools-python.git

GitHub mirror: https://github.com/spdx/sdpx-tools-python
Issues: https://github.com/spdx/sdpx-tools-python/issues

Pypi: https://pypi.python.org/pypi/spdx-tools

License:
========
Apache-2.0

Expected Features:
==================
* API for creating and manipulating SPDX documents.
* Parse Tag/Value format SPDX files
* Parse RDF format SPDX files
* Create Tag/Value files.
* Create RDF files.


Current Status:
===============
* RDF Parser implemented.
* Tag/value parser implemented
* Tag/value writer implemented.
* RDF/Writer implemented.


Plans:
======
* Update to SPDX v2.1


How to use:
===========
Example tag/vlue parsing usage:
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

* `parse_tv.py` is an example tag/vlue parsing uage.
  Try running `python parse_tv.py 'data/SPDXSimpleTag.tag' `

* `write_tv.py` provides an example of writing tag/value files.
  Run `python write_tv.py sample.tag` to test it.

* `pp_tv.py` demonstrates how to pretty-print a tag/value file.
   To test it run `python pp_tv.py data/SPDXTagExample.tag pretty.tag`.

* `parse_rdf.py` demonstrates how to parse an RDF file and print out document 
   information. To test it run `python parse_rdf.py data/SPDXRdfExample.rdf`

* `rdf_to_tv.py` demonstrates how to convert an RDF file to a tag/value one.
   To test it run `python rdf_to_tv.py data/SPDXRdfExample.rdf converted.tag`

* `pp_rdf.py` demonstrates how to pretty-print an RDF file, to test it run 
  `python pp_rdf.py data/SPDXRdfExample.rdf pretty.rdf`


Installation:
=============
Clone or download the repository and run `python setup.py install`


How to run tests:
=================
From the project root directory run: `python setup.py test`.
You can use another test runner such as pytest or nose at your preference.


Dependencies:
=============
* PLY : https://pypi.python.org/pypi/ply/3.4 used for parsing.
* rdflib : https://pypi.python.org/pypi/rdflib/4.1.2 for for handling RDF. 


Support:
=======

* Submit issues, questions or feedback at: https://github.com/spdx/sdpx-tools-python/issues
* Join the dicussion on https://lists.spdx.org/mailman/listinfo/spdx-tech and 
  https://spdx.org/WorkgroupTechnical