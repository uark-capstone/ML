#!/bin/sh
git pull
pip3 install -r requirements.txt
python3 server.py