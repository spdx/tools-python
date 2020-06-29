#!/usr/bin/env python


def RDF_to_JSON(input_file, out_file):
    # if __name__ == "__main__":
    import sys
    from spdx.parsers.rdf import Parser
    from spdx.parsers.loggers import StandardLogger
    from spdx.parsers.rdfbuilders import Builder
    from spdx.writers.json import write_document

    # input_file = sys.argv[1]
    # out_file = sys.argv[2]
    p = Parser(Builder(), StandardLogger())
    with open(input_file) as f:
        document, error = p.parse(f)

        if not error:
            with open(out_file, "w") as out:
                write_document(document, out)
        else:
            print("Errors encountered while parsing")


if __name__ == "__main__":
    import sys

    in_file = sys.argv[1]
    out_file = sys.argv[2]
    RDF_to_JSON(in_file, out_file)
