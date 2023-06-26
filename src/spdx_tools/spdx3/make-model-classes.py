import json
import os

GENERATED_MODEL = 'model-generated'


def write_tools_class(model, mtypes):
    for m in model['Metadata']:
        assert m in {'name', 'SubclassOf', 'Instantiability',
                     '_modelRef', '_profile', '_category', '_file'}

    pdir = os.path.join(GENERATED_MODEL, model['Metadata']['_profile'])
    os.makedirs(pdir, exist_ok=True)
    classname = model['Metadata']['name']
    parentname = model['Metadata'].get('SubclassOf', '')
    if model['Metadata']['_category'] != 'Vocabularies':
        print(f'{parentname:36} {classname}')
    imported = [parentname]
    with open(os.path.join(pdir, model['Metadata']['name']) + '.py', 'w') as fp:
        fp.write(
            f'# SPDX-FileCopyrightText: 2023 spdx contributors\n'
            f'#\n'
            f'# SPDX-License-Identifier: Apache-2.0\n'
            f'from dataclasses import field\n'
            f'from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties\n'
            f'from spdx_tools.common.typing.type_checks import check_types_and_set_values\n'
            f'from spdx_tools.spdx3.model import CreationInfo, Element, ExternalIdentifier, ExternalReference, IntegrityMethod\n'
            f'\n\n'
            f'@dataclass_with_properties\n'
            f'class {classname}({parentname}):\n'
            f'    def __init__(\n'
            f'        self,\n'
        )
        if model['Metadata']['_category'] == 'Classes':
            for k, v in model['Properties'].items():
                pass    # generate properties

        fp.write(
            f'    ):\n'
            f'        check_types_and_set_values(self, locals())\n'
        )


if __name__ == '__main__':
    # Load parsed model file created by "load_model"
    with open(os.path.join(GENERATED_MODEL, 'modelTypes.json')) as fp:
        modelTypes = json.load(fp)

    # Create class files for all model classes in output dir
    print(f'\n{"      Class":36} {"    Subclass"}')
    for mtype in modelTypes.values():
        write_tools_class(mtype, modelTypes)
