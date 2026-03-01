# SPDX-FileCopyrightText: 2022 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import re
from datetime import datetime, timezone


def datetime_from_str(date_str: str) -> datetime:
    if not isinstance(date_str, str):
        raise TypeError(f"Could not convert str to datetime, invalid type: {type(date_str).__name__}")

    if "." not in date_str:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")  # raises ValueError if format does not match

    # Based on the https://www.w3.org/TR/xmlschema11-2/#dateTimeStamp
    # The secondFrag allows fractional second notation as well.
    # normalize to micro seconds so that we can use %f with strptime
    date_str = re.sub(r"\.(\d{1,6})\d*Z$", r".\1Z", date_str)
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")  # raises ValueError if format does not match


def datetime_to_iso_string(date: datetime) -> str:
    """
    Return an ISO-8601 representation of a datetime object.
    """
    if date.tzinfo is not None:
        date = date.astimezone(timezone.utc)  # Convert aware datetimes to UTC
        date = date.replace(tzinfo=None)  # Convert to naive datetime

    if date.microsecond != 0:
        date = date.replace(microsecond=0)  # SPDX does not support microseconds

    return date.isoformat() + "Z"
