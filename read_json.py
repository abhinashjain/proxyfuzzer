#knockpy -j olamoney.com
# python read_json.py olamoney.com.json > subdomains.txt
import sys
import json

(domain,tld,ext)=map(str,sys.argv[1].split('.'))
domainname=domain+'.'+tld
with open(sys.argv[1]) as data_file:
    data = json.load(data_file)

arr=data["found"]["subdomain"]
for name in arr:
    if name.endswith(domainname):
        print "https://"+str(name)
