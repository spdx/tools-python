#!/usr/bin/env python

if __name__ == '__main__':
    import sys
    from spdx.parsers.tagvalue import Parser
    from spdx.parsers.loggers import StandardLogger
    from spdx.parsers.tagvaluebuilders import Builder
    from spdx.writers.xml import write_document

    file = sys.argv[1]
    p = Parser(Builder(), StandardLogger())
    p.build()
    with open(file) as f:
        data = f.read()
        document, error = p.parse(data)
        if not error:
            with open('xml_from_tv_example.xml', 'w') as out:
                write_document(document, out)
        else:
            print('Errors encountered while parsing')
