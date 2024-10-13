from _typeshed import Incomplete
from codecs import CodecInfo

class CodecRegistryError(LookupError, SystemError): ...

def normalize_encoding(encoding: str | bytes) -> str: ...
def search_function(encoding: str) -> CodecInfo | None: ...

# Needed for submodules
def __getattr__(name: str) -> Incomplete: ...
