#!/bin/bash
# your app must be run on 5000 port
month=6
year=2022
url=127.0.0.1:5000
TYPE='kran'
for i in {1..31}
do
  wget --output-document=get.json $url/api/v2.0/get_data_period_with_fio/$TYPE/$i.$month.$year/1
  wget --output-document=get.json $url/api/v2.0/get_data_period_with_fio/$TYPE/$i.$month.$year/2
done
