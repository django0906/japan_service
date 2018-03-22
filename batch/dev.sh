#!/bin/sh

sudo killall -9 uwsgi
sudo service nginx stop
sudo rm -rf /tmp/japan_user/
sudo chmod -R 777 /tmp/japan_user/
sudo rm -rf /tmp/japan_admin/
sudo chmod -R 777 /tmp/japan_admin/
/home/vagrant/project/venv/bin/python /home/vagrant/project/japan_service/manage.py runserver 0.0.0.0:8000

##Test
