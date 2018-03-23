#####################################################################
# THIS SOFTWARE IS RELEASED AND CODED BY WEBPUNK WITH NO WARRANTIES #
#                              2018                                 #                                 
#####################################################################      

import kivy
kivy.require('1.0.6') # Kivy version
import os
os.environ['KIVY_IMAGE'] = 'pil,sdl2'
import pyperclip
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.button import MDIconButton
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.theming import ThemeManager
from kivy.lang import Builder
from network import NetworkManager
from transaction import TransferManager, TransactionListManager
from kivy.config import Config
Config.set('input', 'mouse', 'mouse, multitouch_on_demand')



class IconLeftInfoWidget(ILeftBodyTouch, MDIconButton):
    pass
                 
class ValutoPyApp(App):   
    theme_cls = ThemeManager()
    network_manager = NetworkManager()
    transfer_manager = TransferManager()
    transaction_manager = TransactionListManager()
    
    def build(self):
        self.icon = 'valuto_logo.png'
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette ='BlueGrey'               
        main_widget = Builder.load_file('main.kv')
        return main_widget
        
    def on_stop(self):
        self.network_manager.kill_valutod()
    
if __name__ == '__main__':
    ValutoPyApp().run()
    
