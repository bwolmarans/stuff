[centos@ip-10-0-1-234 ~]$ cat bwaf_login.sh
curl $1/restapi/v3.1/login -X POST -H Content-Type:application/json -d '{"username":"'$2'", "password":"'$3'"}' > blah.txt

sed 's/"/ /g' < blah.txt | awk '{print "-u \"" $4 ":\"" }' > token.txt

echo "Your Token Is: "

cat token.txt

echo "Example of using this token to get the services on the waf: curl -K token.txt <waf url>/restapi/v3.1/services"

[centos@ip-10-0-1-234 ~]$
