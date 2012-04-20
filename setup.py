#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='otrfileconverter',
      version='0.0.0',
      description='converts OTR keys between the different IM programs',
      author='Hans-Christoph Steiner',
      author_email='hans@eds.org',
      url='https://github.com/guardianproject/otrfileconverter',
      packages=['otrapps'],
      scripts=['otrfileconverter', 'otrfileconverter-gui'],
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
