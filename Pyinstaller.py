import PyInstaller.__main__, shutil, os

def clean():
    for folder in ['dist', 'build']:
        if os.path.exists(folder):
            shutil.rmtree(folder)

    if os.path.exists('RDCW.spec'):
        os.remove('RDCW.spec')

    print('Cleaned.')

def get_path(relative_path):
    return os.path.join(os.getcwd(), relative_path)

ico = get_path("Assets/FE-RD.ico")
script = get_path("RDCW.py")
sources = get_path("src")
assets = get_path("Assets")

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

shutil.copy("LICENSE", "pyinstaller/dist")
shutil.copy("README.md", "pyinstaller/dist")
shutil.make_archive("RDCW", 'zip', "pyinstaller/dist")

clean()
