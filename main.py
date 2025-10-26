# -*- coding: utf-8 -*-
from kivymd.app import MDApp
from kivy.core.window import Window
from .config import P
from .scenes.title import Title
from .scenes.play import Play
from kivy.uix.screenmanager import ScreenManager

class GameApp(MDApp):
    def build(self):
        Window.size=(P.WINDOW_W,P.WINDOW_H)
        sm=ScreenManager(); sm.add_widget(Title(name="title")); sm.add_widget(Play(name="play")); sm.current="title"
        return sm

if __name__=="__main__":
    GameApp().run()
