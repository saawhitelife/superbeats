Provisioning a new site
=======================

## Packages required:
 * python3.6
 * nginx
 * pip, virtualenv
 * git

eg, on Ubuntu:
    sudo apt install build-essential checkinstall
    sudo apt install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
    wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tar.xz
    tar xvf Python-3.6.0.tar.xz
    cd Python-3.6.0/
    ./configure
    sudo make altinstall
    sudo apt-get install python3-venv

## Nginx configuration

 * see nginx.template.config
 * replace SITENAME with a domain name
 * note paths

## Systemd service

 * see gunicorn.systemd.service.template
 * replace SITENAME with a domain name
 * replace PASSWORDHERE with email password used for sending emails
 * note paths

## Directory structure

Assume we have a user account at /home/username
    /home/username
    └── sites
        └── SITENAME
             ├── database
             ├── source
             ├── static
             └── virtualenv

