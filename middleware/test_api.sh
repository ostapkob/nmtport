#!/bin/bash
for i in {1..15}
do
  wget --output-document=get.json http://127.0.0.1:5000/api/v2.0/get_data_period_with_fio/usm/$i.09.2021/1
  wget --output-document=get.json http://127.0.0.1:5000/api/v2.0/get_data_period_with_fio/usm/$i.09.2021/2
done
