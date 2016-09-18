#!/usr/bin/env python
import os
import re
import commands
import sys
def start():
        oldUsername = sys.argv[1]
        oldPassword = sys.argv[2]
        userName = commands.getoutput('python ./CalcRealUsername.py '+oldUsername)

        wanConfig = '''config 'interface' 'wan'
    option 'ifname' 'eth1'
    option 'proto' 'pppoe'
    option 'username' '{}'
    option 'password' '{}'
    option 'peerdns' '1'
    option 'defaultroute' '1'

config'''.format(userName, oldPassword)

        output = os.popen('cat ~/network').read()
        result, number = re.subn(r'(config interface \'wan\'[a-zA-Z0-9\t\' \n]+)config', wanConfig, output)
        os.popen('echo "'+result+'">/etc/config/network')
        os.popen('/etc/init.d/network restart')
if __name__ == '__main__':
        if len(sys.argv) != 3:
                print 'Please run this command with 2 params. (username and password)'
                exit(1)
        else:
                start()