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
    'FE-RD-CC.py'
]

PyInstaller.__main__.run(options)

shutil.copy("LICENSE", "dist")
shutil.copy("README.md", "dist")
shutil.make_archive("Radiant Dawn Code Wizard", 'zip', "dist")

for folder in ['dist', 'build']:
    if os.path.exists(folder):
        shutil.rmtree(folder)

if os.path.exists('FE-RD-CC.spec'):
    os.remove('FE-RD-CC.spec')