# Changelog

## v0.8.2 (2023-10-12)

### New features and changes

* added optional encoding parameter for parsing files
* fixed handling of the FilesAnalyzed field in Tag-Value format
* fixed the validation of the DownloadLocation field
* fixed the error handling while parsing license expressions
* fixed output of timezone-sensitive datetimes
* added code architecture documentation

### Contributors

This release was made possible by the following contributors. Thank you very much!

* Christian Decker @chrisdecker1201
* Jeff Licquia @licquia
* Maximilian Huber @maxhbr
* Armin Tänzer @armintaenzertng


## v0.8.1 (2023-08-24)

### New features and changes

* massive speed-up in the validation process of large SBOMs
* validation now detects and checks license references from external documents
* allow for userinfo in git+ssh download location
* more efficient relationship parsing in JSON/YAML/XML

### Contributors

This release was made possible by the following contributors. Thank you very much!

* Brian DeHamer @bdehamer
* Brandon Lum @lumjjb
* Maximilian Huber @maxhbr
* Armin Tänzer @armintaenzertng


## v0.8.0 (2023-07-25)

### New features and changes

* major refactoring of the library
  * new and improved data model
  * type hints and type checks have been added to the model classes
  * license expressions and SPDX license list are now handled by the `license-expression` package
  * to update your existing code, refer to the [migration guide](https://github.com/spdx/tools-python/wiki/How-to-migrate-from-0.7-to-0.8)
* experimental support for the upcoming SPDX v3 specification (note, however, that support is neither complete nor
  stable at this point, as the spec is still evolving)
* full validation of SPDX documents against the v2.2 and v2.3 specification
* support for SPDX's RDF format with all v2.3 features
* unified `pysdpxtools` CLI tool replaces separate `pyspdxtools_parser` and `pyspdxtools_convertor`
* [online API documentation](https://spdx.github.io/tools-python)
* replaced CircleCI with GitHub Actions

### Contributors

This release was made possible by the following contributors. Thank you very much!

* Armin Tänzer @armintaenzertng
* Gary O'Neall @goneall
* Gaurav Mishra @GMishx
* HarshvMahawar @HarshvMahawar
* Holger Frydrych @fholger
* Jeff Licquia @licquia
* Kate Stewart @kestewart
* Maximilian Huber @maxhbr
* Meret Behrens @meretp
* Nicolaus Weidner @nicoweidner
* William Armiros @willarmiros


## v0.7.1 (2023-03-14)

### New features and changes

* added GitHub Actions workflow
* added requirements.txt
* added uritools for URI validation
* Python >= 3.7 is now required
* json/yaml/xml: added support for empty arrays for hasFiles and licenseInfoFromFiles
* rdf: fixed writing of multiple packages
* tag-value: enhanced parsing of snippet ranges to not mix it up with package version
* tag-value: fixed parsing of whitespaces
* tag-value: duplicates in LicenseInfoInFile are now removed during writing
* account for supplier and originator to be NOASSERTION
* checksum validation now requires lowercase values
* during writing of a file, the encoding can be set (default is utf-8)
* license list updated to version 3.20

### Contributors

This release was made possible by the following contributors. Thank you very much!

* Christian Decker @chrisdecker1201
* Marc-Etienne Vargenau @vargenau
* John Vandenberg @jayvdb
* Nicolaus Weidner @nicoweidner
* Meret Behrens @meretp
* Armin Tänzer @armintaenzertng
* Maximilian Huber @maxhbr


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
