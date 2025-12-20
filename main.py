# -*- coding: utf-8 -*-
"""
Coin-Runner / NeonRunnerA 系（講師用）main.py
================================================

目的（このファイルで“埋める”もの）
- Day4（A：Title画面＆導線担当）の「Title → Play 導線」を
  “main.pyだけ”で確実に動かす（他ファイルのTODOは触らない）

重要な前提（ここで混乱しがち）
- scenes/title.py には「Enter/Spaceで play へ」の TODO があるが、
  今回は“そこを直さず” main.py 側で入力を拾って導線を成立させる。
- つまり main.py が「入力ルータ（キー入力を受けて画面遷移）」の役を持つ。

この方針のメリット
- 生徒の Title.py のTODO進捗に依存せず、授業進行が止まらない。
- 後で Title.py 側のTODOを実装したら、main.py の“保険”を薄くできる。

------------------------------------------------
DayNひも付け（コメントの意味）
- [Day1] : 画面サイズ固定（Window.size）
- [Day4-A] : Title → Play の導線（Enter/Space/Touch）
------------------------------------------------
"""

from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

# ------------------------------------------------------------
# 起動方法の差に強くする（動けば尚よし）
# - パッケージ実行: python -m <package>.main  → 相対importが通る
# - 直実行/環境差 : python main.py            → 相対importが落ちることがある
#
# なので「相対import → ダメなら絶対import」の順で保険を掛ける。
# ※ main.pyだけ変更で安定させたいので、ここで吸収する。
# ------------------------------------------------------------
try:
    # ふつうはこれ（パッケージとして実行される想定）
    from .config import P
    from .scenes.title import Title
    from .scenes.play import Play
except Exception:
    # もし相対importが落ちたら、同階層importで拾う（環境保険）
    from config import P
    from scenes.title import Title
    from scenes.play import Play


class GameApp(MDApp):
    """
    ここが“ゲーム全体の入口”。
    Day4-A（Title導線）を main.py だけで成立させるため、
    - ScreenManager を作る
    - Title/Play を登録する
    - Windowのキー入力を受け取り、必要なら画面遷移する
    を担当する。
    """

    def build(self):
        # ============================================================
        # [Day1] Windowサイズ固定
        # ============================================================
        # なぜやる？
        # - KivyはWindowが想定サイズとズレると、HUD座標や当たり判定の感覚が崩れやすい。
        # - 学習初期は「同じ画面で同じ結果」を優先したいので固定する。
        Window.size = (P.WINDOW_W, P.WINDOW_H)

        # ============================================================
        # ScreenManager 構築（Title / Play）
        # ============================================================
        self.sm = ScreenManager()
        self.sm.add_widget(Title(name="title"))
        self.sm.add_widget(Play(name="play"))
        self.sm.current = "title"

        # ============================================================
        # [Day4-A] キー入力（Enter/Space）で Title → Play 導線を成立させる
        # ============================================================
        # ポイント：
        # - scenes/title.py 側に TODO があるが、ここでは触らない。
        # - main.py が Window.on_key_down を受け取り、
        #   「title表示中に Enter/Space が来たら play へ」遷移させる。
        #
        # さらに“やさしさ”：
        # - もし各Screenに on_key_down(key, keycode) が実装されていたら、
        #   先にそれを呼んで「Screen側が処理した」場合はそちらを優先する。
        #   （将来、生徒が Title.py のTODOを実装しても競合しにくい）
        Window.bind(on_key_down=self._on_key_down)

        return self.sm

    # ------------------------------------------------------------
    # [Day4-A] 入力ルータ（main.pyだけで導線を作る核心）
    # ------------------------------------------------------------
    def _on_key_down(self, window, key, scancode, codepoint, modifiers):
        """
        Kivyのon_key_downシグネチャ：
          (window, key, scancode, codepoint, modifiers)

        ここでやること（優先順）
        1) まず「いま表示中のScreenが自分で処理したい」なら任せる
           - current_screen.on_key_down があれば呼ぶ
           - True が返ったら “Screen側で処理済み” とみなして終了
        2) 次に main.py の“保険ルール”を適用（授業止めない）
           - Title中に Enter/Space なら Playへ
        """

        # 1) Screen側に on_key_down(key, keycode) があるなら委譲
        #    ※ scenes/title.py にこのメソッドが既に定義されている（TODOだが）
        try:
            current = self.sm.current_screen
            if hasattr(current, "on_key_down"):
                # Kivyの慣例に合わせて keycode は (key, name) っぽく渡す
                # name は厳密には取りづらいので、ここでは最低限で渡す
                handled = current.on_key_down(key, (key, codepoint))
                if handled:
                    return True
        except Exception:
            # 失敗しても授業を止めない（ここは保険）
            pass

        # 2) main.py の保険ルール：Title → Play
        # ------------------------------------------------------------
        # Kivyのキーコードは環境差がありうるので、複数条件で拾う：
        # - Enter: 13
        # - NumpadEnter: 271（環境によって違うことも）
        # - Space: 32
        # codepoint は通常 ' ' など文字になることが多い（Enterは空になりがち）
        # ------------------------------------------------------------
        if self.sm.current == "title":
            if key in (13, 271, 32) or codepoint in (" ", "\r", "\n"):
                self.sm.current = "play"
                return True

        return False


if __name__ == "__main__":
    GameApp().run()
    
