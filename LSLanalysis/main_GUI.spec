# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['main_GUI.py'],
             pathex=['/Users/inspireadmin/Downloads/RhythmsOfRelating/LSLanalysis'],
             binaries=[('/Users/inspireadmin/miniconda3/lib/python3.7/site-packages/pylsl/liblsl64.dylib','.')],  
             datas=[('/Users/inspireadmin/Downloads/RhythmsOfRelating/LSLanalysis/logging.conf','log'),
('/Users/inspireadmin/Downloads/RhythmsOfRelating/LSLanalysis/log/development.log','log')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=False,
          name='main_GUI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main_GUI')
app = BUNDLE(exe,
         name='myscript.app',
         icon=None,
         bundle_identifier=None)
