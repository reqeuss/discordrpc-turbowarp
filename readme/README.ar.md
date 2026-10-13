# Discord Rich Presence لـ TurboWarp

أضف Discord Rich Presence إلى لعبة TurboWarp باستخدام إضافة مخصّصة وbridge محلي.

**مهم:** يجب دمج الإضافة في مشروع TurboWarp أثناء التطوير، **قبل تصدير اللعبة أو تجميعها**. لا يستطيع هذا المشروع إضافة RPC تلقائيًا إلى لعبة مُصدّرة مسبقًا لم تتضمن الإضافة.

[Français](README.fr.md) · [English](README.en.md) · [Español](README.es.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [한국어](README.ko.md) · [Deutsch](README.de.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md) · [Italiano](README.it.md)

## الميزات
- تخصيص تفاصيل حالة Discord والنصوص وأوقات البداية والنهاية.
- دعم صور Discord ومعلومات المجموعة وأسرار Join/Spectate وعلامة الجلسة.
- إعادة الاتصال تلقائيًا عند انقطاع bridge مؤقتًا.
- استخدام WebSocket محلي على `127.0.0.1:32123`.
- تشغيل اللعبة على Windows عبر `game.bat`.
- يمكن استخدام `rpc_bridge.exe` مُجمّع لتجنّب مطالبة اللاعب بتثبيت Python.

## التثبيت والإعداد
1. أثناء التطوير، حمّل `extension.js` في TurboWarp كإضافة مخصّصة **unsandboxed** واستخدم كتلها في المشروع.
2. صدّر اللعبة أو جمّعها بعد تضمين الإضافة.
3. أنشئ تطبيقًا في [Discord Developer Portal](https://discord.com/developers/applications) وانسخ Application ID.
4. ضع المعرّف الرقمي في `APP_ID` داخل `resources/rpc/rpc_bridge.py`. لا تضع bot token أو client secret.
5. انسخ محتويات `ingame/` إلى جانب الملف التنفيذي للعبة.
6. على Windows شغّل `game.bat`. يبحث bridge افتراضيًا عن `testdiscordrpc.exe`؛ عدّل `GAME_EXE` إذا كان اسم الملف مختلفًا.

يبحث البرنامج أولًا عن `resources/rpc/rpc_bridge.exe`. إن لم يجده، يبحث عن Python 3 ويثبّت الاعتماديات عند التشغيل الأول. اضبط Application ID قبل تجميع bridge. يجب أن يكون تطبيق Discord لسطح المكتب مفتوحًا ومسجّل الدخول.

## كتل الإضافة
- **set [field] to [value]** — ضبط حقل النشاط.
- **update presence** — إرسال النشاط إلى Discord.
- **clear presence** — مسح النشاط.
- **reconnect to bridge** — إعادة محاولة الاتصال.
- **RPC connection status** — عرض حالة الاتصال وآخر خطأ.
- **current value of [field]** — قراءة القيمة الحالية للحقل.

تُستخدم ثواني Unix للطوابع الزمنية، وليس المللي ثانية. تستخدم حقول الصور مفاتيح الأصول من Discord Developer Portal، وليس روابط الصور.

## استكشاف الأخطاء
- لا يوجد اتصال: تأكد من تشغيل bridge وتحميل الإضافة بوضع unsandboxed.
- لا يظهر النشاط: تحقق من تطبيق Discord لسطح المكتب ومن Application ID.
- الصور لا تظهر: تحقق من مفاتيح Rich Presence.
- فتح `http://127.0.0.1:32123/` في المتصفح ليس اختبارًا صحيحًا؛ فالواجهة تتوقع اتصال WebSocket.

## النسبة إلى صاحب المشروع
إذا استخدمت هذا المشروع أو أعدت توزيعه أو عدّلته في لعبة أو مشروع آخر، **يرجى ذكر Reqeuss وإضافة رابط المستودع**:

> [Discord RPC for TurboWarp](https://github.com/reqeuss/discordrpc-turbowarp) by Reqeuss

يرجى الاحتفاظ بالذكر عند إعادة توزيع النسخ المعدّلة. لا يحل هذا الطلب محل شروط تراخيص الجهات الخارجية السارية.

## الأمان
يستمع bridge فقط على `127.0.0.1` المحلي. لا تكشفه لأجهزة أخرى ما لم تفهم المخاطر.
