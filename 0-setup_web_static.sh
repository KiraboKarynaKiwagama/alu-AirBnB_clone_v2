#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static
apt-get update -y
apt-get install -y nginx

mkdir -p /data/web_static/releases/test/ /data/web_static/shared/

cat > /data/web_static/releases/test/index.html << 'EOF'
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF

rm -f /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data/

CONF=/etc/nginx/sites-available/default
if ! grep -q 'hbnb_static' "$CONF"; then
    sed -i '0,/server_name _;/s//server_name _;\n\n\tlocation \/hbnb_static {\n\t\talias \/data\/web_static\/current\/;\n\t}/' "$CONF"
fi

service nginx restart
exit 0