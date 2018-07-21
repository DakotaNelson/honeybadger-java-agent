#!/bin/bash

mkdir build 2> /dev/null

set -e

javac -d ./build *.java
cd ./build
jar cvf applet.jar *
jarsigner -keystore ../verified_code_certificate_keystore.jks applet.jar signer
mv applet.jar ../www/
rm Java.class
# mv Java.class ../www/
