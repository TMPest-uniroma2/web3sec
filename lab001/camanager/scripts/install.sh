#!/usr/bin/env bash

mkdir "$HOME/.pyenv"
virtualenv "$HOME/.pyenv/camanager"
"$HOME/.pyenv/camanager/bin/python" -m pip install camanager@git+https://github.com/klezVirus/camanager

sudo ln -s "$HOME/.pyenv/camanager/bin/camanager" "/usr/local/bin/camanager"
