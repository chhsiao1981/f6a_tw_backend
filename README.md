f6a_tw_backend
================

Setup
------
git submodule update --init --recursive

virtualenv __; . __/bin/activate
pip install -r requirements.django.txt

python -m f6a_tw_backend.csv_to_mongo -i development.ini -f data/dataset/36.csv

./scripts_op/run_django.sh development.txt 9002

you should be able to do

http://localhost:9002/api/query?str=<query string>&limit=<limit>


Introduction
------
這是根據

https://github.com/kiang/data.fda.gov.tw

裡的"全部藥品許可證資料集"的資料

所提供的 api.

目前有以下的 api:

* /api/query?str=<query string>&limit=<limit>
  查詢中文藥名, 英文藥名, 許可證字號, 適應症
