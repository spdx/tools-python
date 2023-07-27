# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import logging
from dataclasses import dataclass

from beartype.typing import Optional

from spdx_tools.spdx.casing_tools import camel_case_to_snake_case

from .class_templates import (
    CLS_FILE,
    CLS_IMPORTS,
    CLS_INIT,
    CLS_INIT_ABSTRACT,
    CLS_INIT_ARG,
    CLS_INIT_ARG_OPT,
    CLS_INIT_REMAP,
    CLS_PROP,
)
from .utils import (
    SPECIAL_TYPE_MAPPINGS,
    extract_parent_type,
    get_file_path,
    get_python_docstring,
    get_qualified_name,
    namespace_name_to_python,
    prop_name_to_python,
    split_qualified_name,
    to_python_type,
)

SPECIAL_PROPTYPE_MAPPINGS: dict[str, tuple[str, Optional[str]]] = {
    # for the moment, we replace Element and Agent references with string references to their ID
    # otherwise, there is a cyclic dependency between CreationInfo and Agent/Tool that is problematic to deal with
    "Core/Agent": ("str", None),
    "Core/Element": ("str", None),
    "Core/Tool": ("str", None),
}


@dataclass
class Property:
    name: str
    type: str
    optional: bool
    is_list: bool
    inherited: bool

    def get_python_type(self) -> str:
        if self.type == "Core/DictionaryEntry":
            return "Dict[str, Optional[str]]"
        if self.type in SPECIAL_PROPTYPE_MAPPINGS:
            prop_type = SPECIAL_PROPTYPE_MAPPINGS[self.type][0]
        else:
            prop_type = to_python_type(self.type)
        if self.is_list:
            prop_type = f"List[{prop_type}]"
        elif self.optional:
            prop_type = f"Optional[{prop_type}]"
        return prop_type


class GenClassFromSpec:
    cls: dict
    model: dict

    typename: str
    namespace: str
    filename: str
    file_path: str
    parent_class: str
    docstring: str
    # module -> types
    imports: dict[str, set[str]]
    props: list[Property]

    def __init__(self, cls: dict, namespace: str, model: dict, output_dir: str):
        self.cls = cls
        self.namespace = namespace
        self.model = model
        self.imports = dict()
        self.props = list()

        self.typename = cls["metadata"]["name"]
        self.filename = camel_case_to_snake_case(self.typename) if self.typename != "AIPackage" else "ai_package"
        parent_class = extract_parent_type(cls, namespace)
        if not parent_class:
            self.parent_class = "ABC"
            self._add_import("abc", "ABC")
        else:
            self.parent_class = to_python_type(parent_class)
            self._import_spdx_type(parent_class)
        self.docstring = get_python_docstring(cls["description"], 4)
        self.file_path = get_file_path(self.typename, namespace, output_dir)

        self._collect_props(self.cls, self.namespace, False)

    def _add_import(self, module: str, typename: str):
        if module not in self.imports:
            self.imports[module] = set()
        self.imports[module].add(typename)

    def _import_spdx_type(self, typename: str):
        if typename in SPECIAL_TYPE_MAPPINGS:
            import_type, import_module = SPECIAL_TYPE_MAPPINGS[typename]
            if import_module:
                self._add_import(import_module, import_type)
            return
        if typename.startswith("xsd:"):
            return
        namespace, typename = split_qualified_name(typename)
        module = camel_case_to_snake_case(typename) if typename != "AIPackage" else "ai_package"
        python_path = f"..{namespace_name_to_python(namespace)}.{module}"
        self._add_import(python_path, typename)

    def _find_prop(self, propname: str) -> Optional[Property]:
        propname = prop_name_to_python(propname)
        return next(filter(lambda p: prop_name_to_python(p.name) == propname, self.props), None)

    def _collect_props(self, cls: dict, namespace: str, is_parent: bool):
        parent = extract_parent_type(cls, namespace)
        if parent:
            parent_namespace, parent_class = split_qualified_name(parent)
            if parent_namespace in self.model and parent_class in self.model[parent_namespace]["classes"]:
                self._collect_props(self.model[parent_namespace]["classes"][parent_class], parent_namespace, True)

        for propname, propinfo in cls["properties"].items():
            if self._find_prop(propname):
                logging.warning("Class %s is redefining property %s from a parent class, ignoring",
                                cls["metadata"]["name"], propname)
                continue
            propname = get_qualified_name(propname, namespace)
            proptype = get_qualified_name(propinfo["type"], namespace)
            optional = "minCount" not in propinfo or propinfo["minCount"] == "0"
            is_list = "maxCount" not in propinfo or propinfo["maxCount"] != "1"
            prop = Property(propname, proptype, optional, is_list, is_parent)
            self.props.append(prop)

        if "externalPropertyRestrictions" not in cls:
            return
        for propname, propinfo in cls["externalPropertyRestrictions"].items():
            prop = self._find_prop(propname)
            if not prop:
                continue
            if "minCount" in propinfo:
                prop.optional = prop.optional and propinfo["minCount"] == "0"
            if "maxCount" in propinfo:
                prop.is_list = prop.is_list and propinfo["maxCount"] != "1"

    def gen_file(self):
        properties = self._gen_props()
        constructor = self._gen_constructor()
        # imports should be last, as we may add additional types to import during generation
        imports = self._gen_imports()
        with open(self.file_path, "w") as output_file:
            output_file.write(
                CLS_FILE.format(typename=self.typename, parent=self.parent_class, docstring=self.docstring,
                                properties=properties, imports=imports, constructor=constructor))

    def _gen_imports(self) -> str:
        imports = ""
        for module in sorted(self.imports.keys()):
            types = ", ".join(sorted(self.imports[module]))
            imports += CLS_IMPORTS.format(module=module, types=types)
        return imports

    def _import_prop_type(self, prop: Property):
        if prop.type in SPECIAL_PROPTYPE_MAPPINGS:
            import_type, import_module = SPECIAL_PROPTYPE_MAPPINGS[prop.type]
            if import_module:
                self._add_import(import_module, import_type)
        else:
            self._import_spdx_type(prop.type)

        if prop.type == "Core/DictionaryEntry":
            self._add_import("beartype.typing", "Dict")
            self._add_import("beartype.typing", "Optional")
        elif prop.is_list:
            self._add_import("beartype.typing", "List")
        elif prop.optional:
            self._add_import("beartype.typing", "Optional")

    def _gen_props(self) -> str:
        code = ""
        own_props = (prop for prop in self.props if not prop.inherited)
        for prop in own_props:
            name = prop_name_to_python(prop.name)
            proptype = prop.get_python_type()
            docstring = self._get_prop_docstring(prop.name)
            self._import_prop_type(prop)
            if prop.type == "Core/DictionaryType":
                default = " = field(default_factory=dict)"
                self._add_import("dataclasses", "field")
            elif prop.is_list:
                default = " = field(default_factory=list)"
                self._add_import("dataclasses", "field")
            else:
                default = " = None"
            code += CLS_PROP.format(prop_name=name, prop_type=proptype, default=default, docstring=docstring)
        return code

    def _get_prop_docstring(self, name: str) -> str:
        namespace, propname = split_qualified_name(name)
        if namespace not in self.model or "properties" not in self.model[namespace]:
            return ""
        prop = self.model[namespace]["properties"].get(propname)
        if not prop:
            return ""
        return get_python_docstring(prop["description"], 4)

    def _gen_constructor(self) -> str:
        if self.cls["metadata"].get("Instantiability") == "Abstract":
            self._add_import("abc", "abstractmethod")
            return CLS_INIT_ABSTRACT

        self._add_import("spdx_tools.common.typing.type_checks", "check_types_and_set_values")
        args = ""
        remaps = ""
        required_props = (prop for prop in self.props if not prop.optional)
        optional_props = (prop for prop in self.props if prop.optional)
        for prop in required_props:
            self._import_prop_type(prop)
            args += CLS_INIT_ARG.format(prop_name=prop_name_to_python(prop.name), prop_type=prop.get_python_type())
        for prop in optional_props:
            self._import_prop_type(prop)
            prop_name = prop_name_to_python(prop.name)
            args += CLS_INIT_ARG_OPT.format(prop_name=prop_name, prop_type=prop.get_python_type())
            if prop.type == "Core/DictionaryEntry":
                remaps += CLS_INIT_REMAP.format(prop_name=prop_name, default="{}")
            elif prop.is_list:
                remaps += CLS_INIT_REMAP.format(prop_name=prop_name, default="[]")
        return CLS_INIT.format(arguments=args, remaps=remaps)
