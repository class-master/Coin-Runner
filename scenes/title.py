# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.metrics import dp
class Title(Screen):
    def on_pre_enter(self):
        self.clear_widgets()
        self.add_widget(Label(text='[ Neon Runner A / Day1 ]\nEnter/Space/Touch', size_hint=(1,1), font_size=dp(24)))
    def on_key_down(self, key, keycode):
        # TODO: 'enter','numpadenter','spacebar' で play へ
        return False
    def on_touch_down(self,*_):
        self.manager.current='play'; return True
