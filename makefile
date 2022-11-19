#move it to home folder
last:
	bash ~/nmtport/bash_script/last.sh

krans:
	bash ~/nmtport/bash_script/kran.sh

usms:
	bash ~/nmtport/bash_script/usm.sh

sens:
	bash ~/nmtport/bash_script/sennebogen.sh

f:
	cat  /var/log/nginx/access.log | rg "number=$n\&" 

stat:
	sudo systemctl status nmtport.service

u:
	cat /var/log/nginx/access.log | rg 'add_usm_[\w]+\?number=$n'

test: 
	sqlcmd -S 192.168.99.106 -U ubuntu -P Port2020 -i sql/test_damage_shift_1.sql
	sleep 1
	sqlcmd -S 192.168.99.106 -U ubuntu -P Port2020 -i sql/test_damage_shift_2.sql
