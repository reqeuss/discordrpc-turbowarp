# TurboWarp के लिए Discord Rich Presence

कस्टम एक्सटेंशन और लोकल bridge की मदद से TurboWarp गेम में Discord Rich Presence जोड़ें।

**ज़रूरी बात:** गेम को export या compile करने से **पहले**, डेवलपमेंट के दौरान एक्सटेंशन को TurboWarp प्रोजेक्ट में शामिल करना आवश्यक है। यह प्रोजेक्ट ऐसे पहले से export किए गए गेम में अपने-आप RPC नहीं जोड़ सकता जिसमें एक्सटेंशन शामिल नहीं था।

[Français](README.fr.md) · [English](README.en.md) · [Español](README.es.md) · [日本語](README.ja.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [한국어](README.ko.md) · [Deutsch](README.de.md) · [Português](README.pt-BR.md) · [Русский](README.ru.md) · [العربية](README.ar.md) · [हिन्दी](README.hi.md) · [Italiano](README.it.md)

## सुविधाएँ
- Discord गतिविधि का विवरण, स्थिति और समय अनुकूलित करें।
- Discord इमेज एसेट, पार्टी जानकारी, Join/Spectate secrets और instance flag का समर्थन।
- bridge अस्थायी रूप से डिस्कनेक्ट होने पर अपने-आप फिर जुड़ता है।
- लोकल WebSocket `127.0.0.1:32123` पर चलता है।
- Windows में `game.bat` से शुरू करें।
- कंपाइल किया हुआ `rpc_bridge.exe` इस्तेमाल करके खिलाड़ी के PC पर Python की आवश्यकता हटाई जा सकती है।

## इंस्टॉलेशन
1. डेवलपमेंट के दौरान `extension.js` को TurboWarp में कस्टम **unsandboxed** एक्सटेंशन के रूप में लोड करें और प्रोजेक्ट में उसके blocks इस्तेमाल करें।
2. एक्सटेंशन शामिल होने के बाद गेम export या compile करें।
3. [Discord Developer Portal](https://discord.com/developers/applications) में ऐप बनाएँ और Application ID कॉपी करें।
4. `resources/rpc/rpc_bridge.py` में `APP_ID` को अपने numeric ID से बदलें। bot token या client secret न डालें।
5. `ingame/` की सामग्री गेम executable के पास कॉपी करें।
6. Windows में `game.bat` चलाएँ। bridge डिफ़ॉल्ट रूप से `testdiscordrpc.exe` खोजता है; नाम अलग हो तो `GAME_EXE` बदलें।

स्क्रिप्ट पहले `resources/rpc/rpc_bridge.exe` खोजती है। वह न मिले तो Python 3 खोजकर पहली बार dependencies इंस्टॉल करती है। bridge compile करने से पहले Application ID सेट करें। Discord Desktop ऐप चालू और लॉग-इन होना चाहिए।

## एक्सटेंशन blocks
- **set [field] to [value]** — गतिविधि फ़ील्ड सेट करें।
- **update presence** — Discord को गतिविधि भेजें।
- **clear presence** — गतिविधि हटाएँ।
- **reconnect to bridge** — दोबारा कनेक्ट करें।
- **RPC connection status** — कनेक्शन स्थिति और पिछली त्रुटि देखें।
- **current value of [field]** — फ़ील्ड की मौजूदा वैल्यू पढ़ें।

टाइमस्टैम्प Unix seconds में होते हैं, milliseconds में नहीं। इमेज फ़ील्ड में Discord Developer Portal की asset keys इस्तेमाल करें, image URLs नहीं।

## समस्या निवारण
- कनेक्शन नहीं है: bridge चल रहा हो और एक्सटेंशन unsandboxed मोड में लोड हो, यह जाँचें।
- गतिविधि नहीं दिखती: Discord Desktop और Application ID जाँचें।
- इमेज नहीं दिखती: Rich Presence asset keys जाँचें।
- ब्राउज़र में `http://127.0.0.1:32123/` खोलना सही परीक्षण नहीं है; यह WebSocket endpoint है।

## क्रेडिट और उपयोग
यदि आप इस प्रोजेक्ट का उपयोग, पुनर्वितरण या संशोधन करते हैं, तो **Reqeuss को क्रेडिट दें और इस repository का लिंक शामिल करें**:

> [Discord RPC for TurboWarp](https://github.com/reqeuss/discordrpc-turbowarp) by Reqeuss

संशोधित संस्करण बाँटते समय भी क्रेडिट बनाए रखें। यह अनुरोध लागू third-party license शर्तों का स्थान नहीं लेता।

## सुरक्षा
bridge केवल लोकल `127.0.0.1` पर सुनता है। जोखिम समझे बिना इसे दूसरे डिवाइसों के लिए उपलब्ध न करें।
