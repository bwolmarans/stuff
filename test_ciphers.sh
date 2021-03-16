test_ciphers.sh         test-project/           test-project-sails-old/
[centos@ip-10-0-1-234 ~]$ cat test_ciphers.sh
#!/usr/bin/env bash

# OpenSSL requires the port number.
SERVER=$1
#Read the main string
#Split the string based on the delimiter, ':'
#readarray -d : -t strarr <<< $SERVER
#tmp=$1
#read -a strarr <<< "$SERVER"

SERVERNAME=`echo $SERVER | cut -d: -f1`
#servername=$(echo $SERVER cut -d: -f1)
#servername=$(date)

#servername=${strarr[1] }
#IFS=' '
echo $SERVER
echo $SERVERNAME
echo "--------------------------------------------------------------------------------------------------------------"
DELAY=1
ciphers=$(openssl ciphers 'ALL:eNULL' | sed -e 's/:/ /g')

echo Obtaining cipher list from $(openssl version).
for cipher in ${ciphers[@]}
do
echo -n Testing $cipher...
#echo ''
#echo openssl s_client -cipher "$cipher" -connect $SERVER -servername $servername
result=$(echo -n | openssl s_client -cipher "$cipher" -connect $SERVER -servername $SERVERNAME 2>&1)
#result=$(echo -n | openssl s_client -cipher "$cipher" -connect $SERVER 2>&1)
if [[ "$result" =~ ":error:" ]] ; then
  error=$(echo -n $result | cut -d':' -f6)
  echo NO \($error\)
else
  if [[ "$result" =~ "Cipher is ${cipher}" || "$result" =~ "Cipher    :" ]] ; then
    echo YES
  else
    echo UNKNOWN RESPONSE
    echo $result
  fi
fi
sleep $DELAY
done
[centos@ip-10-0-1-234 ~]$
