#!/usr/bin/env python

if __name__ == '__main__':
    import sys
    from spdx.parsers.rdf import Parser
    from spdx.parsers.loggers import StandardLogger
    from spdx.parsers.rdfbuilders import Builder
    from spdx.writers.yaml import write_document

    file = sys.argv[1]
    p = Parser(Builder(), StandardLogger())
    with open(file) as f:
        document, error = p.parse(f)
        
        if not error:
            with open('yaml_from_rdf_example.yml', 'w') as out:
                write_document(document, out)
        else:
            print('Errors encountered while parsing')
