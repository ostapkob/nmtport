# !/bin/bash
numbers=(1 2 3 4 5 6 7 8 9)

for i in ${!numbers[*]} 
do 
  echo ----------------- sennebogen${numbers[$i]} -------------------
  grep add_sennebogen\?number="${numbers[$i]}" /var/log/nginx/access.log | tail -1
done
