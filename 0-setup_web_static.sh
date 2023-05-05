#!/usr/bin/env bash
# Bash script that sets up web servers for the deployment of 'web_static'

# Check if Nginx is installed
if ! [ -x "$(command nginx -v)"]; then
        sudo apt-get update
        sudo apt-get install -y nginx
fi

# start nginx
sudo service nginx start

# To create the necessary directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Fake HTML file
echo "<html>
        <head>
        </head>
        <body>
           Holberton School
        </body>
      </html>" > /data/web_static/releases/test/index.html

# creating a symbolic link on test folder
sudo rm -f /data/web_static/current
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Giving ownership of /data to ubuntu users and group
sudo chown -R ubuntu:ubuntu /data

# updating Nginx configuration
sudo sed -i '35i \ \tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}\n' /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart

exit 0
