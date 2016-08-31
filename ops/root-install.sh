apt-get -qq update
/home/gsevolapp/gsevol-web/system-requirements.txt | xargs apt-get -y  install > /dev/null
npm --silent install -g gulp bower

cd /home/gsevolapp
wget http://download.redis.io/releases/redis-stable.tar.gz
tar xzf redis-stable.tar.gz
cd redis-stable
make
make install
cd utils
./install_server.sh <<< $(echo)
# service redis_6379 start
# update-rc.d redis_6379 defaults
echo "bind 127.0.0.1" >> /etc/redis/6379.conf

apt-get -y install nginx supervisor > /dev/null
cp /home/gsevolapp/gsevol-web/ops/nginx/nginx.conf /etc/nginx/nginx.conf
cp /home/gsevolapp/gsevol-web/ops/supervisor/uwsgi-gsevolapp.conf /etc/supervisor/conf.d/
cp /home/gsevolapp/gsevol-web/ops/sv-celery.conf /etc/supervisor/conf.d/
cp /home/gsevolapp/gsevol-web/ops/gsevol-web /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/gsevol-web /etc/nginx/sites-enabled/gsevol-web
rm /etc/nginx/sites-available/default
