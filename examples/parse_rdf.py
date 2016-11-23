#!/usr/bin/env python

# Parses an RDF file and prints out some basic information.
# Usage: parse_rdf.py <rdffile>

if __name__ == '__main__':
    import sys
    import spdx.file as spdxfile
    from spdx.parsers.rdf import Parser
    from spdx.parsers.loggers import StandardLogger
    from spdx.parsers.rdfbuilders import Builder
    file = sys.argv[1]
    p = Parser(Builder(), StandardLogger())
    with open(file) as f:
        doc, error = p.parse(f)
        if not error:
            print 'doc comment: {0}'.format(doc.comment)
            print 'Creators:'
            for c in doc.creation_info.creators:
                print '\t{0}'.format(c)
            print 'Document review information:'
            for review in doc.reviews:
                print '\tReviewer: {0}'.format(review.reviewer)
                print '\tDate: {0}'.format(review.review_date)
                print '\tComment: {0}'.format(review.comment)
            print 'Creation comment: {0}'.format(doc.creation_info.comment)
            print 'Package Name: {0}'.format(doc.package.name)
            print 'Package Version: {0}'.format(doc.package.version)
            print 'Package Download Location: {0}'.format(doc.package.download_location)
            print 'Package Homepage: {0}'.format(doc.package.homepage)
            print 'Package Checksum: {0}'.format(doc.package.check_sum.value)
            print 'Package verification code: {0}'.format(doc.package.verif_code)
            print 'Package excluded from verif: {0}'.format(','.join(doc.package.verif_exc_files))
            print 'Package license concluded: {0}'.format(doc.package.conc_lics)
            print 'Package license declared: {0}'.format(doc.package.license_declared)
            print 'Package licenses from files:'
            for lics in doc.package.licenses_from_files:
                print '\t{0}'.format(lics)
            print 'Package Copyright text: {0}'.format(doc.package.cr_text)
            print 'Package summary: {0}'.format(doc.package.summary)
            print 'Package description: {0}'.format(doc.package.description)
            print 'Package Files:'
            VALUES = {
                spdxfile.FileType.SOURCE: 'SOURCE',
                spdxfile.FileType.OTHER: 'OTHER',
                spdxfile.FileType.BINARY: 'BINARY',
                spdxfile.FileType.ARCHIVE: 'ARCHIVE'
            }
            for f in doc.files:
                print '\tFile name: {0}'.format(f.name)
                print '\tFile type: {0}'.format(VALUES[f.type])
                print '\tFile Checksum: {0}'.format(f.chk_sum.value)
                print '\tFile license concluded: {0}'.format(f.conc_lics)
                print '\tFile license info in file: {0}'.format(','.join(
                     map(lambda l: l.identifier, f.licenses_in_file)))
                print '\tFile artifact of project name: {0}'.format(','.join(f.artifact_of_project_name))

            print 'Document Extracted licenses:'
            for lics in doc.extracted_licenses:
                print '\tIdentifier: {0}'.format(lics.identifier)
                print '\tName: {0}'.format(lics.full_name)

        else:
            print 'Errors while parsing'
