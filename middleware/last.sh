# !/bin/bash
kran_id=(15125 13893 5908 14195 4934 15511 15510 15512 30271 4513)
kran_name=(13 12 22 8 20 33 16 14 54 47 28 18 1 35 31 37 39 23 48 72 65 10)
usm_id=(32711 32740 33287 34213 34214)
usm_name=(3 4 11 12 13)

for i in ${!kran_name[*]} 
do 
  echo ------------------kran${kran_name[$i]}-------------------
  grep number="${kran_name[$i]}\&" /var/log/nginx/access.log | tail -1
done
echo =====================================
for i in ${!usm_id[*]} 
do 
  echo ------------------usm${usm_name[$i]}---------------------
  grep ${usm_id[$i]} /var/log/nginx/access.log | tail -1
done
# for i in 32711 32740 33287 34213 34214
# do 
#   echo -----------------------------------
#   grep $i /var/log/nginx/access.log | tail -1
# done

