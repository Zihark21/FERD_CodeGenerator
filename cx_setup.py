from cx_Freeze import setup, Executable

build_options = {
    "build_exe": {
        "build_exe": 'RDCW',
        "include_files": ['Assets'],
        "optimize": 2,
        'silent': 1
    }
}

setup(
    name="RDCW",
    version="1.0",
    description="",
    options=build_options,
    executables=[Executable("RDCW.py", base="Win32GUI", icon='Assets/FE-RD.ico')],
)