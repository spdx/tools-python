# Copyright (c) 2022 spdx contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
from typing import List

from uritools import isabsuri, urisplit

url_pattern = "(http:\\/\\/www\\.|https:\\/\\/www\\.|http:\\/\\/|https:\\/\\/|ssh:\\/\\/|git:\\/\\/|svn:\\/\\/|sftp:\\/\\/|ftp:\\/\\/)?[a-z0-9]+([\\-\\.]{1}[a-z0-9]+){0,100}\\.[a-z]{2,5}(:[0-9]{1,5})?(\\/.*)?"
supported_download_repos: str = "(git|hg|svn|bzr)"
git_pattern = "(git\\+git@[a-zA-Z0-9\\.\\-]+:[a-zA-Z0-9/\\\\.@\\-]+)"
bazaar_pattern = "(bzr\\+lp:[a-zA-Z0-9\\.\\-]+)"
download_location_pattern = (
    "^(((" + supported_download_repos + "\\+)?" + url_pattern + ")|" + git_pattern + "|" + bazaar_pattern + ")$")


def validate_url(url: str) -> List[str]:
    if not re.match(url_pattern, url):
        return [f"must be a valid URL, but is: {url}"]

    return []


def validate_download_location(location: str) -> List[str]:
    if not re.match(download_location_pattern, location):
        return [f"must be a valid download location according to the specification, but is: {location}"]

    return []


def validate_uri(uri: str) -> List[str]:
    if not isabsuri(uri):
        return [f"must be a valid URI specified in RFC-3986 and must contain no fragment (#), but is: {uri}"]
    else:
        split = urisplit(uri)
        if split.scheme is None:
            return [f"must have a URI scheme, but is: {uri}"]

    return []
