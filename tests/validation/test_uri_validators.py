
from uritools import isuri, isabsuri
import pytest

from src.validation.uri_validators import validate_url, validate_package_download_location, validate_uri


@pytest.mark.parametrize("input_value", ['https://some.url', "https://spdx.org/spdxdocs/spdx-tools-v1.2-3F2504E0-4F89-41D3-9A0C-0305E82...",
                                         "http://some.url", "http://ftp.gnu.org/gnu/glibc/glibc-ports-2.15.tar.gz"])
def test_valid_url(input_value):
    assert validate_url(input_value) == []


# TODO: more negative examples
@pytest.mark.parametrize("input_value", [':::::', ])
def test_invalid_url(input_value):
    assert validate_url(input_value) == [f'must be a valid URL, but is: {input_value}']


@pytest.mark.parametrize("input_value", ["http://ftp.gnu.org/gnu/glibc/glibc-ports-2.15.tar.gz",
                                         "git://git.myproject.org/MyProject",
                                         "git+https://git.myproject.org/MyProject.git",
                                         "git+http://git.myproject.org/MyProject",
                                         "git+ssh://git.myproject.org/MyProject.git",
                                         "git+git://git.myproject.org/MyProject",
                                         "git+git@git.myproject.org:MyProject",
                                         "git://git.myproject.org/MyProject#src/somefile.c",
                                         "git+https://git.myproject.org/MyProject#src/Class.java",
                                         "git://git.myproject.org/MyProject.git@master",
                                         "git+https://git.myproject.org/MyProject.git@v1.0",
                                         "git://git.myproject.org/MyProject.git@da39a3ee5e6b4b0d3255bfef95601890afd80709",
                                         "git+https://git.myproject.org/MyProject.git@master#/src/MyClass.cpp",
                                         "git+https://git.myproject.org/MyProject@da39a3ee5e6b4b0d3255bfef95601890afd80709#lib/variable.rb",
                                         "hg+http://hg.myproject.org/MyProject",
                                         "hg+https://hg.myproject.org/MyProject",
                                         "hg+ssh://hg.myproject.org/MyProject",
                                         "hg+https://hg.myproject.org/MyProject#src/somefile.c",
                                         "hg+https://hg.myproject.org/MyProject#src/Class.java",
                                         "hg+https://hg.myproject.org/MyProject@da39a3ee5e6b",
                                         "hg+https://hg.myproject.org/MyProject@2019",
                                         "hg+https://hg.myproject.org/MyProject@v1.0",
                                         "hg+https://hg.myproject.org/MyProject@special_feature",
                                         "hg+https://hg.myproject.org/MyProject@master#/src/MyClass.cpp",
                                         "hg+https://hg.myproject.org/MyProject@da39a3ee5e6b#lib/variable.rb",
                                         "svn://svn.myproject.org/svn/MyProject",
                                         "svn+svn://svn.myproject.org/svn/MyProject",
                                         "svn+http://svn.myproject.org/svn/MyProject/trunk",
                                         "svn+https://svn.myproject.org/svn/MyProject/trunk",
                                         "svn+https://svn.myproject.org/MyProject#src/somefile.c",
                                         "svn+https://svn.myproject.org/MyProject#src/Class.java",
                                         "svn+https://svn.myproject.org/MyProject/trunk#src/somefile.c",
                                         "svn+https://svn.myproject.org/MyProject/trunk/src/somefile.c",
                                         "svn+https://svn.myproject.org/svn/MyProject/trunk@2019",
                                         "svn+https://svn.myproject.org/MyProject@123#/src/MyClass.cpp",
                                         "svn+https://svn.myproject.org/MyProject/trunk@1234#lib/variable/variable.rb",
                                         "bzr+https://bzr.myproject.org/MyProject/trunk",
                                         "bzr+http://bzr.myproject.org/MyProject/trunk",
                                         "bzr+sftp://myproject.org/MyProject/trunk",
                                         "bzr+ssh://myproject.org/MyProject/trunk",
                                         "bzr+ftp://myproject.org/MyProject/trunk",
                                         "bzr+lp:MyProject",
                                         "bzr+https://bzr.myproject.org/MyProject/trunk#src/somefile.c",
                                         "bzr+https://bzr.myproject.org/MyProject/trunk#src/Class.java",
                                         "bzr+https://bzr.myproject.org/MyProject/trunk@2019",
                                         "bzr+http://bzr.myproject.org/MyProject/trunk@v1.0",
                                         "bzr+https://bzr.myproject.org/MyProject/trunk@2019#src/somefile.c",
                                         ])
def test_valid_package_download_location(input_value):
    assert validate_package_download_location(input_value) == []


# TODO: more negative examples
@pytest.mark.parametrize("input_value", [':::::', ])
def test_invalid_package_download_location(input_value):
    assert validate_package_download_location(input_value) == [f'must be a valid download location, but is: {input_value}']


@pytest.mark.parametrize("input_value", ['https://some.uri', "http:////some", "https://spdx.org/spdxdocs/spdx-tools-v1.2-3F2504E0-4F89-41D3-9A0C-0305E82...",
                                         'h://someweirdtest^?', "https://some.uri that goes on!?"])
def test_valid_uri(input_value):
    message = validate_uri(input_value)

    assert message == []
    

@pytest.mark.parametrize("input_value", ["/invalid/uri", "http//uri", "http://some#uri", "some/uri", 'some weird test'])
def test_invalid_uri(input_value):
    message = validate_uri(input_value)
    
    assert message == [f'must be a valid URI specified in RFC-3986, but is: {input_value}']


@pytest.mark.parametrize("input_value", ['://spdx.org/spdxdocs/spdx-tools-v1.2-3F2504E0-4F89-41D3-9A0C-0305E82...'])
def test_uri_without_scheme(input_value):
    message = validate_uri(input_value)

    assert message == [f'must have a URI scheme, but is: {input_value}']

