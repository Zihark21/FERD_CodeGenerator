import os, sys, subprocess, shutil

if os.path.exists('.venv'):
    shutil.rmtree('.venv')

subprocess.run([sys.executable, '-m', 'venv', '.venv'])
subprocess.run([os.path.join('.venv', 'Scripts', 'python'), '-m', 'pip', 'install', '--upgrade', 'pip'])
subprocess.run([os.path.join('.venv', 'Scripts', 'python'), '-m', 'pip', 'install', '--no-cache-dir', '-r', 'requirements.txt'])