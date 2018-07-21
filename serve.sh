#!/bin/bash

if [ ! -d "www" ]; then
  echo 'Cannot find the "www" directory.'
  echo 'Make sure you run "weaponize.py" first and only run "serve.sh" from within the same directory.'
  exit
fi

cd www

# echo "Shutting down Apache..."
# sudo service apache2 stop
# echo "Shutting down nginx..."
# sudo service nginx stop
echo "Starting python web server..."
python -m SimpleHTTPServer
# wait for user to Ctrl-C
echo "Shutting down python web server..."
echo "You will need to restart Apache."
echo "You will need to restart nginx"

cd ..
