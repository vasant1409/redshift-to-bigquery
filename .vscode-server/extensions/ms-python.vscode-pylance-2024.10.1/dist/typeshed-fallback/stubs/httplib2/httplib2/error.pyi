from typing import Any

class HttpLib2Error(Exception): ...

class HttpLib2ErrorWithResponse(HttpLib2Error):
    response: Any
    content: Any
    def __init__(self, desc, response, content) -> None: ...

class RedirectMissingLocation(HttpLib2ErrorWithResponse): ...
class RedirectLimit(HttpLib2ErrorWithResponse): ...
class FailedToDecompressContent(HttpLib2ErrorWithResponse): ...
class UnimplementedDigestAuthOptionError(HttpLib2ErrorWithResponse): ...
class UnimplementedHmacDigestAuthOptionError(HttpLib2ErrorWithResponse): ...
class MalformedHeader(HttpLib2Error): ...
class RelativeURIError(HttpLib2Error): ...
class ServerNotFoundError(HttpLib2Error): ...
class ProxiesUnavailableError(HttpLib2Error): ...
