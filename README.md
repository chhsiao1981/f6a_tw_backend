f6a_tw_backend
================

Setup
------
virtualenv __; . __/bin/activate
pip install -r requirements.django.txt

./scripts_op/run_django.sh development.txt 9002

you should be able to see

http://localhost:9002/api/default


Introduction
-----
This template intends to efficiently develop with the following libraries:

* pcreate (scaffolding, from pylons pyramid)
* type / str / unicode
* timestamp (by millisecond) / sec_timestamp / datetime / arrow
* sniffer / nosetests (autotest)
* pymongo (db)
* grequests (http post/get)
* ujson (json)
* argparse
* pandas
* lock
* send email
* oauth2
* django
* django-rest-framework

All are welcome to improve this template


Django
-----
1. settings is set in [{{package}}:django] in .ini (with key lowercased)


python-social-auth
-----
1. For now, social-auth is for authentication only.
2. need to change data-clientid to the corresponding clientid in /static/login.html
3. need to change social\_auth\_google\_plus\_key and social\_auth\_google\_plus\_secret in .ini
4. The token on client-side should be revoked immediately once the ajax to login complete (success or error).
5. Once the ajax to login successfully complete, the response return \{id, username, first\_name, last\_time, url\}
6. tested /auth/complete/google-plus (/static/login.html)
