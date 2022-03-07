#!/usr/bin/python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------
import kivy
kivy.require('1.9.1')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.settings import SettingsWithSpinner as Settings
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from kivy.properties import ObjectProperty, ListProperty
from kivy.config import ConfigParser
from kivy.clock import Clock
#-----------------------------------------------------------------------
from jnius import autoclass, cast
#-----------------------------------------------------------------------
from client import Client as GarageClient
#-----------------------------------------------------------------------
global APP, config, wifimanager
#-----------------------------------------------------------------------


def on_settings_end(s):
   s.parent.remove_widget(s)

class GradientWidget(Widget):

   col1 = ListProperty([0,0,255,255])
   col2 = ListProperty([0,0,0,255])

   def __init__(self,**kwargs):
      super(GradientWidget,self).__init__(**kwargs)
      self.background_texture = Texture.create(size=(1,2))
      buf = b''.join(map(chr,self.col1+self.col2))
      self.background_texture.blit_buffer(buf,colorfmt='rgba',bufferfmt='ubyte')
      self.bind(pos=self.update_background_pos_size,size=self.update_background_pos_size)
      with self.canvas.before:
         self.background = Rectangle(texture=self.background_texture,pos=self.pos,size=self.size)
      self.bind(col1=self.update_background_texture,col2=self.update_background_texture)
      if 'col1' in kwargs : self.col1 = kwargs['col1']
      if 'col2' in kwargs : self.col2 = kwargs['col2']

   def update_background_pos_size(self,*args,**kwargs):
      self.background.pos  = self.pos
      self.background.size = self.size

   def update_background_texture(self,*args,**kwargs):
      buf = b''.join(map(chr,self.col1+self.col2))
      self.background_texture.blit_buffer(buf,colorfmt='rgba',bufferfmt='ubyte')
      self.background.texture = self.background_texture

class WifiButton(Button):

   idicon = ObjectProperty(None)
   idtxt  = ObjectProperty(None)

   def __init__(self,**kwargs):
      super(WifiButton,self).__init__(**kwargs)
      self.active = False
      wifimanager.wifibutton_handle = self

   def on_release(self):
      wifimanager.toggle_connectivity()

   def set_activation(self,active):
      self.active = active
      if active:
         self.idicon.source = './data/wifi_on.png'
         self.idtxt.text = u'[b]Wifi activé[/b]'
         self.idtxt.color = (1,1,1)
      else:
         self.idicon.source = './data/wifi_off.png'
         self.idtxt.text = u'[b]Wifi désactivé[/b]'
         self.idtxt.color = (0.451,0.451,0.451)

class ActButton(Button):

   idicon = ObjectProperty(None)
   idtxt  = ObjectProperty(None)

   def __init__(self,**kwargs):
      super(ActButton,self).__init__(**kwargs)
      self.active = False
      wifimanager.actbutton_handle = self

   def on_release(self):
      if self.active and self.parent._pressed_action:
         self.parent.action()

   def set_activation(self,active):
      self.active = active
      if active:
         self.idicon.source = './data/action_on.png'
         self.idtxt.color = (1,1,1)
      else:
         self.idicon.source = './data/action_off.png'
         self.idtxt.color = (0.451,0.451,0.451)
      self.idtxt.texture_update()

class GradientBoxLayout(BoxLayout,GradientWidget):

   wifibutton = ObjectProperty(None)
   actbutton  = ObjectProperty(None)

   def get_garage_client(self):
      server_ip = config.get('Raspberry address','ip')
      server_port = config.getint('Raspberry address','port')
      c = GarageClient(server_ip,server_port)
      return c

   def action(self):
      c = self.get_garage_client()
      try:
         c.garage_press()
         self.actbutton.idtxt.color = (0.2,1,0.2)
      except:
         self.actbutton.idtxt.color = (1,0.2,0.2)

   def on_touch_down(self,touch):
      self._pressed_action = self.actbutton.collide_point(*touch.pos)
      self._pressed_touch = touch
      return super(GradientBoxLayout,self).on_touch_down(touch)

   def on_touch_up(self,touch):
      if self._pressed_action and self.wifibutton.collide_point(*touch.pos)\
         and self._pressed_touch is touch:
         self._pressed_action = False
         self.spawn_settings()
      return super(GradientBoxLayout,self).on_touch_up(touch)

   def spawn_settings(self):
      s = Settings()
      s.add_json_panel('Akenasai settings',config,'./config.json')
      s.bind(on_close=on_settings_end)
      self.parent.add_widget(s)

class AkenasaiApp(App) : pass

#-----------------------------------------------------------------------

class WifiManager:

   def __init__(self):

      # Load classes
      self.PythonActivity = autoclass('org.kivy.android.PythonActivity')
      self.activity = self.PythonActivity.mActivity
      self.Context = autoclass('android.content.Context')

      # Get wifi_service object
      self.wifi_service = self.activity.getSystemService(self.Context.WIFI_SERVICE)

      # Last connection status
      self._was_connected = False

   def update(self,dt):
      connected = self.is_connected()
      if connected <> self._was_connected:
         self._was_connected = connected
         self.set_activation(connected)

   def set_activation(self,active):
      self.actbutton_handle.set_activation(active)
      self.wifibutton_handle.set_activation(active)

   def is_connected(self):

      # Check enabled
      wifi_enabled = self.wifi_service.isWifiEnabled()
      if not wifi_enabled: return False

      # Check SSID
      ssid = self.wifi_service.getConnectionInfo().getSSID()
      ssid_target = config.get('Wifi','ssid')
      if not ssid_target in ssid: return False

      # All OK
      return True

   def toggle_connectivity(self):
      self.wifi_service.setWifiEnabled(not self.is_connected())

#-----------------------------------------------------------------------

if __name__=='__main__':
   config = ConfigParser()
   config.read('config.ini')
   wifimanager = WifiManager()
   APP = AkenasaiApp()
   Clock.schedule_interval(wifimanager.update,config.getint('Wifi','update_interval'))
   APP.run()










