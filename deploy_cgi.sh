#!/bin/bash

apache=/usr/local/apache2
cgi=gallerify.cgi
#bin1=

echo "> -C check..."
perl -c $cgi
if [ $? != 0 ];
then
    echo "  $cgi failed -C check, bailing out"
    exit 1
fi

echo "> deploying.."
sudo cp -v ${cgi} ${apache}/cgi-bin/
sudo chmod -v +x ${apache}/cgi-bin/${cgi}

