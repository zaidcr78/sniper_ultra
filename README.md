# INFR — Discord Username Checker

أداة ويب لتوليد وفحص توفر أسماء المستخدمين في ديسكورد.

## المميزات

- توليد أسماء 4L (4 حروف + `.` أو `_` في مواضع مختلفة).
- فحص التوفر عبر نقطة النهاية الرسمية `pomelo-attempt`.
- واجهة ويب بإحصائيات حية.
- وضع آمن: توكن واحد، 10 أسماء، تأخير 10–20 ثانية.

## الأمان

**التوكنات لا تُخزَّن في الكود.** تُحمَّل من متغير البيئة `TOKENS`:

- `TOKENS` — قائمة توكنات مفصولة بفواصل.

**البروكسيات مكتوبة داخل الكود** في `CONFIG["proxies"]`.

## النشر على Render

1. ارفع الملفات على GitHub.
2. أنشئ Web Service على render.com.
3. الإعداد:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
4. أضف متغير البيئة:
   - `TOKENS` = `token1,token2,token3`
5. Deploy.

## التشغيل المحلي

```bash
pip install -r requirements.txt
export TOKENS="token1,token2"
python app.py
