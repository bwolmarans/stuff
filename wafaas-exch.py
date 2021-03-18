run example:
  

[centos@ip-10-0-1-234 exchange]$ python wafaas-exch.py waas-student01@bugbug.me serenitynow_insanitylater
Application: dd 10423
        Server: Default (HTTP badstore-origin.cudathon.com:80)
Application: new app 10596
        Server: Default (HTTPS 1.1.1.1:443)
Application: new app 10603
        Server: Default (HTTPS 1.1.1.1:443)
Application: new app 10624
        Server: Default (HTTPS 1.1.1.1:443)
Application: new app 10625
        Server: Default (HTTPS 1.1.1.1:443)
https://api.waas.barracudanetworks.com/v2/waasapi/applications/10625/allow_deny/urls/
{ "enabled": true, "name": "bbbblock-themes-CVE-2021-26855", "deny_response": "Response Page", "response_page": "default", "action": "Process", "url_match": "/bbbowa/auth/Current/themes/resources", "follow_up_action_time": 1, "host_match": "*", "allow_deny_rule": "string", "redirect_url": "string", "extended_match": "(Method eq POST) && (Header  User-Agent rco \".*(DuckDuckBot|facebookexternalhit|Baiduspider|Bingbot|Googlebot|Konqueror|Yahoo|YandexBot|antSword).*\")", "follow_up_action": "None", "priority": 3}
{u'non_field_errors': [u'The fields allow_deny_rule, url_match, host_match, priority must make a unique set.']}
400
  
  
  
  
  
[centos@ip-10-0-1-234 exchange]$ cat wafaas-exch.py
import requests
import pprint
import sys
from getpass import getpass
try:
        from urllib.parse import urlparse
        from urllib.parse import urljoin
except ImportError:
        from urlparse import urlparse
        from urlparse import urljoin

API_BASE = "https://api.waas.barracudanetworks.com/v2/waasapi/"

proxies = {
 'http': 'http://127.0.0.1:8080',
 'https': 'http://127.0.0.1:8080',
}

def waas_api_login(email, password):
        res = requests.post(urljoin(API_BASE, 'api_login/'), data=dict(email=email, password=password), proxies=proxies)
        res.raise_for_status()
        response_json = res.json()
        return response_json['key']

def waas_api_get(token, path):
        res = requests.get(urljoin(API_BASE, path), headers={"Content-Type": "application/json", 'auth-api': token}, proxies=proxies)
        res.raise_for_status()
        return res.json()

def waas_api_post(token, path, mydata):
        #print(API_BASE)
        #print(urljoin(API_BASE, path));
        print(path)
        print(mydata)
        res = requests.post(urljoin(API_BASE, path), headers={"Content-Type": "application/json", "Accept": "application/json",'auth-api': token}, data=mydata, proxies=proxies)
        #requests.post(adr_base_url, headers=my_headers, data=global_acl )
        print(res.json())
        res.raise_for_status()
        return res.json()

if __name__ == '__main__':
        if len(sys.argv) >= 3:
                email = sys.argv[1]
                password = sys.argv[2]
        else:
                email = input("Enter user email:")
                password = getpass("Enter user password:")
        token = waas_api_login(email, password)

# Show list of applications, and servers for each application
apps = waas_api_get(token, 'applications')
for app in apps['results']:
        print("Application: {} {}".format(app['name'],app['id']))
        for server in app['servers']:
                print("\tServer: {} ({} {}:{})".format(server['name'], server['protocol'], server['host'], server['port']))

url_allow_deny = "{ \"enabled\": true, \"name\": \"bbbblock-themes-CVE-2021-26855\", \"deny_response\": \"Response Page\", \"response_page\": \"default\", \"action\": \"Process\", \"url_match\": \"/bbbowa/auth/Current/themes/resources\", \"follow_up_action_time\": 1, \"host_match\": \"*\", \"allow_deny_rule\": \"string\", \"redirect_url\": \"string\", \"extended_match\": \"(Method eq POST) && (Header  User-Agent rco \\\".*(DuckDuckBot|facebookexternalhit|Baiduspider|Bingbot|Googlebot|Konqueror|Yahoo|YandexBot|antSword).*\\\")\", \"follow_up_action\": \"None\", \"priority\": 3}"
waas_api_post(token, 'https://api.waas.barracudanetworks.com/v2/waasapi/applications/' + str(app['id']) + '/allow_deny/urls/', url_allow_deny)
[centos@ip-10-0-1-234 exchange]$
