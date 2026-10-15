import subprocess
import shutil
import sys
from pathlib import Path

rmv = ['RDCW', 'src/__pycache__', 'src/functions/__pycache__', 'ui/__pycache__', 'ui/elements/__pycache__']

for r in rmv:
    rpath = Path.cwd() / r
    if rpath.exists():
        print(f'Removing {r}')
        shutil.rmtree(rpath)

if Path.cwd().joinpath('RDCW.zip').exists():
    print('Removing RDCW.zip')
    Path.cwd().joinpath('RDCW.zip').unlink()

subprocess.run(['.venv/Scripts/python.exe', 'cx_setup.py', 'build'])
shutil.make_archive("RDCW", 'zip', "RDCW")