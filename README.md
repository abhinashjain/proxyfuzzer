# proxyfuzzer

ProxyFuzzer is a proxy which intercept and fuzz the paramters in client request with the common web based attacks and payloads.
It's a naive attempt to automate/test for the common web based attacks.

Fuzzing and automating the attacks for the following WebGoat 8.0 challenges:
1. Bypass a Path Based Access Control Scheme (Directory Traversal)
2. Command Injection    (Command Injection)


### Usage:
```
python2 proxyfuzzer.py 8080 directorytraversal
```
```
python2 proxyfuzzer.py 8080 commandinjection
```
```
python2 proxyfuzzer.py 8080 sessionfixation
```


### Code taken from:
*[proxy2](https://github.com/inaz2/proxy2/)
*[knock](https://github.com/guelfoweb/knock)
*[python-sitemap](https://github.com/c4software/python-sitemap)
*[Crawler](https://gist.github.com/debrice/a34563fb078d9d2d15e8)
