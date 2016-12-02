#!/usr/bin/env python

# Parses a tag/value file and prints out some basic information.
# Usage: parse_tv.py <tagvaluefile>

if __name__ == '__main__':
    import sys
    from spdx.parsers.tagvalue import Parser
    from spdx.parsers.loggers import StandardLogger
    from spdx.parsers.tagvaluebuilders import Builder
    file = sys.argv[1]
    p = Parser(Builder(), StandardLogger())
    p.build()
    with open(file) as f:
        data = f.read()
        document, error = p.parse(data)
        if not error:
            print 'Parsing Successful'
            print 'Document Version {0}.{1}'.format(document.version.major,
                document.version.minor)
            print 'Package name : {0}'.format(document.package.name)
            print 'Creators : '
            for creator in document.creation_info.creators:
                print creator.name
        else:
            print 'Errors encountered while parsing'
