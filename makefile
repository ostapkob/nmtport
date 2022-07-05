#move it to home folder
last:
	bash ~/nmtport/bash_script/last.sh

kran:
	bash ~/nmtport/bash_script/kran.sh

usm:
	bash ~/nmtport/bash_script/usm.sh

sen:
	bash ~/nmtport/bash_script/sennebogen.sh

f:
	cat  /var/log/nginx/access.log | rg "number=$n\&" 

stat:
	sudo systemctl status nmtport.service

u:
	cat /var/log/nginx/access.log |  rg 'add_usm_[\w]+\?number=$n'


test: 
	echo "-> $1 = $2"
