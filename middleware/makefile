last:
	bash nmtport/middleware/last.sh

kran:
	bash nmtport/middleware/kran.sh

usm:
	bash nmtport/middleware/usm.sh

sen:
	bash nmtport/middleware/sennebogen.sh

f:
	cat  /var/log/nginx/access.log | rg "number=$n\&" 

stat:
	sudo systemctl status nmtport.service

test: 
	echo "-> $1 = $2"
