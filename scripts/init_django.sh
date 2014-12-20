#!/bin/bash

# based on the following project file structure
# http://www.slideshare.net/DZPM/12-tips-on-django-best-practices

current_dir=`pwd`
the_project=`basename ${current_dir}`

pip install -r requirements.django.txt

pcreate -s dev_starter .
pcreate -s django .

chmod 755 scripts_op/*.sh

git add .; git commit -m "init django"
