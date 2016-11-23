#!/usr/bin/env python

# Parses an RDF file and writes it out pretty-printed.
# Usage: pp_rdf <infile> <outfile>

if __name__ == '__main__':
    import sys
    import spdx.file as spdxfile
    from spdx.parsers.rdf import Parser
    from spdx.parsers.loggers import StandardLogger
    from spdx.parsers.rdfbuilders import Builder
    from spdx.writers.rdf import write_document
    infile = sys.argv[1]
    outfile = sys.argv[2]
    p = Parser(Builder(), StandardLogger())
    with open(infile) as f:
        doc, error = p.parse(f)
        if not error:
            with open(outfile, mode='w') as out:
                write_document(doc, out)

        else:
            print 'Errors while parsing'
