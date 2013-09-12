#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='keysync',
      version='0.0.1',
      description='syncs OTR keys between different IM programs',
      author='The Guardian Project',
      author_email='support@guardianproject.info',
      url='https://github.com/guardianproject/otrfileconverter',
      packages=['otrapps'],
      scripts=['keysync', 'keysync-gui'],
      data_files=[('share/man/man1', ['man/keysync.1']),
                  ('share/applications', ['keysync.desktop'])],
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
     )
