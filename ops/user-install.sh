export DJANGO_SETTINGS_MODULE=settings.production
echo "export WORKON_HOME=~/Env" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc
virtualenv --python=python2.7 --system-site-packages ~/Env/gsevol
source ~/Env/gsevol/bin/activate
pip install -r ~/gsevol-web/requirements.txt

cd ~/gsevol-web/front
npm --silent install
bower install
gulp build-production
cd ~

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
