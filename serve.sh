#!/bin/bash

if [ ! -d "output" ]; then
  echo 'Cannot find the "output" directory.'
  echo 'Make sure you run "weaponize.py" first and only run "serve.sh" from within the same directory.'
  exit
fi

cd output

echo "Shutting down Apache..."
sudo service apache2 stop
sudo python -m SimpleHTTPServer 80 & 2>&1 >> http.log
serverPID="$!"
echo "Now starting payload listeners. Please be patient."
msfconsole -r listeners.rc

# When msfconsole shuts down we also want to kill the python server
echo "Shutting down python web server..."
sudo kill "$serverPID"
echo "You will need to restart Apache."

cd ..