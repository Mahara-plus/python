# -*- coding: utf-8 -*-
"""
CODE QUEST - لعبة ألغاز برمجية (بايثون فقط)
تصميم بأسلوب Code Editor داكن مع إضاءة Neon
"""
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from questions import QUESTIONS
import random

# ---------- Palette (Code Editor Theme) ----------
BG        = get_color_from_hex("#0D1117")   # خلفية داكنة
SURFACE   = get_color_from_hex("#161B22")   # بطاقات
BORDER    = get_color_from_hex("#30363D")
GREEN     = get_color_from_hex("#39FF14")   # نيون أخضر
CYAN      = get_color_from_hex("#00E5FF")
PURPLE    = get_color_from_hex("#BC8CF2")
RED       = get_color_from_hex("#FF5555")
WHITE     = get_color_from_hex("#F0F6FC")
GRAY      = get_color_from_hex("#8B949E")

Window.clearcolor = BG


def neon_button(text, color=GREEN, font_size=20):
    btn = Button(
        text=text, font_size=dp(font_size), bold=True,
        background_normal="", background_color=(0, 0, 0, 0),
        color=WHITE, size_hint_y=None, height=dp(60),
    )
    def draw_bg(*a):
        btn.canvas.before.clear()
        with btn.canvas.before:
            Color(*color[:3], 0.25)
            RoundedRectangle(pos=btn.pos, size=btn.size, radius=[12])
            Color(*color)
            Line(rounded_rectangle=(btn.x, btn.y, btn.width, btn.height, 12), width=1.6)
    btn.bind(pos=lambda *a: draw_bg(), size=lambda *a: draw_bg())
    draw_bg()
    return btn


class CodeCard(BoxLayout):
    """بطاقة كود بإطار Neon"""
    def __init__(self, code_text, color=GREEN, **kw):
        super().__init__(orientation="vertical", size_hint_y=None, padding=dp(12), spacing=dp(6), **kw)
        self.code_text = code_text
        self.color = color
        self.bind(minimum_height=self.setter("height"))
        self.header = Label(
            text="[color=#8B949E]  ● ● ●  python_snippet.py[/color]",
            markup=True, size_hint_y=None, height=dp(26),
            font_size=dp(13), halign="left", valign="middle",
        )
        self.code = Label(
            text=code_text, font_name="RobotoMono-Regular.ttf",
            size_hint_y=None, font_size=dp(16),
            color=WHITE, halign="left", valign="top",
            padding=(dp(10), dp(8)),
        )
        self.code.bind(texture_size=self._fit)
        self.add_widget(self.header)
        self.add_widget(self.code)

    def _fit(self, *a):
        self.code.height = self.code.texture_size[1] + dp(16)
        self.height = self.code.height + self.header.height + dp(30)

    def on_size(self, *a):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*SURFACE)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[14])
            Color(*self.color)
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 14), width=1.8)


class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        root = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(14))
        root.add_widget(Image(source="assets/logo.png", size_hint_y=0.42, allow_stretch=True, keep_ratio=True))

        title = Label(text="[b][color=#00E5FF]CODE[/color] [color=#F0F6FC]QUEST[/color][/b]",
                      markup=True, font_size=dp(38), size_hint_y=None, height=dp(60))
        sub = Label(text="[color=#8B949E]ألغاز برمجية بلغة بايثون فقط[/color]", markup=True,
                    font_size=dp(17), size_hint_y=None, height=dp(40))
        root.add_widget(title); root.add_widget(sub)

        stats = App.get_running_app().stats
        self.best = Label(text=f"[color=#39FF14]★ أفضل نتيجة: {stats['best']} / {len(QUESTIONS)}[/color]",
                          markup=True, font_size=dp(16), size_hint_y=None, height=dp(36))
        root.add_widget(self.best)

        start = neon_button("▶  ابدأ اللعب", GREEN, 22)
        start.bind(on_release=lambda *a: setattr(self.manager, "current", "quiz"))
        root.add_widget(start)

        how = neon_button("؟  طريقة اللعب", CYAN, 18)
        how.bind(on_release=lambda *a: setattr(self.manager, "current", "howto"))
        root.add_widget(how)
        self.add_widget(root)


class HowToScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        root = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(14))
        root.add_widget(Label(text="[b][color=#00E5FF]طريقة اللعب[/color][/b]", markup=True,
                              font_size=dp(28), size_hint_y=None, height=dp(70)))
        txt = ("• لديك [color=#39FF14]20 سؤالاً[/color] برمجياً بلغة بايثون\n"
               "• مع كل سؤال [color=#00E5FF]30 ثانية[/color] فقط!\n"
               "• اختر الإجابة الصحيحة من 4 خيارات\n"
               "• الإجابة الصحيحة تمنحك [color=#39FF14]+10 نقاط[/color]\n"
               "• حاول تحقيق العلامة الكاملة!\n\n"
               "[color=#BC8CF2]# التعليقات داخل الكود قد تحمل تلميحات ;)[/color]")
        card = CodeCard(txt, PURPLE)
        scroll = ScrollView(); scroll.add_widget(card)
        root.add_widget(scroll)
        back = neon_button("← رجوع", RED, 18)
        back.bind(on_release=lambda *a: setattr(self.manager, "current", "menu"))
        root.add_widget(back)
        self.add_widget(root)


class QuizScreen(Screen):
    TIME_LIMIT = 30

    def on_enter(self):
        self.order = random.sample(range(len(QUESTIONS)), len(QUESTIONS))
        self.idx = 0
        self.score = 0
        self.correct = 0
        self._build_question()

    def _build_question(self):
        self.clear_widgets()
        self.time_left = self.TIME_LIMIT
        q = QUESTIONS[self.order[self.idx]]

        root = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))

        top = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        top.add_widget(Label(text=f"[color=#8B949E]سؤال {self.idx+1}/{len(QUESTIONS)}[/color]",
                             markup=True, font_size=dp(16)))
        self.timer_lbl = Label(text="", markup=True, font_size=dp(16),
                               size_hint_x=None, width=dp(120))
        top.add_widget(self.timer_lbl)
        root.add_widget(top)

        self.bar = ProgressBar(max=self.TIME_LIMIT, value=self.TIME_LEFT,
                               size_hint_y=None, height=dp(8))
        root.add_widget(self.bar)

        self.score_lbl = Label(text=f"[color=#39FF14]النقاط: {self.score}[/color]",
                               markup=True, font_size=dp(16), size_hint_y=None, height=dp(32))
        root.add_widget(self.score_lbl)

        body = ScrollView()
        col = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(10), padding=dp(4))
        col.bind(minimum_height=col.setter("height"))
        col.add_widget(CodeCard(q["code"], GREEN if q.get("hint") is None else CYAN))
        qtext = Label(text=f"[b]{q['q']}[/b]", markup=True, font_size=dp(18),
                      color=WHITE, size_hint_y=None, halign="right", valign="middle",
                      text_size=(Window.width - dp(60), None), padding=(dp(6), dp(10)))
        qtext.bind(texture_size=lambda *a: setattr(qtext, "height", qtext.texture_size[1] + dp(10)))
        col.add_widget(qtext)
        body.add_widget(col)
        root.add_widget(body)

        grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(150))
        self.ans_btns = []
        opts = list(q["options"]); random.shuffle(opts)
        for opt in opts:
            btn = neon_button(opt, GREEN, 16)
            btn.height = dp(64)
            btn.bind(on_release=self._choose)
            self.ans_btns.append(btn)
            grid.add_widget(btn)
        root.add_widget(grid)
        self.add_widget(root)
        self._update_timer()
        self._ev = Clock.schedule_interval(self._tick, 1)

    def _update_timer(self):
        color = "#39FF14" if self.time_left > 10 else "#FF5555"
        self.timer_lbl.text = f"[color={color}]⏱ {self.time_left}s[/color]"
        self.bar.value = self.time_left

    def _tick(self, dt):
        self.time_left -= 1
        if self.time_left <= 0:
            self._ev.cancel()
            self._reveal(None)
            return
        self._update_timer()

    def _choose(self, btn):
        self._ev.cancel()
        self._reveal(btn.text)

    def _reveal(self, chosen):
        q = QUESTIONS[self.order[self.idx]]
        ok = (chosen == q["answer"])
        if ok:
            self.score += 10
            self.correct += 1
        for b in self.ans_btns:
            b.disabled = True
            if b.text == q["answer"]:
                b.background_color = (*GREEN, 1)
        popup = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(12))
        res = ("[color=#39FF14][b]✔ إجابة صحيحة! +10[/b][/color]" if ok
               else f"[color=#FF5555][b]✘ خطأ! الصحيح:[/b][/color]\n[color=#39FF14]{q['answer']}[/color]")
        if q.get("explain"):
            res += f"\n\n[color=#8B949E]# {q['explain']}[/color]"
        lbl = Label(text=res, markup=True, font_size=dp(18), halign="center", valign="middle",
                    text_size=(Window.width - dp(80), None))
        lbl.bind(texture_size=lambda *a: setattr(lbl, "height", lbl.texture_size[1]))
        popup.add_widget(lbl)
        nxt = neon_button("التالي ←" if self.idx < len(QUESTIONS)-1 else "النتيجة ←", CYAN, 18)
        nxt.bind(on_release=self._next)
        popup.add_widget(nxt)
        self.clear_widgets()
        s = BoxLayout(orientation="vertical", padding=dp(24))
        s.add_widget(popup)
        self.add_widget(s)

    def _next(self, *a):
        self.idx += 1
        if self.idx >= len(QUESTIONS):
            app = App.get_running_app()
            app.stats["best"] = max(app.stats["best"], self.correct)
            app.save_stats()
            self.manager.get_screen("result").set_result(self.correct, self.score)
            self.manager.current = "result"
        else:
            self._build_question()


class ResultScreen(Screen):
    def set_result(self, correct, score):
        self.clear_widgets()
        total = len(QUESTIONS)
        pct = correct / total
        if pct == 1:   msg, col = "🏆 عبقري بايثون! علامة كاملة!", GREEN
        elif pct >= .7: msg, col = "🔥 ممتاز! مستوى Senior", CYAN
        elif pct >= .5: msg, col = "💪 جيد جداً! واصل التقدم", PURPLE
        else:           msg, col = "📚 راجع أساسيات بايثون وحاول مجدداً", RED

        root = BoxLayout(orientation="vertical", padding=dp(24), spacing=dp(14))
        root.add_widget(Image(source="assets/logo.png", size_hint_y=0.35))
        root.add_widget(Label(text="[b][color=#00E5FF]النتيجة النهائية[/color][/b]",
                              markup=True, font_size=dp(30), size_hint_y=None, height=dp(70)))
        root.add_widget(Label(text=f"[b][size=64][color=#39FF14]{correct}/{total}[/color][/size][/b]",
                              markup=True, size_hint_y=None, height=dp(110)))
        root.add_widget(Label(text=f"[color=#8B949E]النقاط: {score}[/color]", markup=True,
                              font_size=dp(18), size_hint_y=None, height=dp(40)))
        root.add_widget(Label(text=f"[b][color=#{self._hex(col)}]{msg}[/color][/b]",
                              markup=True, font_size=dp(18), size_hint_y=None, height=dp(60),
                              halign="center"))
        again = neon_button("↻ العب مجدداً", GREEN, 20)
        again.bind(on_release=lambda *a: setattr(self.manager, "current", "quiz"))
        home = neon_button("⌂ القائمة الرئيسية", CYAN, 18)
        home.bind(on_release=lambda *a: setattr(self.manager, "current", "menu"))
        root.add_widget(again); root.add_widget(home)
        self.add_widget(root)

    def _hex(self, c):
        return "".join(f"{int(v*255):02X}" for v in c[:3])


class CodeQuestApp(App):
    def build(self):
        self.title = "Code Quest - ألغاز بايثون"
        self.stats = {"best": 0}
        try:
            with open(self.user_data_dir + "/stats.json") as f:
                self.stats = json.load(f)
        except Exception:
            pass
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(HowToScreen(name="howto"))
        sm.add_widget(QuizScreen(name="quiz"))
        sm.add_widget(ResultScreen(name="result"))
        return sm

    def save_stats(self):
        try:
            with open(self.user_data_dir + "/stats.json", "w") as f:
                json.dump(self.stats, f)
        except Exception:
            pass


if __name__ == "__main__":
    import json
    CodeQuestApp().run()
