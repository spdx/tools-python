# SPDX-FileCopyrightText: 2026-present SPDX contributors
# SPDX-License-Identifier: Apache-2.0
from typing import Any, Iterable, Optional, Protocol, Set, runtime_checkable


@runtime_checkable
class SpdxObjectSet(Protocol):
    """Version-agnostic structural type for a SHACL object set.

    Satisfied by ``SHACLObjectSet`` from any ``spdx_python_model.vX_Y_Z``
    version module, so callers are not tied to a specific SPDX spec version.
    """

    def foreach(self) -> Iterable[Any]: ...

    def foreach_type(self, typ: Any, *, match_subclass: bool = True) -> Iterable[Any]: ...

    def find_by_id(self, _id: str, default: Optional[Any] = None) -> Optional[Any]: ...

    def add(self, obj: Any) -> Any: ...

    def link(self) -> Set[str]: ...
