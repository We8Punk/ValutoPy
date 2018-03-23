from kivy.uix.widget import Widget
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ListProperty
from kivy.app import App
from kivymd.snackbar import Snackbar
from kivy.clock import Clock

class TransactionListManager(Widget):

    transactionlist = ListProperty([
    ['','arrow-right-bold',''], 
    ['','arrow-right-bold',''], 
    ['','arrow-right-bold',''],
    ['','arrow-right-bold',''], 
    ['','arrow-right-bold',''],
    ['','arrow-right-bold',''], 
    ['','arrow-right-bold',''],
    ['','arrow-right-bold',''], 
    ['','arrow-right-bold','']])
    
    def __init__(self, **kwargs):
        super(TransactionListManager,self).__init__(**kwargs)
        Clock.schedule_interval(self.update_list, 15)
        
    def update_list(self, dtime):
        
        txbuff = list(reversed(App.get_running_app().network_manager.get_transactions(8,0)))
        for tx in range(8):
            try:
                self.transactionlist[tx] = self.build_listoutput(txbuff[tx])
            except:
                pass
			
    def build_listoutput(self, txbuffer, **kwargs):
        if txbuffer['category'] == 'receive':
            category='Received'
            color='#00FF00'
            icon='arrow-left-bold'
            
        elif txbuffer['category'] == 'send':
            category='Send'
            color='#FF0000'
            icon='arrow-right-bold'
            
        return [category + ' ' + 
        str(txbuffer['amount']) + ' via ' + 
        str(txbuffer['address']), icon, color]
        
class TransferManager(Widget):
    amount = StringProperty()
    address = StringProperty()
    address_hint = StringProperty()
    amount_hint = StringProperty()
    pass_hint = StringProperty()
    button_state = BooleanProperty()

    def __init__(self, **kwargs):
        super(TransferManager,self).__init__(**kwargs) 
        self.addressok = False
        self.amountok = False
        self.passwordok = False
        self.button_state = True
        
    def set_address(self, address, **kwargs):
        self.address = address
        if len(address) == 34:
            self.addressok = True
        else:
            self.addressok = False
            
        self.validate()
        
    def set_amount(self, amount, **kwargs):
        self.amount = amount
        try:
            amount = float(amount)
            self.amountok = True
        except:
            self.amountok = False
                
        self.validate()
    
    def set_pass(self, password, **kwargs):
        self.password = password
        if len(password) > 1 or password == "ValutoPy":
            self.passwordok = True
        else:
            self.passwordok = False                      
        self.validate()
                        
    def validate(self, **kwargs):
        if self.amountok and self.addressok and self.passwordok:
            self.button_state = False
        else:
            self.button_state = True
            
    def send_amount(self, **kwargs):
        #Not as pretty as i would like TODO
        App.get_running_app().network_manager.loadingstate = True
        try:
            if self.password == "ValutoPy":
                App.get_running_app().network_manager.send(self.address, self.amount)   
            else:    
                App.get_running_app().network_manager.lock_wallet()
                App.get_running_app().network_manager.set_passphrase(self.password, 100)
                App.get_running_app().network_manager.send(self.address, self.amount)   
                App.get_running_app().network_manager.lock_wallet() 
            Snackbar('It seems like the transaction went fine!').show() 
                
        except Exception as rpc_error:
            Snackbar(rpc_error[0]).show() 
            App.get_running_app().network_manager.loadingstate = False
            
        App.get_running_app().network_manager.loadingstate = False
            
        #Ugly hack, sry mama.... There seems to be a bug in KivyMD, so the button does not return to disable color, .
        self.amount_hint = ' '
        self.address_hint = ' '
        self.pass_hint = ' '
        self.amount_hint = ''
        self.address_hint = ''
        self.pass_hint = ''
        self.button_state = False
        self.button_state = True
