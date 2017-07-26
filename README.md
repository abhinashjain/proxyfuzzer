# proxyfuzzer

ProxyFuzzer is a proxy which intercept and fuzz the paramters in client request with the common web based attacks and payloads.
It's a naive attempt to automate/test for the common web based attacks.


Usage:
python2 proxyfuzzer.py 8080 directorytraversal
python2 proxyfuzzer.py 8080 commandinjection
python2 proxyfuzzer.py 8080 sessionfixation

Fuzzing and automating the attacks for the following WebGoat 8.0 challenges:
1. Bypass a Path Based Access Control Scheme (Directory Traversal)
2. Command Injection    (Command Injection)


Code taken from:
https://github.com/inaz2/proxy2/
https://github.com/guelfoweb/knock
https://github.com/c4software/python-sitemap
https://gist.github.com/debrice/a34563fb078d9d2d15e8
