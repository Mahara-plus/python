# PY RIDDLE QUEST v2

لعبة ألغاز عربية ببايثون وKivy.

- 500 سؤال موزعة على 5 أقسام: رياضيات، ذكاء ومنطق، Python، ألغاز عامة، أنماط وأرقام.
- 4 مستويات: سهل، متوسط، صعب، مستحيل.
- اختيار القسم والصعوبة، و10 أسئلة في الجولة.
- مؤقت 30/25/20/15 ثانية حسب الصعوبة.
- نقاط أعلى للأسئلة الأصعب ومكافأة للسرعة.
- تلميحات، حفظ أفضل نتيجة محلياً، أصوات، وانتقالات متحركة.

## التشغيل على الكمبيوتر
`pip install kivy` ثم `python main.py`

## بناء APK عبر GitHub
1. ارفع كل محتويات المشروع إلى مستودع GitHub على الفرع main.
2. افتح Actions وشغّل Build Android APK.
3. بعد نجاح البناء، نزّل Artifact باسم PyRiddleQuest-APK-v2 وفك ضغطه لتحصل على APK.

الناتج Debug للتجربة وليس إصدار Release موقعاً للنشر على Google Play.


## App icon
The Android launcher icon is `assets/icon.png`. It is configured in `buildozer.spec` and included in the APK during the GitHub Actions build.
