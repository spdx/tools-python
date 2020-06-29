#!/usr/bin/env python


def TAG_to_YAML(infile_name, outfile_name):
    # if __name__ == "__main__":
    # import sys
    from spdx.parsers.tagvalue import Parser
    from spdx.parsers.loggers import StandardLogger
    from spdx.parsers.tagvaluebuilders import Builder
    from spdx.writers.yaml import write_document

    # file = sys.argv[1]
    p = Parser(Builder(), StandardLogger())
    p.build()
    with open(infile_name) as f:
        data = f.read()
        document, error = p.parse(data)
        if not error:
            with open(outfile_name, "w") as out:
                write_document(document, out)
        else:
            print("Errors encountered while parsing")


if __name__ == "__main__":
    import sys

    in_file = sys.argv[1]
    out_file = sys.argv[2]
    TAG_to_YAML(in_file, out_file)
