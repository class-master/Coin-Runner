# -*- coding: utf-8 -*-
# Day1のTODOを保ちつつ、Day2のヒント（D2:）を追記。
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.clock import Clock

from ..config import P
from ..ui.hud import build_hud
from ..game.player import Player
from ..game.obstacle import Obj
from ..game.spawner import initial_x, pick_kind
# Day2で使用予定のもの（実装はTODO）
# from ..ui.parallax import ParallaxLayer
# from ..game.spawner import SpawnState

def clamp(v, lo, hi): return lo if v < lo else hi if v > hi else v
def aabb(ax, ay, aw, ah, bx, by, bw, bh):
    return (ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by)

GROUND_Y    = dp(P.GROUND_Y_PX)
SPAWN_SPREAD= dp(P.SPAWN_SPREAD_PX)
LOW_JUMP_H  = dp(P.JUMP_TIER_PX)

class GroundLine(FloatLayout):
    color = ListProperty([0.6,0.6,0.9,1])

class Play(Screen):
    def on_pre_enter(self):
        self.root=FloatLayout(); self.add_widget(self.root)
        self.lbl=build_hud(); self.root.add_widget(self.lbl)
        self.player=Player(size=(dp(52),dp(52))); self.player.pos=(dp(80),GROUND_Y); self.root.add_widget(self.player)
        self.objects=[]
        for i in range(6):
            o=Obj(size=(dp(42),dp(42)))
            k=pick_kind(P.COIN_RATE)
            o.color=[0.35,1,0.35,1] if k=='coin' else [1,0.35,0.4,1]
            o.pos=(initial_x(SPAWN_SPREAD, True), GROUND_Y if (pick_kind(0.5)=='ob') else GROUND_Y+LOW_JUMP_H)
            o.kind=k; o.vx=P.BASE_SPEED
            self.objects.append(o); self.root.add_widget(o)
        self.t=0.0; self.speed=P.BASE_SPEED; self.score=0; self.energy=100; self.game_over=False
        Window.bind(on_key_down=self._on_key)
        self._ev=Clock.schedule_interval(self.update,1/60)
    def on_pre_leave(self):
        try:
            Window.unbind(on_key_down=self._on_key)
            if self._ev: self._ev.cancel()
        except Exception: pass
    def _on_key(self,_w,key,scancode,codepoint,keycode,*_):
        name=keycode[1]
        if self.game_over and name in ('enter','numpadenter','spacebar'):
            return self._restart()
        if name in ('up','spacebar'):
            # TODO(Day1): self.player.try_jump(P)
            return True
        return False
    def update(self, dt):
        if self.game_over: return
        # TODO(Day1-2): 速度段階UP
        # TODO(Day1-3): 重力＆地面クランプ
        # TODO(Day1-4): スクロール＆再配置
        # TODO(Day1-5): 当たり判定（AABB）
        # TODO(Day1-6): HUD更新／ゲームオーバー表示
        # ---- D2: ここから追加ヒント（実装は自分で） ----
        # D2-1: パララックス背景 tick（速度は self.speed * 比率）
        # D2-2: SpawnState を使って再配置する（next_item→kind/座標/サイズ）
        # D2-3: kind に応じて色・サイズを切替（ob_low/ob_high/ob_train/coin）
        # D2-4: F1でデバッグ表示のON/OFF（時間・速度・next_x・last_kind）
        pass
    def _restart(self):
        self.t=0.0; self.speed=P.BASE_SPEED; self.score=0; self.energy=100; self.game_over=False
        self.player.pos=(dp(80),GROUND_Y); self.player.vy=0; self.player.on_ground=True
        for o in self.objects:
            o.pos=(initial_x(SPAWN_SPREAD, True), GROUND_Y if (pick_kind(0.5)=='ob') else GROUND_Y+LOW_JUMP_H)
        return True
