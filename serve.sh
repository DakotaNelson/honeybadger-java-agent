#!/bin/bash

echo "Shutting down Apache."
sudo service apache2 stop
(cd output && sudo python -m SimpleHTTPServer 80 &)
echo "Now starting payload listeners. Please be patient."
msfconsole -r output/listeners.rc
