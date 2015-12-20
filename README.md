# README #
###Deploying JakSAFE webapp on Ubuntu 14.04###

**Install base libraries and virtualenv (Python Virtual Environment)**

* cd ~
* sudo apt-get update
* /# install the base libraries
* sudo apt-get -y install build-essential python-pip python-dev python-software-properties git-core
* sudo pip install virtualenv virtualenvwrapper
* nano ~/.bashrc
    * \# add to the end
    * export WORKON_HOME=$HOME/.virtualenvs
    * source /usr/local/bin/virtualenvwrapper.sh
* . .bashrc

**Install MySQL database server**

* sudo apt-get -y install mysql-server libmysqlclient-dev
    * \# follow MySQL configuration and set the root user password
* \# create the MySQL user and database for JakSAFE from MySQL CLI
* mysql -u root -p
    * create database jaksafe;
    * grant all privileges on jaksafe.* to 'jaksafe'@'localhost' identified by 'password';
    * set password for 'jaksafe'@'localhost' = PASSWORD('password');
    * flush privileges;
    * exit;

**Create a new virtualenv and pull the source code from the JakSAFE repo**

* \# create a new virtualenv called ‘jaksafe’
* mkvirtualenv jaksafe
* \# cd to the virtualenv home directory
* cdvirtualenv
* pwd
* \# default path is: ~/.virtualenvs/jaksafe/
* \# initialize a new git repo and pull the source code
* git init
* git remote add origin https://irisiko@bitbucket.org/irisiko/jaksafe.git
* git fetch
* git checkout -t origin/master

**Install the Python package requirements in the virtualenv**

* pip install -r requirements.txt
* \# wait until installation completes
* \# verify that the packages are installed
* pip list

**Sync the JakSAFE webapp database**

* cd jaksafe
* cp jaksafe/settings.py.sample jaksafe/settings.py
* nano jaksafe/settings.py
    * \# adjust the MySQL database connection settings in DATABASES
    * \# adjust the jakservice dirs (use the default)
    * \# check PYTHON_EXEC path (default is to use the ‘JakSAFE’ virtualenv Python binary)
* python manage.py migrate
* nano jaksafe/settings.py
    * \# uncomment extended_flatpages in INSTALLED_APPS
* python manage.py createsuperuser
    * \# create the admin account

**Run the JakSAFE SQL script to create the required tables**

* cdvirtualenv
* mysql -u jaksafe -p jaksafe < ./jaksafe_etc/jaksafe.sql

**Configure JakSERVICE repo**

* cdvirtualenv
* cd jaksafe/jaksafe/jakservice
* git init
* git remote add origin https://irisiko@bitbucket.org/irisiko/jakservice.git
* git fetch
* git checkout -f -t origin/master
* \# complete the JakSERVICE deployment steps before running the web server (refer to jakservice/README.md)

**Optional: install phpMyAdmin for managing the MySQL database**

* \# install phpMyAdmin set it to listen on port 8080
* sudo apt-get -y install phpmyadmin
    * \# during phpMyAdmin setup select:
        * \# apache2
        * \# Yes => enter root user password => leave blank
* sudo php5enmod mcrypt
* sudo nano /etc/apache2/ports.conf
    * \# comment: Listen 80 (example: #Listen 80)
    * \# add below Listen 80: Listen 8080
* sudo service apache2 restart
* \# open in browser http://SERVER_IP:8080/phpmyadmin

**Run the web server**

* \# run the dev web server
* python manage.py runserver 0.0.0.0:8000
* \# open in browser http://SERVER_IP:8000
* \# OR run the web server with Supervisor
* sudo ./start_supervisord.sh
* \# OR run Gunicorn web server directly
* sudo ./start_server.sh
* \# open in browser http://SERVER_IP
* \# to stop the web server (Gunicorn):
    * sudo pkill gunicorn

**Set the web server to always run on server startup**

* sudo crontab -e
    * \# add the following entry
    * @@reboot /path/to/jaksafe/virtualenv/dir/start_server.sh &

**Done!**
