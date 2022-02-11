# !/bin/bash
kran_name=(13 12 22 8 20 33 16 14 54 47 28 18 1 35 31 37 39 23 48 72 65 10)

for i in ${!kran_name[*]} 
do 
  echo ----------------- kran${kran_name[$i]} -------------------
  grep number="${kran_name[$i]}\&" /var/log/nginx/access.log | tail -1
done
