# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main_GUI.py'],
             pathex=['D://PycharmProjects//HybridHarmony//src'],
             binaries=[('D://PycharmProjects//RhythmsOfRelating//LSLanalysis//liblsl64.dll','.')],
             datas=[('D://PycharmProjects//HybridHarmony//src//logging.conf','log'),
('D://PycharmProjects////HybridHarmony//src//log//development.log','log'),
('D://PycharmProjects////HybridHarmony//src//support//samplegeneration.py','support'),
('D://PycharmProjects////HybridHarmony//src//support//session_2020_02_21_14_21_11_anticipation.xdf','support'),
('D://PycharmProjects////HybridHarmony//src//support//xdf.py','support'),
('D://PycharmProjects////HybridHarmony//src//support//__init__.py','support')],
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
          name='HybridHarmonyv1.1',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
