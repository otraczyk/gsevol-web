echo "export WORKON_HOME=~/Env" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc
virtualenv --python=python2.7 --system-site-packages ~/Env/gsevol
source ~/Env/gsevol/bin/activate
pip install -r ~/gsevol-web/requirements.txt

npm --silent install --prefix ~/gsevol-web/front/
cd ~/gsevol-web/front
bower install --allow-root
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
