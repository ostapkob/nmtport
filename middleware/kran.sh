# !/bin/bash
kran_name=(13 12 22 8 20 33 16 14 54 47 82)

for i in ${!kran_name[*]} 
do 
  echo ----------------- kran${kran_name[$i]} -------------------
  grep number=${kran_name[$i]} /var/log/nginx/access.log | tail -1
done