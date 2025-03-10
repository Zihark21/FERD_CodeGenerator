import PyInstaller.__main__
import os, zipfile

def get_path(relative_path):
    return os.path.join(os.getcwd(), relative_path)

ico = get_path(r"Assets\FE-RD.ico")
script = get_path(r"FE-RD-CC.py")
sources = get_path(r"Sources")
assets = get_path(r"Assets")

options = [
    '--clean',
    '--noconfirm',
    '--optimize=2',
    '--onefile',
    '--noconsole',
    '--workpath=pyinstaller/build',
    '--distpath=pyinstaller/dist',
    '--specpath=pyinstaller/spec',
    '--log-level=WARN',
    f'--ico={ico}',
    f'--add-data={sources};Sources',
    f'--add-data={assets};Assets',
    script
]

PyInstaller.__main__.run(options)

with zipfile.ZipFile("FE-RD-CC.zip", 'w') as zipf:
    zipf.write('pyinstaller/dist/FE-RD-CC.exe', os.path.basename('FE-RD-CC.exe'))
    zipf.write('LICENSE', os.path.basename('LICENSE'))
    zipf.write('README.md', os.path.basename('README.md'))