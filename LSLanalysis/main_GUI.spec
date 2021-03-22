# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main_GUI.py'],
             pathex=['D://PycharmProjects//RhythmsOfRelating//LSLanalysis'],
             binaries=[('D://PycharmProjects//RhythmsOfRelating//LSLanalysis//liblsl64.dll','.')],
             datas=[('D://PycharmProjects//RhythmsOfRelating//LSLanalysis//logging.conf','log'),
('D://PycharmProjects//RhythmsOfRelating//LSLanalysis//log//development.log','log'),
('D://PycharmProjects//RhythmsOfRelating//LSLanalysis//support//generate_random_samples.py','support')],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main_GUI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
