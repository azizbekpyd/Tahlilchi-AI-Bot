# Tahlilchi AI Bot - POS Sistemasi So'rov Boti

Bu bot marketing sayt orqali kelgan foydalanuvchilarga POS sistemasi bor-yo'qligini so'raydi va mos dasturni yuboradi.

## 🚀 O'rnatish

### 1. Kerakli kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 2. Bot Token olish

1. Telegram'da [@BotFather](https://t.me/BotFather) ga murojaat qiling
2. `/newbot` buyrug'ini yuboring
3. Bot nomi va username ni kiriting
4. Olingan token ni saqlang

### 3. Konfiguratsiya

`.env.example` faylini `.env` ga ko'chiring va o'z ma'lumotlaringizni kiriting:

```bash
cp .env.example .env
```

`.env` faylini ochib, `BOT_TOKEN` va `ADMIN_ID` ni kiriting:

```
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_telegram_id_here
```

**Admin ID ni olish:** [@userinfobot](https://t.me/userinfobot) ga murojaat qiling

### 4. Fayllarni tayyorlash

Ikkita ZIP fayl tayyorlang:
- `pos_yes.zip` - POS sistemasi bor bo'lgan do'konlar uchun
- `pos_no.zip` - POS sistemasi yo'q bo'lgan do'konlar uchun

## 📁 Fayl ID olish (Tavsiya etiladi)

Telegram serverida fayllarni saqlash va tezroq yuborish uchun:

### Usul 1: Admin Panel orqali (Eng qulay - Tavsiya etiladi)

1. Botni ishga tushiring
2. Botga `/admin` buyrug'ini yuboring
3. `/set_pos_yes` yoki `/set_pos_no` buyrug'ini yuboring
4. ZIP faylni yuboring
5. File ID avtomatik saqlanadi va bot foydalanuvchilarga yuboradi

**Afzalliklari:**
- Faylni to'g'ridan-to'g'ri botga yuborishingiz mumkin
- File ID avtomatik saqlanadi (`file_ids.json`)
- Qo'shimcha skriptlar kerak emas

### Usul 2: Yordamchi skriptdan foydalanish

1. Chat ID ni olish uchun [@userinfobot](https://t.me/userinfobot) ga murojaat qiling
2. `.env` faylida `YOUR_CHAT_ID` ni qo'ying (yoki skript ishga tushganda so'raladi)
3. `get_file_id.py` skriptini ishga tushiring:

```bash
python get_file_id.py
```

4. Skript sizga file_id ni ko'rsatadi va uni `.env` faylida qo'yishingiz kerak

### Usul 3: Qo'lda olish

1. Birinchi marta botni ishga tushiring
2. Bot orqali faylni yuboring (file_path orqali)
3. Bot loglarida yoki kodda `file_id` ni toping
4. `.env` faylida `POS_YES_FILE_ID` va `POS_NO_FILE_ID` ga qo'ying

**Misol:**
```python
# Birinchi marta fayl yuborilganda, file_id ni olish
file_id = message.document.file_id
print(f"File ID: {file_id}")
```

Keyin `.env` faylida:
```
POS_YES_FILE_ID=BAACAgIAAxkBAAIBY2...
POS_NO_FILE_ID=BAACAgIAAxkBAAIBY3...
```

## 🏃 Botni ishga tushirish

```bash
python main.py
```

## 📋 Botning ishlash prinsipi

1. Foydalanuvchi `/start` buyrug'ini yuboradi
2. Bot xush kelibsiz xabarini va POS sistemasi haqida savolni yuboradi
3. Foydalanuvchi "Ha" yoki "Yo'q" tugmasini bosadi
4. Bot mos ZIP faylni yuboradi

## 👨‍💼 Admin Funksiyalari

Botda admin panel mavjud. Admin sifatida quyidagi buyruqlardan foydalanishingiz mumkin:

- `/admin` - Admin panelni ochish
- `/set_pos_yes` - POS bor bo'lganlar uchun fayl yuborish
- `/set_pos_no` - POS yo'q bo'lganlar uchun fayl yuborish
- `/file_ids` - Hozirgi file ID larni ko'rish

**Qanday ishlaydi:**
1. `/set_pos_yes` yoki `/set_pos_no` buyrug'ini yuboring
2. Bot sizdan ZIP fayl kutadi
3. ZIP faylni yuboring
4. Bot file_id ni avtomatik saqlaydi (`file_ids.json` faylga)
5. Endi foydalanuvchilar javob berganida bu fayl yuboriladi

**Eslatma:** Admin ID `.env` faylida `ADMIN_ID` o'zgaruvchisida belgilanishi kerak.

## 🔧 Sozlash

### Fayl yo'llarini o'zgartirish

`.env` faylida `POS_YES_FILE_PATH` va `POS_NO_FILE_PATH` ni o'zgartiring.

### Xabarlarni o'zgartirish

`main.py` faylida xabar matnlarini o'zgartiring.

## 📝 Eslatmalar

- Bot token ni hech qachon GitHub ga yuklamang
- `.env` faylini `.gitignore` ga qo'shing
- Fayl ID dan foydalanish tezroq ishlaydi va server resurslarini tejaydi

## 🐛 Muammolarni hal qilish

**Bot ishlamayapti:**
- `.env` faylida `BOT_TOKEN` to'g'ri kirilganligini tekshiring
- Internet ulanishini tekshiring

**Fayl yuborilmayapti:**
- Fayl yo'llarini tekshiring
- Fayl mavjudligini tekshiring
- File ID to'g'ri kirilganligini tekshiring

## 📞 Yordam

Muammo bo'lsa, administrator bilan bog'laning.

