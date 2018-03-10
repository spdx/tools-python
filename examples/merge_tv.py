# !/usr/bin/env python

# Merge multiple tag-value files into one
# Usage : merge_tv.py <tagvaluefile1> <tagvaluefile2> <destinationfile>
# In case of any conflict, the first file is given preference

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
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    p = Parser(Builder(), StandardLogger())
    p.build()
    doc = Document()
    with open(file1) as f1, open(file2) as f2:
        data1 = f1.read()
        data2 = f2.read()
        document1, error1 = p.parse(data1)
        document2, error2 = p.parse(data2)
        if not error1 and not error2:
            print('Parsing Successful')
            if document1.version == document2.version:
                doc.version = document1.version
            else:
                print('Version Mismatch. SPDX document may be inconsistent. Check Version specifications for more info.')
                doc.version = document1.version
            doc.data_license = document1.data_license
            doc.comment = "1.{}\n2.{}".format(document1.comment,document2.comment)
            for creator in document1.creation_info.creators:
                doc.creation_info.add_creator(creator)
            for creator in document2.creation_info.creators:
                doc.creation_info.add_creator(creator)
            doc.creation_info.set_created_now()
            doc.comment = "1.{}\n2.{}".format(document1.comment,document2.comment)
            for reviewer in document1.reviews:
                doc.add_review(reviewer)
            for reviewer in document2.reviews:
                doc.add_review(reviewer)

            #Package Information
            #General Package information of the resulting file will derive from tag file that represents newer version
            #Package license information will derive from the first file given
            
            package = Package()
            if document1.package.version > document2.package.version:
                package.name = document1.package.name
                package.version = document1.package.version
                package.file_name = document1.package.file_name
                package.supplier = document1.package.supplier
                package.originator = document1.package.originator
                package.download_location = document1.package.download_location
                package.homepage = document1.package.homepage
                package.verif_code = document1.package.verif_code
                package.check_sum = document1.package.check_sum
                package.source_info = document1.package.source_info
            else:
                package.name = document2.package.name
                package.version = document2.package.version
                package.file_name = document2.package.file_name
                package.supplier = document2.package.supplier
                package.originator = document2.package.originator
                package.download_location = document2.package.download_location
                package.homepage = document2.package.homepage
                package.verif_code = document2.package.verif_code
                package.check_sum = document2.package.check_sum
                package.source_info = document2.package.source_info

            package.summary = '1.{}\n2.{}'.format(document1.package.summary,document2.package.summary)
            package.description = document1.package.description
            package.cr_text = document1.package.cr_text
            #Package License Information

            package.conc_lics = document1.package.conc_lics
            package.license_declared = document1.package.license_declared
            package.license_comment = document1.package.license_comment

            for lics_from_file in document1.package.licenses_from_files:
                package.add_lics_from_file(lics_from_file)
            for lics_from_file in document2.package.licenses_from_files:
                package.add_lics_from_file(lics_from_file)
            for file in document1.package.files:
                package.add_file(file)
            for file in document2.package.files:
                package.add_file(file)
            for exc_file in document1.package.verif_exc_files:
                package.add_exc_file(exc_file)
            for exc_file in document2.package.verif_exc_files:
                package.add_exc_file(exc_file)

            doc.package = package
            #License Information

            for extracted_lic in document1.extracted_licenses:
                doc.add_extr_lic(extracted_lic)
            for extracted_lic in document2.extracted_licenses:
                doc.add_extr_lic(extracted_lic)

            file = sys.argv[3]
            with codecs.open(file, mode='w', encoding='utf-8') as out:
                try:
                    write_document(doc, out)
                except InvalidDocumentError:
                    print('Document is Invalid')
                    messages = []
                    doc.validate(messages)
                    print('\n').join(messages)
        else:
            print("Errors while parsing")

