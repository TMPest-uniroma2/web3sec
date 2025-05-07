#!/usr/bin/env bash

# Erase dependencies cause they apparently cause troubles
rm -rf /usr/src/app/node_modules

# Re-install deps
npm install

# Finally start the app
npm start

# If it fails, keep the container going so it is possible to fix manually
tail -f /dev/null