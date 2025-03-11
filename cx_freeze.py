import subprocess, shutil, sys, os

if os.path.exists('RDCW'):
    shutil.rmtree('RDCW')

if os.path.exists('RDCW.zip'):
    os.remove('RDCW.zip')

subprocess.run([sys.executable, 'cx_setup.py', 'build'])
shutil.make_archive("RDCW", 'zip', "RDCW")