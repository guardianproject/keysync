mkdir -p files/
cd files/

# git 
wget -c https://msysgit.googlecode.com/files/Git-1.8.4-preview20130916.exe

# python
wget -c http://www.python.org/ftp/python/2.7.5/python-2.7.5.msi
wget -c http://www.python.org/ftp/python/2.7.5/python-2.7.5.msi.asc
wget -c "https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py" 

# pywin32
wget -c "http://downloads.sourceforge.net/project/pywin32/pywin32/Build%20218/pywin32-218.win32-py2.7.exe?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fpywin32%2Ffiles%2Fpywin32%2FBuild%2520218%2F&use_mirror=iweb" -O pywin32-218.win32-py2.7.exe

# pyinstaller
wget -c https://github.com/pyinstaller/pyinstaller/tarball/develop -O pyinstaller-git.tar.gz

# mingw
wget -c "http://downloads.sourceforge.net/project/mingw/Installer/mingw-get-inst/mingw-get-inst-20120426/mingw-get-inst-20120426.exe?r=&use_mirror=superb-dca3" -O mingw-get-inst-20120426.exe

# openssl
wget -c https://slproweb.com/download/Win32OpenSSL-1_0_1e.exe

# pycrypto
wget -c "https://pypi.python.org/packages/source/p/pycrypto/pycrypto-2.6.tar.gz#md5=88dad0a270d1fe83a39e0467a66a22bb" -O pycrypto-2.6.tar.gz
wget -c "https://pypi.python.org/packages/source/p/pycrypto/pycrypto-2.6.tar.gz.asc"

# python pure otr
wget -c https://github.com/afflux/pure-python-otr/archive/1.0.0beta6.zip -O python-potr-1.0.0beta6.zip

# pidgin
wget -c "http://downloads.sourceforge.net/project/pidgin/Pidgin/2.10.7/pidgin-2.10.7-offline.exe.asc?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fpidgin%2Ffiles%2FPidgin%2F2.10.7%2F&use_mirror=superb-dca3" -O pidgin-2.10.7-offline.exe.asc
wget -c "http://downloads.sourceforge.net/project/pidgin/Pidgin/2.10.7/pidgin-2.10.7-offline.exe?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fpidgin%2Ffiles%2FPidgin%2F2.10.7%2F&use_mirror=superb-dca3" -O pidgin-2.10.7-offline.exe

# pidgin OTR
wget -c http://www.cypherpunks.ca/otr/binaries/windows/pidgin-otr-4.0.0-1.exe
wget -c http://www.cypherpunks.ca/otr/binaries/windows/pidgin-otr-4.0.0-1.exe.asc

mkdir -p gpgkeys/
gpg --homedir gpgkeys/ --import ../*asc

for sig in `find -iname "*.asc"`; do
    echo "Verifying $sig"
    gpg --homedir gpgkeys/ --verify $sig
done
