if __name__ == '__main__':
    import sys
    from spdx.writers.tagvalue import write_document, InvalidDocumentError
    from spdx.document import Document, License
    from spdx.version import Version
    from spdx.creationinfo import Person
    from spdx.review import Review
    from spdx.package import Package

    doc = Document()
    doc.version = Version(1, 2)
    doc.comment = 'Example Document'
    doc.data_license = License.from_identifier('CC-1.0')
    doc.creation_info.add_creator(Person('Alice', 'alice@example.com'))
    doc.creation_info.set_created_now()
    review = Review(Person('Joe', None))
    review.set_review_date_now()
    review.comment = 'Joe reviewed this document'
    doc.add_review(review)
    doc.package = Package()

    file = sys.argv[1]
    with open(file, 'w') as out:
        try:
            write_document(doc, out)
        except InvalidDocumentError:
            print 'Document is Invlid'
            messages = []
            doc.validate(messages)
            print '\n'.join(messages)