import subprocess, shutil, sys

subprocess.run([sys.executable, 'cx_setup.py', 'build'])
shutil.make_archive("RDCW", 'zip', "RDCW")