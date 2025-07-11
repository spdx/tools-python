# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0

import re

from beartype.typing import List
from uritools import isabsuri, urisplit

url_pattern = (
    "(http:\\/\\/www\\.|https:\\/\\/www\\.|http:\\/\\/|https:\\/\\/|ssh:\\/\\/|git:\\/\\/|svn:\\/\\/|sftp:"
    "\\/\\/|ftp:\\/\\/)?([\\w\\-.!~*'()%;:&=+$,]+@)?[a-z0-9]+([\\-\\.]{1}[a-z0-9]+){0,100}\\.[a-z]{2,5}"
    "(:[0-9]{1,5})?(\\/.*)?"
)
url_pattern_ignore_case = re.compile(url_pattern, re.IGNORECASE)

supported_download_repos: str = "(git|hg|svn|bzr)"
git_pattern = "(git\\+git@[a-zA-Z0-9\\.\\-]+:[a-zA-Z0-9/\\\\.@\\-]+)"
bazaar_pattern = "(bzr\\+lp:[a-zA-Z0-9\\.\\-]+)"
download_location_pattern = (
    "^(((" + supported_download_repos + "\\+)?" + url_pattern + ")|" + git_pattern + "|" + bazaar_pattern + ")$"
)
compiled_pattern = re.compile(download_location_pattern, re.IGNORECASE)


def validate_url(url: str) -> List[str]:
    if not url_pattern_ignore_case.match(url):
        return [f"must be a valid URL, but is: {url}"]

    return []


def validate_download_location(location: str) -> List[str]:
    if not (validate_url(location) == [] or compiled_pattern.match(location)):
        return [f"must be a valid URL or download location according to the specification, but is: {location}"]

    return []


def validate_uri(uri: str) -> List[str]:
    if not isabsuri(uri):
        return [f"must be a valid URI specified in RFC-3986 and must contain no fragment (#), but is: {uri}"]
    else:
        split = urisplit(uri)
        if split.scheme is None:
            return [f"must have a URI scheme, but is: {uri}"]

    return []
