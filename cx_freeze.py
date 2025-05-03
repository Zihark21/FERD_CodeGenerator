import subprocess, shutil, sys, os

rmv = ['RDCW', 'src/__pycache__', 'src/functions/__pycache__', 'ui/__pycache__', 'ui/elements/__pycache__']

for r in rmv:
    if os.path.exists(r):
        print(f'Removing {r}')
        shutil.rmtree(r)

if os.path.exists('RDCW.zip'):
    print('Removing RDCW.zip')
    os.remove('RDCW.zip')

subprocess.run([sys.executable, 'cx_setup.py', 'build'])
shutil.make_archive("RDCW", 'zip', "RDCW")