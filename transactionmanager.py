from kivy.uix.widget import Widget
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.app import App
from kivymd.snackbar import Snackbar

class TransactionListManager(Widget):
    
    def __init__(self, **kwargs):
        super(TransferManager,self).__init__(**kwargs)
        pass
        
class TransferManager(Widget):
    amount = StringProperty()
    address = StringProperty()
    address_hint = StringProperty()
    amount_hint = StringProperty()
    button_state = BooleanProperty()

    def __init__(self, **kwargs):
        super(TransferManager,self).__init__(**kwargs) 
        self.addressok = False
        self.amountok = False
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
                
    def validate(self, **kwargs):
        if self.amountok and self.addressok:
            self.button_state = False
        else:
            self.button_state = True
            
    def send_amount(self, **kwargs):
        try:
            App.get_running_app().network_manager.send(self.address, self.amount)    
        except Exception as rpc_error:
            rpc_error = str(rpc_error).split(':')
            Snackbar(rpc_error[1]).show() 
            
        #Ugly hack, sry mama....
        self.amount_hint = ' '
        self.address_hint = ' '
        self.amount_hint = ''
        self.address_hint = ''
        self.button_state = True
