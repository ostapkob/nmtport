#!/bin/bash
month=3
year=2022
for i in {1..31}
do
  wget --output-document=get.json http://127.0.0.1:5000/api/v2.0/get_data_period_with_fio/kran/$i.$month.$year/1
  wget --output-document=get.json http://127.0.0.1:5000/api/v2.0/get_data_period_with_fio/kran/$i.$month.$year/2
done
