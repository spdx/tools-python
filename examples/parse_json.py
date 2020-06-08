#!/usr/bin/env python

# Parses an JSON file and prints out some basic information.
# Usage: parse_json.py <jsonfile>

if __name__ == '__main__':
    import sys
    import spdx.file as spdxfile
    from spdx.parsers.jsonparser import Parser
    from spdx.parsers.loggers import StandardLogger
    from spdx.parsers.jsonyamlxmlbuilders import Builder
    file = sys.argv[1]
    p = Parser(Builder(), StandardLogger())
    with open(file) as f:
        doc, error = p.parse(f)
        if not error:
            print(f'doc comment: {doc.comment}')
            print('Creators:')
            for c in doc.creation_info.creators:
                print(f'\t{c}')
            print('Document review information:')
            for review in doc.reviews:
                print(f'\tReviewer: {review.reviewer}')
                print(f'\tDate: {review.review_date}')
                print(f'\tComment: {review.comment}')
            print(f'Creation comment: {doc.creation_info.comment}')
            print(f'Package Name: {doc.package.name}')
            print(f'Package Version: {doc.package.version}')
            print(f'Package Download Location: {doc.package.download_location}')
            print(f'Package Homepage: {doc.package.homepage}')
            print(f'Package Checksum: {doc.package.check_sum.value}')
            print(f'Package verification code: {doc.package.verif_code}')
            print('Package excluded from verif: {0}'.format(','.join(doc.package.verif_exc_files)))
            print(f'Package license concluded: {doc.package.conc_lics}')
            print(f'Package license declared: {doc.package.license_declared}')
            print('Package licenses from files:')
            for lics in doc.package.licenses_from_files:
                print(f'\t{lics}')
            print(f'Package Copyright text: {doc.package.cr_text}')
            print(f'Package summary: {doc.package.summary}')
            print(f'Package description: {doc.package.description}')
            print('Package Files:')
            VALUES = {
                spdxfile.FileType.SOURCE: 'SOURCE',
                spdxfile.FileType.OTHER: 'OTHER',
                spdxfile.FileType.BINARY: 'BINARY',
                spdxfile.FileType.ARCHIVE: 'ARCHIVE'
            }
            for f in doc.files:
                print(f'\tFile name: {f.name}')
                print(f'\tFile type: {VALUES[f.type]}')
                print(f'\tFile Checksum: {f.chk_sum.value}')
                print(f'\tFile license concluded: {f.conc_lics}')
                print('\tFile license info in file: {0}'.format(','.join(
                     map(lambda l: l.identifier, f.licenses_in_file))))
                print('\tFile artifact of project name: {0}'.format(','.join(f.artifact_of_project_name)))

            print('Document Extracted licenses:')
            for lics in doc.extracted_licenses:
                print(f'\tIdentifier: {lics.identifier}')
                print(f'\tName: {lics.full_name}')
            print('Annotations:')
            for an in doc.annotations:
                print(f'\tAnnotator: {an.annotator}')
                print(f'\tAnnotation Date: {an.annotation_date}')
                print(f'\tAnnotation Comment: {an.comment}')
                print(f'\tAnnotation Type: {an.annotation_type}')
                print(f'\tAnnotation SPDX Identifier: {an.spdx_id}')

        else:
            print('Errors while parsing')
