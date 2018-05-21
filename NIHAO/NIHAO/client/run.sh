#!/bin/bash
# Authro: Lantian
# Time: 2018.5.10

# start the servrer
./BBS_Pro/manage.py runserver
firefox localhost:8000

# start client
sudo ./uTalk
