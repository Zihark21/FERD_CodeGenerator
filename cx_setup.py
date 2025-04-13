from cx_Freeze import setup, Executable

build_options = {
    "build_exe": {
        "build_exe": "RDCW",
        "include_files": ["assets"],
        "optimize": 2,
        "silent": 1,
        "packages": [],
        "excludes": [],
        "zip_include_packages": ["*"],
        "zip_exclude_packages": ['customtkinter'],
        # "include_msvcr": True
    }
}

setup(
    name="RDCW",
    version="1.0",
    description="",
    options=build_options,
    executables=[Executable("RDCW.py", base="Win32GUI", icon="assets/RD_Custom.ico")],
)