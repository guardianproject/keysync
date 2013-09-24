#!/bin/sh

set -e

tmpdir=`mktemp -d`

echo '========================================================================'
echo "Run each python file's __main__ tests"
echo '========================================================================'
cd ../otrapps
for app in adium chatsecure gajim gpg irssi jitsi pidgin xchat util; do
    echo ''
    echo ''
    echo '------------------------------------------------------------------------'
    echo $app
    echo '------------------------------------------------------------------------'
    python ./$app.py
done

echo '========================================================================'
echo "Merge all test files into an app's format"
echo '========================================================================'
cd ..
for app in adium chatsecure gajim irssi jitsi pidgin xchat; do
    echo '------------------------------------------------------------------------'
    echo $app
    echo '------------------------------------------------------------------------'
    outdir=$tmpdir/merge-into-$app
    mkdir $outdir
    if [ $app = 'adium' ]; then
        cp tests/adium/Accounts.plist $outdir/
    elif [ $app = 'jitsi' ]; then
        cp tests/jitsi/contactlist.xml $outdir/
    fi
    ./keysync --test tests/ \
        -i adium -i irssi -i jitsi -i pidgin -i xchat \
        -o $app \
        --output-folder $outdir
done

echo $tmpdir
ls -l $tmpdir
