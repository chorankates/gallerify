#!/bin/bash

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
# copy the wrapper into apache
sudo cp -v ${cgi} /usr/local/apache2/cgi-bin/
sudo chmod -v +x /usr/local/apache2/cgi-bin/${cgi}

