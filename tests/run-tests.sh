#!/bin/sh

set -e

copy_accounts_files () {
    app=$1
    tests="$2"
    outdir="$3"
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

# allow the location of the script to be overridden
if [ -z $keysync ]; then
    keysync="./keysync"
fi


echo '========================================================================'
echo "Run each SAMENESS test"
echo '========================================================================'
cd $projectbase
for inapp in adium pidgin; do
    for outapp in adium pidgin; do
        echo ''
        echo ''
        echo '------------------------------------------------------------------------'
        echo "Run $inapp-$outapp SAMENESS tests"
        echo '------------------------------------------------------------------------'
        tests=$testbase/SAMENESS
        outdir=$tmpdir/SAMENESS-$inapp-$outapp
        copy_accounts_files $outapp $tests $outdir
        $keysync --test $tests -i $inapp -o $outapp --output-folder $outdir
        for f in $tests/$outapp/*; do
            echo '--------------------------------'
            echo $f
# remove '|| true' once these tests actually pass:
            diff -u $f $outdir/$(basename $f) || true
# nice way to see the diff:
#            meld $f  $outdir/$(basename $f)
        done
    done
done


echo '========================================================================'
echo "Run each python file's __main__ tests"
echo '========================================================================'
cd $projectbase/otrapps
for app in adium chatsecure gajim gnupg irssi jitsi pidgin xchat util; do
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
    copy_accounts_files $app $tests $outdir
    $keysync --test $tests \
        -i adium -i gnupg -i irssi -i jitsi -i pidgin -i xchat \
        -o $app \
        --output-folder $outdir
done


echo '========================================================================'
echo "Convert each app to each other app"
echo '========================================================================'
cd $projectbase
for inapp in adium chatsecure gajim gnupg irssi jitsi pidgin xchat; do
    for outapp in adium chatsecure gajim gnupg irssi jitsi pidgin xchat; do
	echo '------------------------------------------------------------------------'
	echo "Convert $inapp to $outapp "
	echo '------------------------------------------------------------------------'
	tests=$testbase
	outdir=$tmpdir/each-$inapp-to-$outapp
	mkdir $outdir
	copy_accounts_files $outapp $tests $outdir
	$keysync --test $tests --input $inapp --output $outapp --output-folder $outdir
    done
done

echo $tmpdir
ls -l $tmpdir
