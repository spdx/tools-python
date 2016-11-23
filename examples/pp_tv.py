#!/usr/bin/env python

# Parses a tag/value file and writes it out pretty-printed.
# Usage: pp_tv <infile> <outfile>

if __name__ == '__main__':
    import sys
    import codecs
    from spdx.writers.tagvalue import write_document, InvalidDocumentError
    from spdx.parsers.tagvalue import Parser
    from spdx.parsers.loggers import StandardLogger
    from spdx.parsers.tagvaluebuilders import Builder
    source = sys.argv[1]
    target = sys.argv[2]
    p = Parser(Builder(), StandardLogger())
    p.build()
    with open(source, 'r') as f:
        data = f.read()
        document, error = p.parse(data)
        if not error:
            print 'Parsing Successful'
            with codecs.open(target, mode='w', encoding='utf-8') as out:
                try:
                    write_document(document, out)
                except InvalidDocumentError:
                    print 'Document is Invalid'
                    messages = []
                    document.validate(messages)
                    print '\n'.join(messages)
        else:
            print 'Errors encountered while parsing'
