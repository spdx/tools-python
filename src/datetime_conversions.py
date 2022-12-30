#  Copyright (c) 2022 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from datetime import datetime


def datetime_from_str(date_str: str) -> datetime:
    if not isinstance(date_str, str):
        raise TypeError(f"Could not convert str to datetime, invalid type: {type(date_str).__name__}")

    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ") # raises ValueError if format does not match
    return date

def datetime_to_iso_string(date: datetime) -> str:
    """
    Return an ISO-8601 representation of a datetime object.
    """
    return date.isoformat() + "Z"

