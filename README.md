Стандартный backend на  Flask, frontend на Vue 

Все вспомогательные функции вынесенны в functions.py

Логика: Arduino -> Api [GET] -> Python -> DB -> Api [GET] -> Axios -> Vue  
wsgi.py точка входа
bot.py бот для телеграм
add_mechanism.py добавляет механизмы в БД
post_get.py искуственно набивает БД

psw.py не комичу там три переменных:
    post_pass
    form_pass
    api_key

Настрой дату и время: 
время DB записывается в формате Coordinated Universal Time 
apt install tzdata 
sudo dpkg-reconfigure tzdata

Настройки Nginix
#/etc/nginx/sites-enabled/nmtport
server {
    listen 80;
    server_name 18.139.162.128;
    include mime.types;

    location / {
            include proxy_params;
            proxy_pass http://unix:/home/ubuntu/nmtport/nmtport.sock;
        }
}

#/etc/nginx/sites-enabled/nmtport.service
[Unit]
Description=Gunicorn instance to serve nmtport
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/nmtport
Environment="PATH=/home/ubuntu/nmtport/venv/bin"
ExecStart=/home/ubuntu/nmtport/venv/bin/gunicorn --workers 3 --bind unix:nmtport.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target



#/etc/nginx/sites-enabled/nmtport.ini
[uwsgi]
module = wsgi:app
master = true
processes = 5
socket = nmtport.sock
chmod-socket = 660
vacuum = true
die-on-term = true
sudo systemctl restart nmtport
sudo systemctl restart nginx


