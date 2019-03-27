from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import ruamel.yaml as yaml
from spdx.writers.tagvalue import InvalidDocumentError
from spdx.writers.jsonyaml import Writer
import rdflib

def write_document(document, out, validate=True):

    if validate:
        messages = []
        messages = document.validate(messages)
        if messages:
            raise InvalidDocumentError(messages)

    writer = Writer(document)
    document_object = writer.create_document()

    yaml.round_trip_dump(document_object, out, indent=2, explicit_start=True)
