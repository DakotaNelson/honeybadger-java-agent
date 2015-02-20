#!/bin/bash

(cd output && python -m SimpleHTTPServer &)
msfconsole -r output/listeners.rc
