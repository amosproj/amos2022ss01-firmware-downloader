#!/bin/bash

RANDOM_PW=$(tr -dc 'a-zA-Z0-9' < /dev/urandom | fold -w 10 | head -n 1)

# first install
pip install pipreqs
pipreqs path/to/project # Generate requirements.txt file
# There is now a requirements.txt file in the project folder which will have dependencies.
# to install a requirements.txt file:
pip install -r requirements.txt

echo "Packages Installed Successfully"

USER_NAME="firmware.downloader"
PASSWORD=$RANDOM_PW

echo "{username:\"${USER_NAME}\", password:\"${PASSWORD}\"}" > config/auth_config.json

echo "DB Username=$USER_NAME"
echo "DB Password=$PASSWORD"
echo "Config File Created Successfully For DB Username and Password"