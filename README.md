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


# Information

This library implements an SPDX tag/value and RDF parser, validator and handler in Python.
This is the result of an initial GSoC contribution by @[ah450](https://github.com/ah450) (or https://github.com/a-h-i) and 
is maintained by a community of SPDX adopters and enthusiasts.

Home: https://github.com/spdx/tools-python

Issues: https://github.com/spdx/tools-python/issues

Pypi: https://pypi.python.org/pypi/spdx-tools


# License

[Apache-2.0](LICENSE)


# Features

* API to create and manipulate SPDX documents.
* Parse and create Tag/Value, RDF, JSON, YAML, XML format SPDX files


# TODOs

* Update to full SPDX v2.1
* Add to full license expression support


# How to use

## Command-line usage:

1. **PARSER** (for parsing any format):
* Use   `parser --file <filename>`   where  `<filename>`  is the location of the file.              
Try running :   `parser --file data/SPDXRdfExample.rdf`.
       
* Or you can use  `parser`  only and then it will automatically prompt/ask for  `filename`. 

* for help - use `parser --help` 


2. **CONVERTOR** (for converting one format to another):
* If I/O formats are known:
    
    * Use `convertor --infile/-i <input_file> --outfile/-o <output_file>` where `<input_file>` is the location of the file to be converted 
    (Note: only RDF and Tag formated supported) and `<output_file>` is the location of the output file.  
    Try running : `convertor --infile data/SPDXRdfExample.rdf --outfile output.json` 

* If I/O formats are not known:

    * Use `convertor --from/-f <input_format> <input_file> --to/-t <output_format> <output_file>` where `<input_format>` is the manually enterred format of the input file (can be either rdf or tag)
    and `<out_format>` (can be tag, rdf, json, yaml, xml) is the manually enterred format of the output file. 
    Try running : `convertor --from tag data/SPDXTagExample.in --to yaml output.out` 

* If anyone format is known and other is not, you can use the mixture of the above two points.      
Ex. : `convertor -f rdf data/SPDXRdfExample.xyz -o output.xml`

* for help - use `convertor --help`



# Installation

As always you should work in a virtualenv or venv.  You can install a local clone
of this repo with `yourenv/bin/pip install .` or install from PyPI with
`yourenv/bin/pip install spdx-tools`.  Note that on Windows it would be `Scripts`
instead of `bin`.


# How to run tests

From the project root directory run: `python setup.py test`.
You can use another test runner such as pytest or nose at your preference.


# Development process

We use the GitHub flow that is described here: https://guides.github.com/introduction/flow/

So, whenever we have to make some changes to the code, we should follow these steps:
1. Create a new branch:
    `git checkout -b fix-or-improve-something`
2. Make some changes and the first commit(s) to the branch: 
    `git commit --signoff -m 'What changes we did'`
3. Push the branch to GitHub:
    `git push origin fix-or-improve-something`
4. Make a pull request on GitHub.
5. Continue making more changes and commits on the branch, with `git commit --signoff` and `git push`.
6. When done, write a comment on the PR asking for a code review.
7. Some other developer will review your changes and accept your PR. The merge should be done with `rebase`, if possible, or with `squash`.
8. The temporary branch on GitHub should be deleted (there is a button for deleting it).
9. Delete the local branch as well:
    ```
    git checkout master
    git pull -p
    git branch -a
    git branch -d fix-or-improve-something
    ```

Besides this, another requirement is that every change should be made to fix or close an issue: https://guides.github.com/features/issues/
If there is no issue for the changes that you want to make, create first an issue about it that describes what needs to be done, assign it to yourself, and then start working for closing it.


# Dependencies

* PLY : https://pypi.python.org/pypi/ply/ used for parsing.
* rdflib : https://pypi.python.org/pypi/rdflib/ for handling RDF. 
* PyYAML: https://pypi.org/project/PyYAML/ for handling YAML.
* xmltodict: https://pypi.org/project/xmltodict/ for handling XML.


# Support

* Submit issues, questions or feedback at: https://github.com/spdx/tools-python/issues
* Join the dicussion on https://lists.spdx.org/mailman/listinfo/spdx-tech and 
  https://spdx.org/WorkgroupTechnical
