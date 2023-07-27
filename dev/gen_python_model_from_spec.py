# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

"""
Auto-generates the python model representation from the SPDX3 model spec.

Usage: fetch a fresh copy of the spdx-3-model and the spec-parser, then generate a json dump of the model with
the spec-parser:

    python main.py --json-dump ../spdx-3-model/model

Copy the generated `model_dump.json` in `md_generated` next to this file, then run it:

    python gen_python_model_from_spec.py

Commit resulting changes.

Note: needs an additional dependency for proper formatting of docstrings:

    pip install mistletoe
"""

import json
import os.path
from pathlib import Path

from model_gen.gen_class import GenClassFromSpec
from model_gen.general_templates import FILE_HEADER
from model_gen.utils import (
    SPECIAL_TYPE_MAPPINGS,
    get_file_path,
    get_python_docstring,
    get_qualified_name,
    namespace_name_to_python,
)
from model_gen.vocab_templates import VOCAB_ENTRY, VOCAB_FILE, VOCAB_STR_TO_VALUE, VOCAB_VALUE_TO_STR

from spdx_tools.spdx.casing_tools import camel_case_to_snake_case

# TODO: use the actual model package path rather than a separate path
output_dir = os.path.join(os.path.dirname(__file__), "../src/spdx_tools/spdx3/new_model")


class GenPythonModelFromSpec:
    namespace_imports: str
    init_imports: dict[str, dict[str, str]]

    def __init__(self):
        self.namespace_imports = ""
        self.init_imports = {}

    def create_namespace_import(self, model: dict):
        namespaces = [namespace_name_to_python(namespace["name"]) for namespace in model.values()]
        if namespaces:
            self.namespace_imports = "from . import " + ", ".join(namespaces)

    def handle_class(self, clazz: dict, namespace_name: str, model: dict):
        qualified_name = get_qualified_name(clazz["metadata"]["name"], namespace_name)
        if qualified_name in SPECIAL_TYPE_MAPPINGS:
            # do not generate Python classes for types we are mapping differently
            return

        clsinfo = GenClassFromSpec(clazz, namespace_name, model, output_dir)
        clsinfo.gen_file()

        if namespace_name not in self.init_imports:
            self.init_imports[namespace_name] = dict()
        self.init_imports[namespace_name][clsinfo.filename] = clsinfo.typename

    def handle_vocab(self, vocab: dict, namespace_name: str):
        typename = vocab["metadata"]["name"]
        python_typename = camel_case_to_snake_case(typename)
        values_text = "\n".join([VOCAB_ENTRY.format(value=camel_case_to_snake_case(value).upper(),
                                                    docstring=get_python_docstring(description, 4)) for
                                 value, description in vocab["entries"].items()])
        values_to_str_text = "\n".join([VOCAB_VALUE_TO_STR.format(python_value=camel_case_to_snake_case(value).upper(),
                                                                  str_value=value, typename=typename) for value in
                                        vocab["entries"]])
        str_to_values_text = "\n".join([VOCAB_STR_TO_VALUE.format(python_value=camel_case_to_snake_case(value).upper(),
                                                                  str_value=value, typename=typename) for value in
                                        vocab["entries"]])
        docstring = get_python_docstring(vocab["description"], 4)
        file_path = get_file_path(typename, namespace_name, output_dir)
        with open(file_path, "w") as output_file:
            output_file.write(VOCAB_FILE.format(typename=typename, values=values_text,
                                                values_to_str=values_to_str_text, str_to_values=str_to_values_text,
                                                python_typename=python_typename, docstring=docstring))

        if namespace_name not in self.init_imports:
            self.init_imports[namespace_name] = dict()
        self.init_imports[namespace_name][python_typename] = typename

    def handle_namespace(self, namespace: dict, model: dict):
        namespace_name = namespace["name"]
        namespace_path = os.path.join(output_dir, namespace_name_to_python(namespace_name))
        os.makedirs(namespace_path, exist_ok=True)
        for clazz in namespace["classes"].values():
            self.handle_class(clazz, namespace_name, model)
        for vocab in namespace["vocabs"].values():
            self.handle_vocab(vocab, namespace_name)

        if namespace_name in self.init_imports:
            with open(os.path.join(output_dir, namespace_name_to_python(namespace_name), "__init__.py"),
                      "w") as init_file:
                init_file.write(FILE_HEADER)
                for module, typename in sorted(self.init_imports[namespace_name].items()):
                    init_file.write(f"from .{module} import {typename}\n")

    def run(self):
        os.makedirs(output_dir, exist_ok=True)
        Path(os.path.join(output_dir, "__init__.py")).touch()

        with open("model_dump.json") as model_file:
            model = json.load(model_file)

        self.create_namespace_import(model)

        for namespace in model.values():
            self.handle_namespace(namespace, model)

        with open(os.path.join(output_dir, "__init__.py"), "w") as init_file:
            init_file.write(FILE_HEADER)
            namespace_imports = ", ".join(
                [namespace_name_to_python(namespace) for namespace in self.init_imports.keys()])
            init_file.write(f"from . import {namespace_imports}\n")
            init_file.write("from .core import *\n")

        os.system(f'black "{output_dir}"')
        os.system(f'isort "{output_dir}"')


if __name__ == "__main__":
    GenPythonModelFromSpec().run()
