#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup
import sys

dependencies = [
        'BeautifulSoup',
        'psutil',
        'python-potr',
        'pyasn1',
        'pycrypto',
        'pyparsing',
        'pyjavaproperties',
        'pgpdump',
        'qrcode',
    ]

if sys.platform == 'darwin':
     dependencies.append('PIL')
     extra_options = dict(
         setup_requires=['py2app'],
         app=['keysync-gui'],
         # Cross-platform applications generally expect sys.argv to
         # be used for opening files.
         options=dict(
             py2app=dict(
                 argv_emulation=True,
                 semi_standalone=True,
                 use_pythonpath=False,
                 iconfile='icons/keysync.icns',
                 plist={
                     'CFBundleIdentifier': 'info.guardianproject.keysync',
                     'CFBundleName': 'KeySync',
                     'CFBundleLocalizations': ['en'],
                 },
             ),
         ),
     )
elif sys.platform == 'win32':
     dependencies.append('pyinstaller')
     dependencies.append('pywin32')
     # PIL doesn't build on Windows, so use Pillow instead, pegged at
     # 2.1.0 until pyinstaller supports newer version
     dependencies.append('Pillow==2.1.0')
     extra_options = dict()
else:
     dependencies.append('PIL')
     extra_options = dict(
         # Normally unix-like platforms will use "setup.py install"
         # and install the main script as such
         scripts=['keysync-gui'],
     )

setup(name='keysync',
    version='0.1.1',
    description='syncs OTR keys between different IM programs',
    author='The Guardian Project',
    author_email='support@guardianproject.info',
    url='https://guardianproject.info/apps/keysync',
    packages=['otrapps'],
    scripts=['keysync', 'keysync-gui'],
    data_files=[
        ('share/man/man1', ['man/keysync.1']),
        ('share/icons/hicolor/128x128/apps', ['icons/128x128/keysync.png']),
        ('share/icons/hicolor/256x256/apps', ['icons/keysync.png']),
        ('share/keysync',
         ['icons/add.png', 'icons/adium.png', 'icons/chatsecure.png',
          'icons/gajim.png', 'icons/irssi.png', 'icons/jitsi.png',
          'icons/pidgin.png', 'icons/xchat.png']),
        ('share/applications', ['keysync.desktop'])
    ],
    license='GPLv3+',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    install_requires=dependencies,
    **extra_options
)
