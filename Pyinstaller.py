import PyInstaller.__main__

path = r"C:\Users\aadai\Documents\GitHub\FERD_CodeGenerator"

ico = path + r"\FE-RD.ico"
script = path + r"\FE-RD-CC.py"

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
        f'--add-data={ico};.',
        script
    ]

PyInstaller.__main__.run(options)