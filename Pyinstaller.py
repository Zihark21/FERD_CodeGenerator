import PyInstaller.__main__, os

path = os.getcwd()

ico = path + r"\Assets\FE-RD.ico"
script = path + r"\FE-RD-CC.py"
assets = path + r"\Assets"

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
        f'--add-data={ico};Assets',
        f'--add-data={assets};Assets',
        script
    ]

PyInstaller.__main__.run(options)