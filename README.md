backend на  Flask, frontend на Vue  

Все вспомогательные функции вынесенны в functions.py  

Логика: Arduino -> Api [GET] -> Python -> DB -> Api [GET] -> Axios -> Vue  
+ wsgi.py точка входа  
+ bot.py бот для телеграм  
+ add_mechanism.py добавляет механизмы в БД  
+ post_get.py искуственно набивает БД  

psw.py не комичу там переменные с паролями:

### Настрой дату и время: 
время DB записывается в формате Coordinated Universal Time 

    apt install tzdata 
    sudo dpkg-reconfigure tzdata

Создай виртуальное окружение

    python3 -m venv venv

* * *
### Настройки Nginix

	#/etc/nginx/sites-enabled/nmtport 
	server {
	    listen 80;
	    listen [::]:80;
	    server_name 94.154.76.136;
	    include mime.types;
    location / {
            include proxy_params;
            proxy_pass http://unix:/home/UBUNTU/nmtport/nmtport.sock;
        }
    }

	#/etc/systemd/system/nmtport.service
    [Unit]
    Description=Gunicorn instance to serve nmtport
    After=network.target
    [Service]
    User=USER
    Group=www-data
    WorkingDirectory=/home/USER/nmtport
    Environment="PATH=/home/USER/nmtport/venv/bin"
    ExecStart=/home/USER/nmtport/venv/bin/gunicorn --workers 3 --bind unix:nmtport.sock -m 007 wsgi:app
    [Install]
    WantedBy=multi-user.target


	#nmtport.ini
    [uwsgi]
    module = wsgi:app
    master = true
    processes = 5
    socket = nmtport.sock
    chmod-socket = 660
    vacuum = true
    die-on-term = true
* * *

    sudo systemctl restart nmtport
    sudo systemctl restart nginx

    pip install gunicorn
    sudo apt-get install unixodbc-dev
    pip install pyodbc


### Brandmauer
    sudo apt-get install -y ufw
    sudo ufw allow ssh
    sudo ufw allow http
    sudo ufw allow 443/tcp
    sudo ufw --force enable
    sudo ufw status


[MS SQL Driver](https://docs.microsoft.com/ru-ru/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15)