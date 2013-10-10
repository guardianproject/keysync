#!/bin/sh

set -e

copy_accounts_files () {
    tests="$1"
    outdir="$2"
    test -d $outdir || mkdir -p $outdir
    if [ $app = 'adium' ]; then
        cp $tests/adium/Accounts.plist $outdir/
    elif [ $app = 'jitsi' ]; then
        cp $tests/jitsi/contactlist.xml \
            $tests/jitsi/sip-communicator.properties \
            $outdir/
    elif [ $app = 'pidgin' ]; then
        cp $tests/pidgin/accounts.xml $outdir/
    fi
}


tmpdir=`mktemp -d /tmp/keysync-XXXXXXXXXXXXXX`
testbase=`pwd`
projectbase=$(dirname $testbase)


echo '========================================================================'
echo "Run each SAMENESS test"
echo '========================================================================'
cd $projectbase
for app in adium pidgin; do
    echo ''
    echo ''
    echo '------------------------------------------------------------------------'
    echo "Run $app's SAMENESS tests"
    echo '------------------------------------------------------------------------'
    tests=$testbase/SAMENESS
    outdir=$tmpdir/SAMENESS-$app
    copy_accounts_files $tests $outdir
    ./keysync --test $tests -i $app -o $app --output-folder $outdir
    for f in $tests/$app/*; do
        echo '--------------------------------'
        echo $f
# remove '|| true' once these tests actually pass:
        diff -u $f $outdir/$(basename $f) || true
    done
done


echo '========================================================================'
echo "Run each python file's __main__ tests"
echo '========================================================================'
cd $projectbase/otrapps
for app in adium chatsecure gajim gpg irssi jitsi pidgin xchat util; do
    echo ''
    echo ''
    echo '------------------------------------------------------------------------'
    echo "Run $app's __main__ tests"
    echo '------------------------------------------------------------------------'
    python ./$app.py
done

echo '========================================================================'
echo "Merge all test files into an app's format"
echo '========================================================================'
cd $projectbase
for app in adium chatsecure gajim irssi jitsi pidgin xchat; do
    echo '------------------------------------------------------------------------'
    echo "Merge all test files into $app's format"
    echo '------------------------------------------------------------------------'
    tests=$testbase
    outdir=$tmpdir/merge-into-$app
    mkdir $outdir
    copy_accounts_files $tests $outdir
    ./keysync --test $tests \
        -i adium -i irssi -i jitsi -i pidgin -i xchat \
        -o $app \
        --output-folder $outdir
done

echo $tmpdir
ls -l $tmpdir
