#!/usr/bin/env python

# Writes a new tag/value file from scratch.
# Usage: write_tv <tagvaluefile>

if __name__ == '__main__':
    import sys
    import codecs
    from spdx.writers.tagvalue import write_document, InvalidDocumentError
    from spdx.document import Document, License, LicenseConjunction, ExtractedLicense
    from spdx.version import Version
    from spdx.creationinfo import Person
    from spdx.review import Review
    from spdx.package import Package
    from spdx.file import File, FileType
    from spdx.checksum import Algorithm
    from spdx.utils import SPDXNone, NoAssert, UnKnown

    doc = Document()
    doc.version = Version(1, 2)
    doc.comment = 'Example Document'
    doc.data_license = License.from_identifier('CC0-1.0')
    doc.creation_info.add_creator(Person('Alice', 'alice@example.com'))
    doc.creation_info.set_created_now()
    review = Review(Person('Joe', None))
    review.set_review_date_now()
    review.comment = 'Joe reviewed this document'
    doc.add_review(review)
    # File
    testfile1 = File('TestFile1')
    testfile1.type = FileType.BINARY
    testfile1.comment = 'This is a test file.'
    testfile1.chk_sum = Algorithm('SHA1', 'c537c5d99eca5333f23491d47ededd083fefb7ad')
    testfile1.conc_lics = License.from_identifier('BSD-2-Clause')
    testfile1.add_lics(License.from_identifier('BSD-2-Clause'))
    testfile1.copyright = SPDXNone()
    testfile1.add_artifact('name', 'TagWriteTest')
    testfile1.add_artifact('home', UnKnown())
    testfile1.add_artifact('uri', 'http://tagwritetest.test')

    testfile2 = File('TestFile2')
    testfile2.type = FileType.SOURCE
    testfile2.comment = 'This is a test file.'
    testfile2.chk_sum = Algorithm('SHA1', 'bb154f28d1cf0646ae21bb0bec6c669a2b90e113')
    testfile2.conc_lics = License.from_identifier('Apache-2.0')
    testfile2.add_lics(License.from_identifier('Apache-2.0'))
    testfile2.copyright = NoAssert()


    # Package
    package = Package()
    package.name = 'TagWriteTest'
    package.version = '1.0'
    package.file_name = 'twt.jar'
    package.download_location = 'http://www.tagwritetest.test/download'
    package.homepage = SPDXNone()
    package.verif_code = '4e3211c67a2d28fced849ee1bb76e7391b93feba'
    license_set = LicenseConjunction(License.from_identifier('Apache-2.0'),
        License.from_identifier('BSD-2-Clause'))
    package.conc_lics = license_set
    package.license_declared = license_set
    package.add_lics_from_file(License.from_identifier('Apache-2.0'))
    package.add_lics_from_file(License.from_identifier('BSD-2-Clause'))
    package.cr_text = NoAssert()
    package.summary = 'Simple package.'
    package.description = 'Really simple package.'
    package.add_file(testfile1)
    package.add_file(testfile2)

    doc.package = package

    # An extracted license

    lic = ExtractedLicense('LicenseRef-1')
    lic.text = 'Some non legal legal text..'
    doc.add_extr_lic(lic)

    file = sys.argv[1]
    with codecs.open(file, mode='w', encoding='utf-8') as out:
        try:
            write_document(doc, out)
        except InvalidDocumentError:
            print 'Document is Invalid'
            messages = []
            doc.validate(messages)
            print '\n'.join(messages)
