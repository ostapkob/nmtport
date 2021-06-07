backend на  Flask, frontend на Vue  

Все вспомогательные функции вынесенны в functions.py and functions_all.py

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
###/etc/systemd/system/nmtport.service
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

### OpenSSL
Updating System Packages
It is always recommended that you update the system to the latest packages before beginning any major installations. This is done with the command below:
    sudo apt-get update && sudo apt-get upgrade
Before we begin our installation, you can check the version of OpenSSL installed on your server by issuing the command below:
    openssl version -a
Step 1: Install the necessary packages for compiling
Issue the command below to install the necessary packages for compilation:
    sudo apt install build-essential checkinstall zlib1g-dev -y
Step 2: Download OpenSSL
Next, we are going to download OpenSSL from the source (getting the latest version which at the time of writing this guide, the latest stable version is the 1.1.1 series).
    cd /usr/local/src/
    sudo wget https://www.openssl.org/source/openssl-1.1.1c.tar.gz
Next, extract the downloaded file using the command below:
    sudo tar -xf openssl-1.1.1c.tar.gz
Next, navigate to the extracted directory.
    cd openssl-1.1.1c
Step 3: Install OpenSSL
We are now going to install the latest version of OpenSSL which we downloaded using the command below:
    sudo ./config --prefix=/usr/local/ssl --openssldir=/usr/local/ssl shared zlib
    sudo make
    sudo make test
    sudo make install
Step 4: Configure OpenSSL Shared Libraries
Naviagate to the /etc/ld.so.conf.d directory and create a new configuration file 'openssl-1.1.1c.conf'.
    cd /etc/ld.so.conf.d/
    sudo nano openssl-1.1.1c.conf
Enter the following:
    /usr/local/ssl/lib
Ensure to save before you exit.
Next, reload the dynamic link by issuing the command below:
    sudo ldconfig -v
Step 5: Configure OpenSSL Binary
In our final configuration, we are going to insert the binary of our new version of OpenSSL installed (located at /usr/local/ssl/bin/openssl) to replace the default openssl binary (located at /usr/bin/openssl or /bin/openssl).
First, carry out a backup of the binary files.
    sudo mv /usr/bin/c_rehash /usr/bin/c_rehash.backup
    sudo mv /usr/bin/openssl /usr/bin/openssl.backup
Next, edit the /etc/environment file using vim.
MinProtocol = TLSv1.2
    sudo nano /etc/environment
Insert the following:
    PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/local/ssl/bin"
Ensure to save before you exit.
Next, reload the OpenSSL environment and check the PATH bin directory using commands below:
    source /etc/environment
    echo $PATH
We can now check and verify our installation of the latest stable version of OpenSSL using the command below:
    which openssl
    openssl version -a

[OpenSSL] (https://cloudwafer.com/blog/installing-openssl-on-ubuntu-16-04-18-04)
[MS SQL Driver](https://docs.microsoft.com/ru-ru/sql/connececho $PATHWe can now check and verify our installation of the latest stable version of OpenSSL using the command below: which openssl openssl version -at/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15)

