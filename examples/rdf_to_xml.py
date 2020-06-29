#!/usr/bin/env python


def RDF_to_XML(infile_name, outfile_name):
    # if __name__ == "__main__":
    # import sys
    from spdx.parsers.rdf import Parser
    from spdx.parsers.loggers import StandardLogger
    from spdx.parsers.rdfbuilders import Builder
    from spdx.writers.xml import write_document

    # file = sys.argv[1]
    p = Parser(Builder(), StandardLogger())
    with open(infile_name) as f:
        document, error = p.parse(f)

        if not error:
            with open(outfile_name, "w") as out:
                write_document(document, out)
        else:
            print("Errors encountered while parsing")


if __name__ == "__main__":
    import sys

    in_file = sys.argv[1]
    out_file = sys.argv[2]
    RDF_to_XML(in_file, out_file)
