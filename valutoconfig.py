import os
import uuid
import platform

# FIRST RUN, A BIT CLUMPSY, SHOULD BE REWRITTEN BUT WORKS FOR NOW
FIRSTRUN = False
if platform.system() == "Linux":
    CONFPATH = os.path.expanduser('~/.valuto/valuto.conf')
elif platform.system() == "Windows":
    CONFPATH = os.path.expanduser('~\\AppData\\Roaming\\Valuto\\valuto.conf')   
    WINDOWS_DETECTED = True
    print "Windows detected: file:" + CONFPATH

#Damn it's getting ugly
if not os.path.isfile(CONFPATH):
    if WINDOWS_DETECTED:
        os.makedirs(os.path.expanduser('~\\AppData\\Roaming\\Valuto\\'))
    print "Conf not found.. First run detected"
    FIRSTRUN = True
    f = open(CONFPATH, 'a')
    f.write('rpcuser=valutorpc\n')
    f.write('rpcpassword=' + uuid.uuid4().hex)
    
# READ PASS/USER FROM VALUTO.CONF
f = open(CONFPATH, 'r')
flines = f.readlines()
RPCUSER = flines[0].replace('rpcuser=','').rstrip()
RPCPASSWORD = flines[1].replace('rpcpassword=','').rstrip()
           
## DO NOT CHANGE THIS IF YOU ARE NOT ADVANCED USER
## Set serverurl where valutod is listening
## Eg. http://<username>:<password>@<ip>:<port>
SERVER_URL = 'http://'+ RPCUSER +':'+ RPCPASSWORD +'@127.0.0.1:40332'
ACCOUNT_NAME = 'ValutoKivy'

