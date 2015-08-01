apt-get -y update
apt-get -y install openssh-server python-setuptools python-dev build-essential git nginx

sed -i "s/#PasswordAuthentication yes/PasswordAuthentication no/" /etc/ssh/sshd_config
sed -i "s/UsePAM yes/UsePAM no/" /etc/ssh/sshd_config

adduser --system --disabled-password --gecos "" oldfashion

echo "oldfashion ALL=(ALL) NOPASSWD:/etc/init.d/nginx reload, /usr/sbin/nginx -t" > /etc/sudoers.d/oldfashion-nginx
chmod 0440 /etc/sudoers.d/oldfashion-nginx

cat<<EOF > /etc/nginx/conf.d/oldfashion.conf
include /home/oldfashion/*.conf;
EOF

service nginx start

mkdir -p /home/oldfashion/.ssh

touch /home/oldfashion/.ssh/authorized_keys

chown -R oldfashion:nogroup /home/oldfashion/

sed -i s#/home/oldfashion:/bin/false#/home/oldfashion:/bin/bash# /etc/passwd

wget -qO- https://get.docker.com/ | sh

usermod -aG docker oldfashion