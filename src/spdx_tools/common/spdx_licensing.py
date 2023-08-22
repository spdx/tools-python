# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
from license_expression import get_spdx_licensing

# this getter takes quite long so we only call it once in this singleton module
spdx_licensing = get_spdx_licensing()
