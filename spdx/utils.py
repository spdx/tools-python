# Copyright 2014 Ahmed H. Ismail

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import re
import datetime

def datetime_iso_format(date):
        return "{0:0>4}-{1:0>2}-{2:0>2}T{3:0>2}:{4:0>2}:{5:0>2}Z".format(
                date.year, date.month, date.day, date.hour, 
                date.minute, date.second)

DATE_ISO_REGEX = re.compile(r'(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)Z', 
                    re.UNICODE)
DATE_ISO_YEAR_GRP = 1
DATE_ISO_MONTH_GRP = 2
DATE_ISO_DAY_GRP = 3
DATE_ISO_HOUR_GRP = 4
DATE_ISO_MIN_GRP = 5
DATE_ISO_SEC_GRP = 6

def datetime_from_iso_format(string):
    match = DATE_ISO_REGEX.match(string)
    if match:
        date = datetime.datetime(year=int(match.group(DATE_ISO_YEAR_GRP)), 
            month=int(match.group(DATE_ISO_MONTH_GRP)), 
            day=int(match.group(DATE_ISO_DAY_GRP)),
            hour=int(match.group(DATE_ISO_HOUR_GRP)), 
            second=int(match.group(DATE_ISO_SEC_GRP)),
            minute=int(match.group(DATE_ISO_MIN_GRP)))
        return date
    else:
        return None

class NoAssert(object):
    pass

