if __name__ == '__main__':
    import sys
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
            print 'Creation comment: {0}'.format(doc.creation_info.comment)

        else:
            print 'Errors while parsing'