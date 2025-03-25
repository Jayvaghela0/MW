#!/bin/bash

# Install Chrome
wget -qO- https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb > google-chrome-stable.deb
sudo dpkg -i google-chrome-stable.deb || sudo apt-get -f install -y
rm google-chrome-stable.deb

# Install Chromedriver
wget -qO- https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip > chromedriver.zip
unzip chromedriver.zip
sudo mv chromedriver /usr/bin/
sudo chmod +x /usr/bin/chromedriver
rm chromedriver.zip
