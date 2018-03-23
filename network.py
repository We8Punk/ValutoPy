import platform
import os
import time
import json
import subprocess
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivymd.snackbar import Snackbar
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
import valutoconfig as Config
import signal
import sys

class NetworkManager(Widget):

    blockcount = StringProperty()
    balance = StringProperty()
    connections = StringProperty()
    txfee = StringProperty()
    networkdiff = StringProperty()
    myaddress = StringProperty()
    unconfirmedbalance = StringProperty()
    connectioncolor = StringProperty()
    loadingstate = BooleanProperty() 
    terminalbuffer = StringProperty()
    
    def __init__(self, **kwargs):
        super(NetworkManager,self).__init__(**kwargs) 
        self.loadingstate = True
        self.lasttransaction = ''
        self.connectioncolor = '#FF0000'
        self.RPC_server = None
        self.connect_rpc()
        self.terminalbuffer = ''
        self.lastterminalcommand = ''
        ### Start polling 
        Clock.schedule_interval(self.poll_info, 15)
        
    def send(self, address, amount, **kwargs):
        print 'sending ' + amount + ' to ' + address
        self.RPC_server.sendfrom(Config.ACCOUNT_NAME, address, float(amount), 6)
    
    def onchangeterminal(self, input, **kwargs):
        if input == '':
            input = ' '
        inputchar = input[-1]
        
        if inputchar == chr(10):
            inputcommand = input.split(chr(10))
            self.lastterminalcommand = inputcommand[-2]
            print 'valutod.exe ' + self.lastterminalcommand
            output = self.commandsend_terminal('valutod ' + self.lastterminalcommand)
            print output
            self.terminalbuffer += output
            #except:
            #    self.terminalbuffer += chr(10) + 'Error!' + chr(10)
    
    def commandsend_terminal(self, input, **kwargs):
        try:
            output = subprocess.check_output(input, shell=True)
        except:
            output = ''
        return output   
        
    def kill_valutod(self, **kwargs):
        print 'Killing Valutod'
        try:
            os.kill(self.valutod.pid, signal.SIGTERM)
        except:
            pass
            
        subprocess.call('valutod.exe stop', shell=True)
        
    def start_valutod(self, **kwargs):

        print 'Starting Valutod....'
        
        if platform.system() == "Linux":
            self.valutod = subprocess.Popen('./valutod')    
        else:
            self.valutod = subprocess.Popen('valutod', shell=True)            
            
            while True:
                checkifrunning = subprocess.call('valutod getinfo', shell=True)
                if checkifrunning == 0:
                    print 'Valutod started'
                    break
                else:
                    print 'Starting Valutod'			
				
            print 'valutod started with pid:' + str(self.valutod.pid)
        
        
    def connect_rpc(self, **kwargs):
        self.start_valutod()
        print 'Connecting to: ', Config.SERVER_URL
        while not self.RPC_server:
            try:
                self.RPC_server = AuthServiceProxy(Config.SERVER_URL)
                print '... Connection established'
            except:
                print '....FAILED'
        
    
    def encrypt_wallet(self, passphrase, **kwargs):
        self.RPC_server.encryptwallet(passphrase)
                
    def poll_info(self, dtime):
        print 'Polling...'    
        self.loadingstate = True
        try:         
            self.blockcount = self.get_blockcount()
            self.balance = self.get_balance(False)
            self.unconfirmedbalance = self.get_balance(True)
            self.connections = self.get_connectioncount()
            self.txfee = self.get_txfee()
            self.networkdiff = self.get_networkdiff()
            self.myaddress = self.get_myaddress()
            self.get_last_transaction()
            self.set_connection_color()
        except:
            print 'trying to restart Valutod.exe'
            self.connect_rpc()
            
        self.loadingstate = False

    def lock_wallet(self, **kwargs):
        return self.RPC_server.walletlock()
    
    def get_networkdiff(self, **kwargs):
        return str(self.RPC_server.getinfo()['difficulty'])
                
    def get_myaddress(self, **kwargs):
        return str(self.RPC_server.getaccountaddress(Config.ACCOUNT_NAME))
                        
    def get_txfee(self, **kwargs):
        return str('{0:.8f}'.format(float(self.RPC_server.getinfo()['paytxfee'])))
        
    def get_connectioncount(self, **kwargs):
        return str(self.RPC_server.getinfo()['connections'])    
    
    def get_balance(self, UNCONFIRMED, **kwargs):
        if UNCONFIRMED:
            return str('{0:.8f}'.format(float(self.RPC_server.getbalance(Config.ACCOUNT_NAME, 0)) - float(self.balance)))
        else:
            return str('{0:.8f}'.format(float(self.RPC_server.getbalance(Config.ACCOUNT_NAME, 6))))

    def get_blockcount(self, **kwargs):
        return str(self.RPC_server.getinfo()['blocks'])
                       
    def set_connection_color(self, **kwargs):
        connbuffer = int(self.connections)
        if connbuffer < 2:
            self.connectioncolor = '#FF0000'
                
        elif connbuffer >= 2 and connbuffer < 3:
            self.connectioncolor = '#FFFF00'
        
        else:
            self.connectioncolor = '#00FF00'
            
    def set_passphrase(self, password, seconds, **kwargs):
        self.RPC_server.walletpassphrase(password, seconds)
                  
    def copyaction(self, copytxt, **kwargs):
        Snackbar(text='Copied to clipboard: ' + copytxt).show()
               
    def get_last_transaction(self, **kwargs):
        try:
            transbuffer = self.RPC_server.listtransactions(Config.ACCOUNT_NAME, 1,0)[0]['txid']
            
            if self.lasttransaction != transbuffer:
                self.lasttransaction = transbuffer
                Snackbar(text='Last transaction: ' + self.lasttransaction).show()
        except:
            print 'No transactions yet'
            
    def get_transactions(self, height, start, **kwargs):
        return self.RPC_server.listtransactions(Config.ACCOUNT_NAME, height, start)
