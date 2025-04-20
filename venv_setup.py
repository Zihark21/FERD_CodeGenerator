import os, sys, subprocess, shutil

if os.path.exists('.venv'):
    shutil.rmtree('.venv')

files = ['RDCW.zip']
folders = ['src/__pycache__', 'ui/__pycache__', 'RDCW']

for file in files:
    if os.path.exists(file):
        os.remove(file)

for folder in folders:
    if os.path.exists(folder):
        shutil.rmtree(folder)

subprocess.run([sys.executable, '-m', 'venv', '.venv'])
subprocess.run([os.path.join('.venv', 'Scripts', 'python'), '-m', 'pip', 'install', '--upgrade', 'pip'])
subprocess.run([os.path.join('.venv', 'Scripts', 'python'), '-m', 'pip', 'install', '--no-cache-dir', '-r', 'requirements.txt'])