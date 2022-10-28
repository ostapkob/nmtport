# !/bin/bash
kran_name=(26 13 12 22 8 20 33 11 25 16 14 54 47 82 28 18 1 35 31 17 39 23 48 72 65 10)

for i in ${!kran_name[*]} 
do 
  echo ----------------- kran${kran_name[$i]} -------------------
  grep add_kran\?number="${kran_name[$i]}" /var/log/nginx/access.log | tail -1
done
