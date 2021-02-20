#!/bin/sh
git reset --hard HEAD
git pull

pip3 install -r requirements.txt
python3 server.py