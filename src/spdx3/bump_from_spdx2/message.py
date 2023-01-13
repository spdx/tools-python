#  Copyright (c) 2023 spdx contributors
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

MISSING_CONVERSION_REASONS = {0: "missing conversion rule", 1: "missing implementation"}


def print_missing_conversion(field: str, reason, additional_information: str= ""):
    print(f"{field} not converted: {MISSING_CONVERSION_REASONS[reason]} {additional_information}")
