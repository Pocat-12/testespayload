import PyInstaller.__main__

PyInstaller.__main__.run([
    'img.py',
    '--noconsole',
    '--onefile',
    '--add-data=hacked.png;.' # Attaches your image asset
])