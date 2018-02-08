#!/usr/bin/env python

# Parses a tag/value file and prints out some basic information.
# Usage: parse_tv.py <tagvaluefile>

if __name__ == '__main__':
    import sys
    from spdx.parsers.tagvalue import Parser
    from spdx.parsers.loggers import StandardLogger
    from spdx.parsers.tagvaluebuilders import Builder
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


    allFiles = sys.argv
    filePosition = 1
    fileData = []
    p = Parser(Builder(), StandardLogger())
    p.build()


    while filePosition < len(allFiles):
        with open(allFiles[filePosition]) as f:
            data = f.read()
            fileData.append(data);

        filePosition += 1

    newFileName = input("Enter file name to save: ")

    with codecs.open(newFileName, mode='w', encoding='utf-8') as newFile:
        try:
            write_document("".join(fileData), newFile)

        except InvalidDocumentError:
            print ('Document is Invalid')
            messages = []
            doc.validate(messages)
            print ('\n'.join(messages))
