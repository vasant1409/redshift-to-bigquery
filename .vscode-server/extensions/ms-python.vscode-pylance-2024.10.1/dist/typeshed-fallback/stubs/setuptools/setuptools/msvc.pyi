import sys
from typing import Final, TypedDict, overload, type_check_only
from typing_extensions import LiteralString, NotRequired

if sys.platform == "win32":
    import winreg as winreg
    from os import environ as environ
else:
    class winreg:
        HKEY_USERS: Final[None]
        HKEY_CURRENT_USER: Final[None]
        HKEY_LOCAL_MACHINE: Final[None]
        HKEY_CLASSES_ROOT: Final[None]

    environ: dict[str, str]

class PlatformInfo:
    current_cpu: Final[str]

    arch: str

    def __init__(self, arch: str) -> None: ...
    @property
    def target_cpu(self) -> str: ...
    def target_is_x86(self) -> bool: ...
    def current_is_x86(self) -> bool: ...
    def current_dir(self, hidex86: bool = False, x64: bool = False) -> str: ...
    def target_dir(self, hidex86: bool = False, x64: bool = False) -> str: ...
    def cross_dir(self, forcex86: bool = False) -> str: ...

class RegistryInfo:
    if sys.platform == "win32":
        HKEYS: Final[tuple[int, int, int, int]]
    else:
        HKEYS: Final[tuple[None, None, None, None]]

    pi: PlatformInfo

    def __init__(self, platform_info: PlatformInfo) -> None: ...
    @property
    def visualstudio(self) -> LiteralString: ...
    @property
    def sxs(self) -> LiteralString: ...
    @property
    def vc(self) -> LiteralString: ...
    @property
    def vs(self) -> LiteralString: ...
    @property
    def vc_for_python(self) -> LiteralString: ...
    @property
    def microsoft_sdk(self) -> LiteralString: ...
    @property
    def windows_sdk(self) -> LiteralString: ...
    @property
    def netfx_sdk(self) -> LiteralString: ...
    @property
    def windows_kits_roots(self) -> LiteralString: ...
    @overload
    def microsoft(self, key: LiteralString, x86: bool = False) -> LiteralString: ...
    @overload
    def microsoft(self, key: str, x86: bool = False) -> str: ...  # type: ignore[misc]
    def lookup(self, key: str, name: str) -> str: ...

class SystemInfo:
    WinDir: Final[str]
    ProgramFiles: Final[str]
    ProgramFilesx86: Final[str]

    ri: RegistryInfo
    pi: PlatformInfo
    known_vs_paths: dict[float, str]
    vs_ver: float
    vc_ver: float

    def __init__(self, registry_info: RegistryInfo, vc_ver: float | None = None) -> None: ...
    def find_reg_vs_vers(self) -> list[float]: ...
    def find_programdata_vs_vers(self) -> dict[float, str]: ...
    @property
    def VSInstallDir(self) -> str: ...
    @property
    def VCInstallDir(self) -> str: ...
    @property
    def WindowsSdkVersion(self) -> tuple[str, ...] | None: ...
    @property
    def WindowsSdkLastVersion(self) -> str: ...
    @property
    def WindowsSdkDir(self) -> str: ...
    @property
    def WindowsSDKExecutablePath(self) -> str | None: ...
    @property
    def FSharpInstallDir(self) -> str: ...
    @property
    def UniversalCRTSdkDir(self) -> str | None: ...
    @property
    def UniversalCRTSdkLastVersion(self) -> str: ...
    @property
    def NetFxSdkVersion(self) -> tuple[str, ...]: ...
    @property
    def NetFxSdkDir(self) -> str: ...
    @property
    def FrameworkDir32(self) -> str: ...
    @property
    def FrameworkDir64(self) -> str: ...
    @property
    def FrameworkVersion32(self) -> tuple[str, ...] | None: ...
    @property
    def FrameworkVersion64(self) -> tuple[str, ...] | None: ...

@type_check_only
class _EnvironmentDict(TypedDict):
    include: str
    lib: str
    libpath: str
    path: str
    py_vcruntime_redist: NotRequired[str | None]

class EnvironmentInfo:
    pi: PlatformInfo
    ri: RegistryInfo
    si: SystemInfo

    def __init__(self, arch: str, vc_ver: float | None = None, vc_min_ver: float = 0) -> None: ...
    @property
    def vs_ver(self) -> float: ...
    @property
    def vc_ver(self) -> float: ...
    @property
    def VSTools(self) -> list[str]: ...
    @property
    def VCIncludes(self) -> list[str]: ...
    @property
    def VCLibraries(self) -> list[str]: ...
    @property
    def VCStoreRefs(self) -> list[str]: ...
    @property
    def VCTools(self) -> list[str]: ...
    @property
    def OSLibraries(self) -> list[str]: ...
    @property
    def OSIncludes(self) -> list[str]: ...
    @property
    def OSLibpath(self) -> list[str]: ...
    @property
    def SdkTools(self) -> list[str]: ...
    @property
    def SdkSetup(self) -> list[str]: ...
    @property
    def FxTools(self) -> list[str]: ...
    @property
    def NetFxSDKLibraries(self) -> list[str]: ...
    @property
    def NetFxSDKIncludes(self) -> list[str]: ...
    @property
    def VsTDb(self) -> list[str]: ...
    @property
    def MSBuild(self) -> list[str]: ...
    @property
    def HTMLHelpWorkshop(self) -> list[str]: ...
    @property
    def UCRTLibraries(self) -> list[str]: ...
    @property
    def UCRTIncludes(self) -> list[str]: ...
    @property
    def FSharp(self) -> list[str]: ...
    @property
    def VCRuntimeRedist(self) -> str | None: ...
    def return_env(self, exists: bool = True) -> _EnvironmentDict: ...
