import json
import os
import re
from io import TextIOWrapper
from typing import TextIO
from urllib.request import urlopen, Request
from urllib.parse import urlparse

"""
Read SPDX model files from GitHub or a local copy (SPDX_MODEL), parse and save into a single file (GENERATED_MODEL)
"""

SPDX_MODEL = 'https://api.github.com/repos/spdx/spdx-3-model/contents/model'
GENERATED_MODEL = 'model-generated'

AUTH = {'Authorization': f'token {os.environ["GitHubToken"]}'}  # Prevent rate limiting


class WebDirEntry:
    """
    Fake os.DirEntry type for GitHub filesystem
    """
    def __init__(self, name, path, url):
        self.name = name
        self.path = path
        self.url = url


def list_dir(dirpath: str) -> dict:
    """
    Return a dict listing the files and directories in a directory on local filesystem or GitHub repo.

    :param dirpath: str - a filesystem path or GitHub API URL
    :return: dict {files: [DirEntry*], dirs: [DirEntry*]}
    Local Filesystem: Each list item is an os.DirEntry structure containing name and path attributes
    GitHub Filesystem: Each list item has name, path, and url (download URL) attributes
    """

    files, dirs = [], []
    u = urlparse(dirpath)
    if all([u.scheme, u.netloc]):
        with urlopen(Request(dirpath, headers=AUTH)) as d:
            for dl in json.loads(d.read().decode()):
                url = 'url' if dl['type'] == 'dir' else 'download_url'
                entry = WebDirEntry(dl['name'], dl[url], dl['url'])
                (dirs if dl['type'] == 'dir' else files).append(entry)
    else:
        with os.scandir(dirpath) as dlist:
            for entry in dlist:
                (dirs if os.path.isdir(entry) else files).append(entry)
    return {'files': files, 'dirs': dirs}


def open_file(fileentry: os.DirEntry) -> TextIO:
    u = urlparse(fileentry.path)
    if all([u.scheme, u.netloc]):
        return TextIOWrapper(urlopen(Request(fileentry.path, headers=AUTH)), encoding='utf8')
    return open(fileentry.path, 'r', encoding='utf8')


def load_model(fp):
    model = {}
    cursor = []
    for line in fp.readlines():
        if m := re.match(r'^\s*##\s*(.+?)(\s*)$', line):
            model[c := m.group(1)] = {}
            cursor = [model[c]]
        elif m := re.match(r'^[-*]\s*([-/\w]+):\s*(.*)\s*$', line):
            cursor[0].update({m.group(1): m.group(2)})
        elif m := re.match(r'^[-*]\s*([-/\w]+)\s*$', line):
            cursor[0][c := m.group(1)] = {}
            cursor = [cursor[0], cursor[0][c]]
        elif m := re.match(r'^\s+[-*]\s*([-/\w]+):\s*(.*)\s*$', line):
            cursor[1].update({m.group(1): m.group(2)})
    return model


if __name__ == '__main__':
    os.makedirs(GENERATED_MODEL, exist_ok=True)

    modelRefs = {}
    modelTypes = {}
    e1 = list_dir(SPDX_MODEL)
    assert len(e1['files']) == 0
    for d1 in e1['dirs']:
        print(f'{d1.name}')
        e2 = list_dir(d1.path)
        assert len(e2['files']) == 1
        prefix = load_model(open_file((e2['files'][0])))['Metadata']['id']
        for d2 in e2['dirs']:
            # print(f'. {d2.name}')
            e3 = list_dir(d2.path)
            assert len(e3['dirs']) == 0
            assert d2.name in {'Classes', 'Individuals', 'Properties', 'Vocabularies'}
            if d2.name in {'Classes', 'Vocabularies'}:
                for f3 in e3['files']:
                    if not f3.name.startswith('_'):
                        model = load_model(open_file(f3))
                        meta = model['Metadata']
                        if meta['name'] in modelRefs:
                            m = modelTypes[meta['name']]['Metadata']
                            print(f"###### Duplicate: {meta['name']} in {m['_profile']}/{m['_file']}, {d1.name}/{f3.name}")
                        ref = '/'.join((prefix, meta['name']))
                        modelRefs[meta['name']] = ref
                        meta['_modelRef'] = ref
                        meta['_profile'] = d1.name
                        meta['_category'] = d2.name
                        meta['_file'] = f3.name
                        modelTypes[meta['name']] = model
                    else:
                        print('###### Ignored:', f3.name)

    # Dump list of model URIs and full parsed model into output dir
    print(f'\n{len(modelTypes)} Types in model')
    with open(os.path.join(GENERATED_MODEL, 'modelRefs.json'), 'w') as fp:
        json.dump(modelRefs, fp, indent=2)
    with open(os.path.join(GENERATED_MODEL, 'modelTypes.json'), 'w') as fp:
        json.dump(modelTypes, fp, indent=2)

