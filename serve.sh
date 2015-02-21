#!/bin/bash

echo "Shutting down Apache..."
sudo service apache2 stop
(cd output && sudo python -m SimpleHTTPServer 80 &)
serverPID="$!"
echo "Now starting payload listeners. Please be patient."
msfconsole -r output/listeners.rc

# When msfconsole shuts down we also want to kill the python server
echo "Shutting down python web server..."
kill -INT "$serverPID"
echo "You will need to restart Apache."