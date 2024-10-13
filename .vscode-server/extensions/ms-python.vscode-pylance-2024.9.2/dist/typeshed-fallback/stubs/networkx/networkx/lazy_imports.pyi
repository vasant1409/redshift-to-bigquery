import types
from _typeshed import Incomplete

__all__ = ["attach", "_lazy_import"]

def attach(module_name, submodules: Incomplete | None = None, submod_attrs: Incomplete | None = None): ...

class DelayedImportErrorModule(types.ModuleType):
    def __init__(self, frame_data, *args, **kwargs) -> None: ...
    def __getattr__(self, x) -> None: ...

def _lazy_import(fullname) -> types.ModuleType | DelayedImportErrorModule: ...
