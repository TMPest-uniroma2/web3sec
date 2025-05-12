#!/usr/bin/env bash

sudo apt install python3-pip python3-virtualenv
sudo apt-get install openjdk-11-jdk
sudo apt install graphviz pandoc

virtualenv "$HOME/.pyenv/pytm"
"$HOME/.pyenv/pytm/bin/python" -m pip install -r requirements.txt

. source "$HOME/.pyenv/pytm/bin/activate"

