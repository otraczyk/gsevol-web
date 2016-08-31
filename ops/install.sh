apt-get -qq update
apt-get -y install build-essential tcl8.5 python2.7-dev python-gtk2-dev >/dev/null
# apt-get -y install git >/dev/null

# git clone https://github.com/otraczyk/gsevol-web.git
apt-get -y install python-virtualenv virtualenvwrapper > /dev/null
echo "export WORKON_HOME=~/Env" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc
virtualenv --python=python2.7 --system-site-packages ~/Env/gsevol
source ~/Env/gsevol/bin/activate
pip install -r ~/gsevol-web/requirements.txt

apt-get -y install fonts-inconsolata > /dev/null

apt-get -y install npm > /dev/null
ln -s "$(which nodejs)" /usr/bin/node
npm --silent install -g gulp bower
npm --silent install --prefix ~/gsevol-web/front/
cd ~/gsevol-web/front
bower install --allow-root

# to remove:
# npm --silent install bluebird
# gulp build-dev
# pip install amqp anyjson

gulp build-production
cd ~


wget http://download.redis.io/releases/redis-stable.tar.gz
tar xzf redis-stable.tar.gz
cd redis-stable
make
sudo make install
cd utils
./install_server.sh <<< $(echo)
# service redis_6379 start
# update-rc.d redis_6379 defaults
echo "bind 127.0.0.1" >> /etc/redis/6379.conf

cd ~/gsevol-web/urec
make
chmod +x urec/urec

cd ~/gsevol-web/fasturec
make
chmod +x fasturec/fasturec

cd ~/gsevol-web/
~/gsevol-web/manage.py migrate
~/gsevol-web/manage.py loaddata options.json
~/gsevol-web/manage.py collectstatic <<< "yes"

apt-get -y install nginx supervisor > /dev/null
pip install uwsgi
# cat ~/gsevol-web/system-requirements.txt | xargs apt-get -y  install
# cp ~/gsevol-web/ops/nginx.conf /etc/nginx/nginx.conf
cp ~/gsevol-web/ops/sv-uwsgi.conf /etc/supervisor/conf.d/uwsgi-gsevolapp.conf
cp ~/gsevol-web/ops/gsevol-web /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/gsevol-web /etc/nginx/sites-enabled/gsevol-web
rm /etc/nginx/sites-available/default
