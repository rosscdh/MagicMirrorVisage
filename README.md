# MagicMirrorVisage
Facial Recognition for MagicMirror


### cleanup
sudo apt-get purge libreoffice wolfram-engine sonic-pi scratch
sudo apt-get autoremove

### install nodejs
curl -sL https://deb.nodesource.com/setup_9.x | sudo -E bash -
sudo apt-get -y install nodejs

### start from ssh
DISPLAY=:0 nohup npm start &