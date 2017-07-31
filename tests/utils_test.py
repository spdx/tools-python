from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import codecs
import ntpath
import os
import posixpath
import re

import xmltodict


test_data_dir = os.path.join(os.path.dirname(__file__), 'data')


def get_test_loc(test_path, test_data_dir, debug=False, exists=True):
    """
    Given a `test_path` relative to the `test_data_dir` directory,
    return the location to a test file or directory for this path. No
    copy is done.
    """
    if debug:
        import inspect
        caller = inspect.stack()[1][3]
        print('\nget_test_loc,%(caller)s,"%(test_path)s","%(test_data_dir)s"' % locals())

    assert test_path
    assert test_data_dir

    if not os.path.exists(test_data_dir):
        raise IOError("[Errno 2] No such directory: test_data_dir not found:"
                      " '%(test_data_dir)s'" % locals())

    tpath = to_os_native_path(test_path)
    test_loc = os.path.abspath(os.path.join(test_data_dir, tpath))

    if exists and not os.path.exists(test_loc):
        raise IOError("[Errno 2] No such file or directory: "
                      "test_path not found: '%(test_loc)s'" % locals())

    return test_loc


def to_os_native_path(path):
    """
    Normalize a path to use the native OS path separator.
    """
    path = path.replace(posixpath.sep, os.path.sep)
    path = path.replace(ntpath.sep, os.path.sep)
    path = path.rstrip(os.path.sep)
    return path


def strip_variable_text(rdf_text):
    """
    Return rdf_text stripped from variable parts such as rdf nodeids
    """

    replace_nid = re.compile('rdf:nodeID="[^\"]*"').sub
    rdf_text = replace_nid('', rdf_text)

    replace_creation = re.compile('<ns1:creationInfo>.*</ns1:creationInfo>', re.DOTALL).sub
    rdf_text = replace_creation('', rdf_text)

    replace_pcc = re.compile('<ns1:packageVerificationCode>.*</ns1:packageVerificationCode>', re.DOTALL).sub
    rdf_text = replace_pcc('', rdf_text)
    return rdf_text


def load_and_clean_rdf(location):
    """
    Return plain Python nested data for the SPDX RDF file at location
    suitable for comparison. The file content is cleaned from variable
    parts such as dates, generated UUIDs and versions

    NOTE: we use plain dicts to avoid ordering issues in XML. the SPDX
    tool and lxml do not seem to return a consistent ordering that is
    needed for tests.
    """
    content = codecs.open(location, encoding='utf-8').read()
    content = strip_variable_text(content)
    data = xmltodict.parse(content, dict_constructor=dict)
    return sort_nested(data)


def sort_nested(data):
    """
    Return a new dict with any nested list sorted recursively.
    """
    if isinstance(data, dict):
        new_data = {}
        for k, v in data.items():
            if isinstance(v, list):
                v = sorted(v)
            if isinstance(v, dict):
                v = sort_nested(v)
            new_data[k] = v
        return new_data
    elif isinstance(data, list):
        new_data = []
        for v in sorted(data):
            if isinstance(v, list):
                v = sort_nested(v)
            if isinstance(v, dict):
                v = sort_nested(v)
            new_data.append(v)
        return new_data


def check_rdf_scan(expected_file, result_file, regen=False):
    """
    Check that expected and result_file are equal.
    Both are paths to SPDX RDF XML files, UTF-8 encoded.
    """
    import json
    result = load_and_clean_rdf(result_file)
    if regen:
        expected = result
        with codecs.open(expected_file, 'w', encoding='utf-8') as o:
            json.dump(expected, o, indent=2)
    else:
        with codecs.open(expected_file, 'r', encoding='utf-8') as i:
            expected = sort_nested(json.load(i))
    assert expected == result


def load_and_clean_tv(location):
    """
    Return a mapping for the SPDX TV file at location suitable for
    comparison. The file content is cleaned from variable parts such as
    dates, generated UUIDs and versions
    """
    content = codecs.open(location, encoding='utf-8').read()
    content = [l for l in content.splitlines(False)
        if l and l.strip() and not l.startswith(('Creator: ', 'Created: ',))]
    return '\n'.join(content)


def check_tv_scan(expected_file, result_file, regen=False):
    """
    Check that expected and result_file are equal.
    Both are paths to plain SPDX tv text files, UTF-8 encoded.
    """
    result = load_and_clean_tv(result_file)
    if regen:
        with codecs.open(expected_file, 'w', encoding='utf-8') as o:
            o.write(result)

    expected = load_and_clean_tv(expected_file)
    assert expected == result
