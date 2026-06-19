import PyInstaller.__main__

PyInstaller.__main__.run([
    'payload2.py',
    '--noconsole',
    '--onefile',
    '--add-data=hacked.png;.' # Attaches your image asset
])