from collections.abc import Iterator, Sequence
from typing import Any

from paramiko.file import BufferedFile
from paramiko.message import _LikeBytes
from paramiko.sftp_attr import SFTPAttributes
from paramiko.sftp_client import SFTPClient
from paramiko.sftp_handle import SFTPHandle

class SFTPFile(BufferedFile[Any]):
    MAX_REQUEST_SIZE: int
    sftp: SFTPClient
    handle: SFTPHandle
    pipelined: bool
    def __init__(self, sftp: SFTPClient, handle: _LikeBytes, mode: str = "r", bufsize: int = -1) -> None: ...
    def __del__(self) -> None: ...
    def close(self) -> None: ...
    def settimeout(self, timeout: float) -> None: ...
    def gettimeout(self) -> float: ...
    def setblocking(self, blocking: bool) -> None: ...
    def seekable(self) -> bool: ...
    def seek(self, offset: int, whence: int = 0) -> None: ...
    def stat(self) -> SFTPAttributes: ...
    def chmod(self, mode: int) -> None: ...
    def chown(self, uid: int, gid: int) -> None: ...
    def utime(self, times: tuple[float, float] | None) -> None: ...
    def truncate(self, size: int) -> None: ...
    def check(self, hash_algorithm: str, offset: int = 0, length: int = 0, block_size: int = 0) -> bytes: ...
    def set_pipelined(self, pipelined: bool = True) -> None: ...
    def prefetch(self, file_size: int | None = None, max_concurrent_requests: int | None = None) -> None: ...
    def readv(
        self, chunks: Sequence[tuple[int, int]], max_concurrent_prefetch_requests: int | None = None
    ) -> Iterator[bytes]: ...
