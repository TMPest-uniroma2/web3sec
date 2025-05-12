#!/usr/bin/env bash

mkdir "$HOME/.pyenv"
virtualenv "$HOME/.pyenv/simba"
"$HOME/.pyenv/simba/bin/python" -m pip install -r requirements.txt

. source "$HOME/.pyenv/simba/bin/activate"