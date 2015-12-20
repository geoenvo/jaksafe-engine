# README #
###Deploying JakSERVICE on Ubuntu 14.04###

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


**Install QGIS and other library requirements**

* \# install the newer QGIS version from QGIS repo
* cd ~
* sudo nano /etc/apt/sources.list
    * \# add to the end
    * deb http://qgis.org/debian trusty main
    * deb-src http://qgis.org/debian trusty main
* gpg --keyserver keyserver.ubuntu.com --recv DD45F6C3
* gpg --export --armor DD45F6C3 | sudo apt-key add -
* sudo apt-get update
* sudo apt-get -y install qgis python-qgis
* \# install locale library requirements for pdf report generation
* sudo apt-get -y install language-pack-id
* \# install Matplotlib library requirements
* sudo apt-get -y install libpng-dev libfreetype6-dev libxft-dev
* \# activate ‘jaksafe’ virtualenv
* workon jaksafe
* add2virtualenv "/usr/lib/python2.7/dist-packages/"
* cdvirtualenv
* cd jaksafe/jaksafe/jakservice

**Configure JakSERVICE repo (skip if already completed)**

* git init
* git remote add origin https://irisiko@bitbucket.org/irisiko/jakservice.git
* git fetch
* git checkout -f -t origin/master

**install JakSERVICE Python package requirements in virtualenv**

* pip install -r requirements.txt
* \# wait until installation completes
* \# verify that the packages are installed
* pip list

**Edit JakSERVICE configuration file**

* cp global_conf.cfg.sample global_conf.cfg
* nano global_conf.cfg
    * \# set [database configuration]: url_address, user, passwd, database_name, port
    * \# set [dims_conf]: url_dims
    * \# set [folder_conf]:
        * project_folder = /set/absolute/path/to/jakservice/dir (example: /home/user/.virtualenvs/jaksafe/jaksafe/jaksafe/jakservice)
        * auto_folder = relative path from jakservice dir (use default: ../uploaded/jakservice/auto)
        * adhoc_folder = relative path from jakservice dir (use default: ../uploaded/jakservice/adhoc)
    * \# set [directory]:
        * \# set absolute path for all, default settings below is provided for example:
        * resource = /home/user/.virtualenvs/jaksafe/jaksafe/jaksafe/uploaded/jakservice/auto/resource/
        * assumptions = /home/user/.virtualenvs/jaksafe/jaksafe/jaksafe/uploaded/jakservice/auto/input/assumptions/
        * aggregate = /home/user/.virtualenvs/jaksafe/jaksafe/jaksafe/uploaded/jakservice/auto/input/aggregat/
        * log = /home/user/.virtualenvs/jaksafe/jaksafe/jaksafe/uploaded/jakservice/auto/output/log/
        * impact = /home/user/.virtualenvs/jaksafe/jaksafe/jaksafe/uploaded/jakservice/auto/output/impact/
        * report = /home/user/.virtualenvs/jaksafe/jaksafe/jaksafe/uploaded/jakservice/auto/output/report/
        * hazard = /home/user/.virtualenvs/jaksafe/jaksafe/jaksafe/uploaded/jakservice/auto/output/hazard/
        * log_adhoc = /home/user/.virtualenvs/jaksafe/jaksafe/jaksafe/uploaded/jakservice/adhoc/output/log/
        * impact_adhoc = /home/user/.virtualenvs/jaksafe/jaksafe/jaksafe/uploaded/jakservice/adhoc/output/impact/
        * report_adhoc = /home/user/.virtualenvs/jaksafe/jaksafe/jaksafe/uploaded/jakservice/adhoc/output/report/
        * hazard_adhoc = /home/user/.virtualenvs/jaksafe/jaksafe/jaksafe/uploaded/jakservice/adhoc/output/hazard/

**Copy JakSERVICE input files to JakSAFE webapp uploaded directory**

* cp -R auto adhoc ../uploaded/jakservice/

**Run the script to populate fl_event table with past flood reports from DIMS flr API**

* python populate_dims.py

**Create cron jobs for automatic DALA calculation every 6 hours**

* sudo crontab -e
    * \# add the following entries
    * 59 5 * * * /home/user/.virtualenvs/jaksafe/bin/python /home/user/.virtualenvs/jaksafe/jaksafe/jaksafe/jakservice/run_dalla_auto.py > /dev/null 2>&1
    * 59 11 * * * /home/user/.virtualenvs/jaksafe/bin/python /home/user/.virtualenvs/jaksafe/jaksafe/jaksafe/jakservice/run_dalla_auto.py > /dev/null 2>&1
    * 59 17 * * * /home/user/.virtualenvs/jaksafe/bin/python /home/user/.virtualenvs/jaksafe/jaksafe/jaksafe/jakservice/run_dalla_auto.py > /dev/null 2>&1
    * 59 23 * * * /home/user/.virtualenvs/jaksafe/bin/python /home/user/.virtualenvs/jaksafe/jaksafe/jaksafe/jakservice/run_dalla_auto.py > /dev/null 2>&1

**Done!**