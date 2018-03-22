#!/bin/sh

echo "server start" >> server.log
date '+%Y-%m-%d %H:%M:%S' -d 'today' >> server.log

/home/vagrant/project/venv/bin/python /home/vagrant/project/japan_service/manage.py collectstatic --clear
sudo killall -9 uwsgi
sudo /usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data --daemonize /var/log/uwsgi-emperor.log
sudo rm -rf /tmp/japan_user/
sudo chmod -R 777 /tmp/japan_user/
sudo rm -rf /tmp/japan_admin/
sudo chmod -R 777 /tmp/japan_admin/
sudo service nginx restart

echo "server end" >> server.log
date '+%Y-%m-%d %H:%M:%S' -d 'today' >> server.log

echo "--------------------------------" >> server.log
