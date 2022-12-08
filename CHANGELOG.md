# Changelog


## v0.7.0 (2022-12-08)

Starting a Changelog.

### New features and changes

* Dropped Python 2 support. Python >= 3.6 is now required.
* Added `pyspdxtools_convertor` and `pyspdxtools_parser` CLI scripts. See [the readme](README.md) for usage instructions.
* Updated the tools to support SPDX versions up to 2.3 and to conform with the specification. Apart from many bugfixes 
  and new properties, some of the more significant changes include:
    * Support for multiple packages per document
    * Support for multiple checksums for packages and files
    * Support for files outside a package
* **Note**: Validation was updated to follow the 2.3 specification. Since there is currently no support for 
  version-specific handling, some details may be handled incorrectly for documents using lower
  versions. The changes are mostly restricted to properties becoming optional and new property values becoming
  available, and should be of limited impact. See https://spdx.github.io/spdx-spec/v2.3/diffs-from-previous-editions/
  for a list of changes between the versions.
* **Note**: RDF support for 2.3 is not completed, see https://github.com/spdx/tools-python/issues/295
* Removed example documents from production code. Added additional up-to-date examples to test files.
* Introduced pytest as the preferred test framework.
* Improved error message handling and display.
* Extended the contribution guidelines.
* Improved tag/value output structure.
* Added .editorconfig and pyproject.toml.
* Improved handling of JSON-specific properties `documentDescribes` and `hasFiles`.
* Added new LicenseListVersion tag.
* Fixed annotation handling for the JSON and Tag/Value formats.
* Free form text values in Tag/Value no longer require `<text>` tags if they don't span multiple lines.

### Contributors

This release was made possible by the following contributors. Thank you very much!

* Meret Behrens @meretp
* Philippe Ombredanne @pombredanne
* Pierre Tardy @tardyp
* Nicolaus Weidner @nicoweidner
* Jeff Licquia @licquia
* Armin Tänzer @armintaenzertng
* Alberto Pianon @alpianon
* Rodney Richardson @RodneyRichardson
* Lon Hohberger @lhh
* Nathan Voss @njv299
* Gary O'Neall @goneall
* Jeffrey Otterson @jotterson
* KOLANICH @KOLANICH
* Yash Varshney @Yash-Varshney
* HARDIK @HARDIK-TSH1392
* Jose Quaresma @quaresmajose
* Santiago Torres @SantiagoTorres
* Shubham Kumar Jha @ShubhamKJha
* Steven Kalt @SKalt
* Cole Helbling @cole-h
* Daniel Holth @dholth
* John Vandenberg @jayvdb
* Kate Stewart @kestewart
* Alexios Zavras @zvr
* Maximilian Huber @maxhbr
* Kyle Altendorf @altendky
* alpianon @alpianon
* kbermude @kbermude
* mzfr @mzfr
