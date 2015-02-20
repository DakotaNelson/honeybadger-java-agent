#!/bin/bash

(cd output && python -m SimpleHTTPServer &)
echo "Now starting payload listeners. Please be patient."
msfconsole -r output/listeners.rc
