# -*- coding: utf-8 -*-
"""بنك الأسئلة - ألغاز برمجية بلغة بايثون فقط"""

QUESTIONS = [
    {"code": "x = 5\ny = '5'\nprint(x + int(y))",
     "q": "ما ناتج تنفيذ هذا الكود؟",
     "options": ["55", "10", "TypeError", "'55'"], "answer": "10",
     "explain": "int('5') يحول النص إلى رقم 5، والمجموع 10"},

    {"code": "a = [1, 2, 3]\nb = a\nb.append(4)\nprint(a)",
     "q": "ما الذي سيطبعه الكود؟",
     "options": ["[1, 2, 3]", "[1, 2, 3, 4]", "[4]", "Error"], "answer": "[1, 2, 3, 4]",
     "explain": "b تشير لنفس الكائن في الذاكرة (reference)"},

    {"code": "print(bool('False'))",
     "q": "ما ناتج هذا الكود؟",
     "options": ["False", "True", "Error", "'False'"], "answer": "True",
     "explain": "أي نص غير فارغ يُعتبر True حتى لو كان 'False'"},

    {"code": "s = 'python'\nprint(s[1:4])",
     "q": "ما ناتج القطع (slicing)؟",
     "options": ["yth", "pyt", "ytho", "hon"], "answer": "yth",
     "explain": "الفهرس 1 هو 'y' وحتى الفهرس 3 (النهاية غير شاملة)"},

    {"code": "def f(x=[]):\n    x.append(1)\n    return x\nprint(f())\nprint(f())",
     "q": "ما المشكلة الشهيرة في هذا الكود؟",
     "options": ["يطبع [1] مرتين", "يطبع [1] ثم [1, 1]",
                 "يطبع [1, 1] مرتين", "يطبع [1] ثم [1]"],
     "answer": "يطبع [1] ثم [1, 1]",
     "explain": "المعامل الافتراضي يُنشأ مرة واحدة ويُشار إليه"},

    {"code": "print(2 ** 3 ** 1)",
     "q": "ما ناتج العملية؟ (انتبه للأسبقية)",
     "options": ["64", "8", "9", "6"], "answer": "8",
     "explain": "** يُقيّم من اليمين لليسار: 2 ** (3 ** 1) = 8"},

    {"code": "x = 10\ndef f():\n    global x\n    x += 5\nf()\nprint(x)",
     "q": "ما قيمة x بعد التنفيذ؟",
     "options": ["10", "5", "15", "Error"], "answer": "15",
     "explain": "global تسمح بتعديل المتغير الخارجي"},

    {"code": "d = {'a': 1, 'b': 2}\nprint(d.get('c', 3))",
     "q": "ما ناتج get عند غياب المفتاح؟",
     "options": ["None", "3", "KeyError", "0"], "answer": "3",
     "explain": "القيمة الافتراضية الثانية تُعاد عند غياب المفتاح"},

    {"code": "t = (1, 2, 3)\nt[0] = 10",
     "q": "ماذا يحدث عند تنفيذ هذا الكود؟",
     "options": ["t تصبح (10, 2, 3)", "TypeError",
                 "t تصبح [10, 2, 3]", "لا شيء"], "answer": "TypeError",
     "explain": "الـ tuple غير قابلة للتعديل (immutable)"},

    {"code": "print(list(range(3, 10, 3)))",
     "q": "ما ناتج الكود؟",
     "options": ["[3, 6, 9]", "[3, 6, 9, 10]", "[3, 6]", "[4, 7, 10]"],
     "answer": "[3, 6, 9]",
     "explain": "يبدأ من 3 بخطوة 3 والنهاية 10 غير شاملة"},

    {"code": "a = [1, 2, 3]\nprint(a[-1] + a[0])",
     "q": "ما ناتج الكود؟",
     "options": ["3", "4", "2", "Error"], "answer": "4",
     "explain": "a[-1] هو آخر عنصر = 3، و a[0] = 1"},

    {"code": "s = 'Code Quest'\nprint(s.split()[1])",
     "q": "ما ناتج split()[1]؟",
     "options": ["Code", "Quest", "'Quest'", "C"], "answer": "Quest",
     "explain": "split() تقسم على المسافة و [1] تأخذ الكلمة الثانية"},

    {"code": "print(10 == '10')",
     "q": "مقارنة رقم مع نص - النتيجة؟",
     "options": ["True", "False", "Error", "10"], "answer": "False",
     "explain": "int 10 لا يساوي str '10' في بايثون 3"},

    {"code": "nums = [1, 2, 3, 4]\nprint([n*n for n in nums if n % 2 == 0])",
     "q": "ما ناتج List Comprehension؟",
     "options": ["[1, 4, 9, 16]", "[4, 16]", "[2, 4]", "[4]"], "answer": "[4, 16]",
     "explain": "الأعداد الزوجية فقط (2 و4) تُربَّع"},

    {"code": "def f(a, b=2, c=3):\n    return a * b + c\nprint(f(2, c=5))",
     "q": "ما ناتج الاستدعاء؟",
     "options": ["9", "13", "7", "15"], "answer": "9",
     "explain": "a=2, b=2 (افتراضي), c=5 → 2*2+5 = 9"},

    {"code": "x = '5' * 3\nprint(x)",
     "q": "ضرب نص في رقم - النتيجة؟",
     "options": ["15", "555", "'15'", "Error"], "answer": "555",
     "explain": "تكرار النص 3 مرات: '5'+'5'+'5'"},

    {"code": "print(0.1 + 0.2 == 0.3)",
     "q": "السؤال الشهير عن الفاصلة العائمة!",
     "options": ["True", "False", "0.3", "Error"], "answer": "False",
     "explain": "0.1+0.2 = 0.30000000000000004 بسبب تمثيل float"},

    {"code": "d = {'x': 1}\nd.update({'y': 2})\nprint(len(d))",
     "q": "ما طول القاموس بعد update؟",
     "options": ["1", "2", "3", "Error"], "answer": "2",
     "explain": "update أضاف مفتاح y، فالمجموع مفتاحان"},

    {"code": "try:\n    x = 1 / 0\nexcept ZeroDivisionError:\n    print('caught')",
     "q": "ما الذي سيطبع؟",
     "options": ["caught", "Error غير معالج", "0", "inf"], "answer": "caught",
     "explain": "الاستثناء ZeroDivisionError تم التقاطه بنجاح"},

    {"code": "print(type(()))",
     "q": "ما نوع القوسين الفارغين ()؟",
     "options": ["list", "dict", "tuple", "set"], "answer": "tuple",
     "explain": "القوسان المستديران يعرّفان tuple فارغة"},
]
