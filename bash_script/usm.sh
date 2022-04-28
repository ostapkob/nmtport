# !/bin/bash
usm_id=(32711 32740 32770 32771 32772 32773 32941 32942 33287 34213 34214)
usm_name=(3 4 5 6 7 8 9 10 11 12 13)

for i in ${!usm_id[*]} 
do 
  echo ------------------ usm${usm_name[$i]} ---------------------
  grep ${usm_id[$i]} /var/log/nginx/access.log | tail -1
done

