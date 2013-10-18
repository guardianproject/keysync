# -*- mode: python -*-
a = Analysis(['keysync-gui'],
             pathex=['c:\\Users\\abel\\Documents\\keysync'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
icon_dir = Tree('icons', prefix='icons')
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          icon_dir,
          name='KeySync.exe',
          icon='icons/keysync.ico',
          debug=False,
          strip=None,
          upx=True,
          console=False)
