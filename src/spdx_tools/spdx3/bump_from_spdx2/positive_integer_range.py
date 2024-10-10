from beartype.typing import Optional, Tuple

from ..model.core import PositiveIntegerRange

def bump_positive_integer_range(spdx2_range: Optional[Tuple[int, int]]) -> PositiveIntegerRange:
    return PositiveIntegerRange(spdx2_range[0], spdx2_range[1]) if spdx2_range else None
