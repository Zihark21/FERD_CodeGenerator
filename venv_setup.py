import os, sys, subprocess, shutil

if os.path.exists('.venv'):
    print('Removing existing venv...')
    shutil.rmtree('.venv')

files = ['RDCW.zip']
folders = ['src/__pycache__', 'ui/__pycache__', 'RDCW']

for file in files:
    if os.path.exists(file):
        print(f'Removing {file}...')
        os.remove(file)

for folder in folders:
    if os.path.exists(folder):
        print(f'Removing {folder}...')
        shutil.rmtree(folder)

subprocess.run([sys.executable, '-m', 'venv', '.venv'])
subprocess.run([os.path.join('.venv', 'Scripts', 'python'), '-m', 'pip', 'install', '--upgrade', 'pip'])
subprocess.run([os.path.join('.venv', 'Scripts', 'python'), '-m', 'pip', 'install', '--no-cache-dir', '-r', 'requirements.txt'])