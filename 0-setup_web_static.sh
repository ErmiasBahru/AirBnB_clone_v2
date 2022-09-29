#!/usr/bin/env bash
# installs nginx and configure it to task needs

apt-get -y update
apt-get -y install nginx
mkdir -p /data/web_static/releases/test/ /data/web_static/shared/
echo "This is for testing" | sudo tee /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -hR ubuntu:ubuntu /data/
new_loc="\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n"
sed -i "38i\ $new_loc" /etc/nginx/sites-available/default

sudo /etc/init.d/nginx restart
