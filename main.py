import json, random, os, re
from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, RoundedRectangle

Window.clearcolor=(.025,.04,.07,1)
CYAN=(0,.84,.96,1); GREEN=(.20,.91,.59,1); WHITE=(.91,.95,1,1)
MUTED=(.48,.62,.72,1); PANEL=(.055,.085,.14,1); ORANGE=(1,.69,.28,1)
DIFFS=["سهل","متوسط","صعب","مستحيل"]
CATEGORIES=["الكل","Python","JavaScript","SQL","HTML/CSS","الأمن السيبراني البرمجي"]
TIMES={"سهل":30,"متوسط":25,"صعب":20,"مستحيل":15}
POINTS={"سهل":10,"متوسط":20,"صعب":30,"مستحيل":50}
def norm(s):
    s=str(s).strip().lower()
    for a,b in [("أ","ا"),("إ","ا"),("آ","ا"),("ى","ي"),("ة","ه"),("ـ","")]: s=s.replace(a,b)
    return re.sub(r"\s+","",s)
class Panel(BoxLayout):
    def __init__(self,**kw):
        super().__init__(**kw)
        with self.canvas.before:
            Color(*PANEL); self.rect=RoundedRectangle(pos=self.pos,size=self.size,radius=[dp(18)])
        self.bind(pos=self.sync,size=self.sync)
    def sync(self,*_): self.rect.pos=self.pos; self.rect.size=self.size
class RiddleQuest(App):
    def build(self):
        self.title="CODE QUEST"; self.questions=json.load(open(os.path.join(os.path.dirname(__file__),"questions.json"),encoding="utf-8"))
        self.best=0; self.sound_on=True; self.timer_event=None; self.load_best()
        self.root=BoxLayout(orientation="vertical",padding=dp(16),spacing=dp(10))
        row=BoxLayout(size_hint_y=None,height=dp(58)); brand=BoxLayout(orientation="vertical")
        brand.add_widget(Label(text="[b]CODE_QUEST[/b]",markup=True,color=CYAN,font_size="23sp",halign="left"))
        brand.add_widget(Label(text="CODE / DEBUG / BUILD",color=MUTED,font_size="10sp",halign="left"))
        row.add_widget(brand); self.best_lbl=Label(text=f"BEST {self.best}",color=GREEN,bold=True,size_hint_x=.35); row.add_widget(self.best_lbl)
        self.root.add_widget(row); self.progress=ProgressBar(max=10,size_hint_y=None,height=dp(5)); self.root.add_widget(self.progress)
        self.body=Panel(orientation="vertical",padding=dp(14),spacing=dp(9)); self.root.add_widget(self.body)
        self.status=Label(text="SYSTEM ONLINE // PROGRAMMING CHALLENGE ENGINE",color=MUTED,size_hint_y=None,height=dp(22),font_size="9sp"); self.root.add_widget(self.status)
        self.home(); return self.root
    def load_best(self):
        try: self.best=json.load(open(os.path.join(self.user_data_dir,"record.json"),encoding="utf-8")).get("best",0)
        except: self.best=0
    def save_best(self):
        os.makedirs(self.user_data_dir,exist_ok=True)
        json.dump({"best":self.best},open(os.path.join(self.user_data_dir,"record.json"),"w",encoding="utf-8"))
    def clear(self):
        if self.timer_event: self.timer_event.cancel(); self.timer_event=None
        self.body.clear_widgets()
    def lbl(self,t,size=15,c=WHITE,b=False,h=None):
        x=Label(text=t,color=c,font_size=f"{size}sp",bold=b,halign="center",valign="middle")
        if h: x.size_hint_y=None; x.height=dp(h)
        return x
    def btn(self,t,fn,c=(.12,.22,.34,1),h=45):
        x=Button(text=t,size_hint_y=None,height=dp(h),background_normal="",background_color=c,color=WHITE,bold=True)
        x.bind(on_release=lambda *_:fn()); return x
    def home(self):
        self.clear(); self.body.add_widget(self.lbl("مرحباً بك في تحديات البرمجة",22,CYAN,True,48))
        self.body.add_widget(self.lbl("500 تحدٍ برمجي • 5 مسارات تقنية • 4 مستويات",13,MUTED,False,30))
        self.body.add_widget(self.lbl(f"أفضل نتيجة محفوظة: {self.best}",15,GREEN,True,32))
        self.body.add_widget(self.lbl("اختر مسار البرمجة",15,WHITE,True,26))
        for cat in CATEGORIES: self.body.add_widget(self.btn(cat,lambda c=cat:self.select_category(c),(.09,.17,.26,1),40))
        self.body.add_widget(self.btn("الصوت: "+("تشغيل 🔊" if self.sound_on else "إيقاف 🔇"),self.toggle_sound))
    def select_category(self,cat):
        self.category=cat; self.clear(); self.body.add_widget(self.lbl("حدد مستوى الصعوبة",22,CYAN,True,50))
        for d in ["الكل"]+DIFFS: self.body.add_widget(self.btn(d,lambda x=d:self.start_game(x),(.09,.17,.26,1),50))
        self.body.add_widget(self.btn("رجوع",self.home))
    def toggle_sound(self): self.sound_on=not self.sound_on; self.home()
    def sound(self,kind):
        if not self.sound_on: return
        try:
            s=SoundLoader.load(os.path.join(os.path.dirname(__file__),"assets",kind+".wav"))
            if s: s.play()
        except: pass
    def start_game(self,diff):
        self.difficulty=diff
        pool=[q for q in self.questions if (self.category=="الكل" or q["category"]==self.category) and (diff=="الكل" or q["difficulty"]==diff)]
        random.shuffle(pool); self.deck=pool[:10]; self.index=0; self.score=0; self.hints=2; self.correct=0
        self.progress.max=len(self.deck); self.progress.value=0; self.show_question()
    def show_question(self):
        if self.index>=len(self.deck): return self.finish()
        self.clear(); self.current=self.deck[self.index]
        self.body.add_widget(self.lbl(f"// CHALLENGE {self.index+1:02d}/{len(self.deck):02d}",12,CYAN,True,26))
        self.body.add_widget(self.lbl(self.current["category"]+" • "+self.current["difficulty"],13,ORANGE,True,28))
        self.timer_lbl=self.lbl("",19,ORANGE,True,30); self.body.add_widget(self.timer_lbl)
        self.body.add_widget(self.lbl(self.current["question"],18,WHITE,True))
        self.entry=TextInput(hint_text="اكتب ناتج الكود أو الإجابة البرمجية...",multiline=False,size_hint_y=None,height=dp(50),font_size="17sp",
            background_normal="",background_active="",background_color=(.09,.14,.21,1),foreground_color=WHITE,cursor_color=CYAN)
        self.entry.bind(on_text_validate=lambda *_:self.check()); self.body.add_widget(self.entry)
        row=BoxLayout(size_hint_y=None,height=dp(46),spacing=dp(8))
        row.add_widget(self.btn("تحقق",self.check,CYAN,46)); row.add_widget(self.btn("تلميح",self.hint,(.16,.27,.40,1),46)); self.body.add_widget(row)
        self.feedback=self.lbl("حل التحدي البرمجي قبل انتهاء الوقت.",12,MUTED,False,34); self.body.add_widget(self.feedback)
        self.stats=self.lbl("",12,GREEN,True,26); self.body.add_widget(self.stats); self.refresh_stats()
        self.remaining=TIMES[self.current["difficulty"]]; self.update_timer()
        self.timer_event=Clock.schedule_interval(self.tick,1)
        self.body.opacity=0; Animation(opacity=1,duration=.25).start(self.body)
    def refresh_stats(self): self.stats.text=f"النقاط: {self.score}    التلميحات: {self.hints}"
    def update_timer(self): self.timer_lbl.text=f"⏱ {self.remaining} ثانية"
    def tick(self,dt):
        self.remaining-=1; self.update_timer()
        if self.remaining<=0:
            self.timer_event.cancel(); self.timer_event=None
            self.feedback.text="انتهى الوقت! الإجابة: "+self.current["answers"][0]; self.feedback.color=ORANGE
            Clock.schedule_once(self.advance,2)
    def check(self):
        if not self.entry.text.strip(): self.feedback.text="اكتب إجابة أولاً."; return
        if norm(self.entry.text) in [norm(a) for a in self.current["answers"]]:
            if self.timer_event: self.timer_event.cancel(); self.timer_event=None
            gained=POINTS[self.current["difficulty"]]+max(0,self.remaining//5)
            self.score+=gained; self.correct+=1; self.sound("correct")
            self.feedback.text=f"✓ إجابة صحيحة! +{gained} نقطة"; self.feedback.color=GREEN
            self.refresh_stats(); Clock.schedule_once(self.advance,1.1)
        else:
            self.sound("wrong"); self.feedback.text="✕ إجابة غير صحيحة، حاول مرة أخرى."; self.feedback.color=(1,.38,.42,1)
    def hint(self):
        if self.hints<=0: self.feedback.text="انتهت التلميحات."; return
        self.hints-=1; self.feedback.text="تلميح: "+self.current["hint"]; self.feedback.color=ORANGE; self.refresh_stats()
    def advance(self,*_): self.index+=1; self.progress.value=self.index; self.show_question()
    def finish(self):
        self.clear()
        if self.score>self.best: self.best=self.score; self.save_best(); self.best_lbl.text=f"BEST {self.best}"
        self.body.add_widget(self.lbl("CODING RUN COMPLETE",23,GREEN,True,55))
        self.body.add_widget(self.lbl(f"نتيجتك: {self.score} نقطة",24,WHITE,True,55))
        self.body.add_widget(self.lbl(f"إجابات صحيحة: {self.correct}/{len(self.deck)}",15,CYAN,True,38))
        self.body.add_widget(self.lbl(f"أفضل نتيجة: {self.best}",15,GREEN,True,38))
        self.body.add_widget(self.btn("إعادة اللعب",lambda:self.start_game(self.difficulty),CYAN,50))
        self.body.add_widget(self.btn("القائمة الرئيسية",self.home,(.12,.22,.34,1),46))
if __name__=="__main__": RiddleQuest().run()
