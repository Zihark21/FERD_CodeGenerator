import PyInstaller.__main__, shutil, os

options = [
    '--clean',
    '--noconfirm',
    '--optimize=2',
    '--onefile',
    '--noconsole',
    '--log-level=WARN',
    f'--ico=Assets/FE-RD.ico',
    f'--add-data=src;src',
    f'--add-data=Assets;Assets',
    'RDCW.py'
]

PyInstaller.__main__.run(options)

shutil.copy("LICENSE", "dist")
shutil.copy("README.md", "dist")
shutil.make_archive("RDCW", 'zip', "dist")

for folder in ['dist', 'build']:
    if os.path.exists(folder):
        shutil.rmtree(folder)

if os.path.exists('RDCW.spec'):
    os.remove('RDCW.spec')