"""
Yordamchi skript: Fayl yuborib, file_id ni olish uchun
Bu skriptni birinchi marta fayllarni yuklaganda ishlatishingiz mumkin
"""
import os
import asyncio
from aiogram import Bot, types
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable topilmadi!")

bot = Bot(token=BOT_TOKEN)


async def get_file_id(file_path: str, caption: str = ""):
    """
    Faylni yuborib, file_id ni olish
    
    Args:
        file_path: Yuboriladigan fayl yo'li
        caption: Fayl uchun izoh
    """
    if not os.path.exists(file_path):
        print(f"❌ Xatolik: {file_path} fayli topilmadi!")
        return None
    
    try:
        # O'zingizning chat ID ni kiriting (o'zingizga xabar yuborish uchun)
        # Chat ID ni olish uchun @userinfobot ga murojaat qiling
        YOUR_CHAT_ID = os.getenv('YOUR_CHAT_ID')
        
        if not YOUR_CHAT_ID:
            print("⚠️ Eslatma: YOUR_CHAT_ID ni .env faylida belgilang")
            print("   Chat ID ni olish uchun @userinfobot ga murojaat qiling")
            YOUR_CHAT_ID = input("Yoki chat ID ni shu yerga kiriting: ")
        
        # Faylni yuborish
        print(f"📤 {file_path} fayli yuborilmoqda...")
        message = await bot.send_document(
            chat_id=YOUR_CHAT_ID,
            document=types.FSInputFile(file_path),
            caption=caption
        )
        
        # File ID ni olish
        file_id = message.document.file_id
        print(f"\n✅ Muvaffaqiyatli!")
        print(f"📁 Fayl: {file_path}")
        print(f"🆔 File ID: {file_id}")
        print(f"\n💡 Bu file_id ni .env faylida quyidagicha qo'ying:")
        print(f"   POS_YES_FILE_ID={file_id}" if 'yes' in file_path.lower() else f"   POS_NO_FILE_ID={file_id}")
        
        return file_id
        
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        return None
    finally:
        await bot.session.close()


async def main():
    """Asosiy funksiya"""
    print("=" * 50)
    print("📦 File ID olish dasturi")
    print("=" * 50)
    print("\nQaysi fayl uchun file_id olishni xohlaysiz?")
    print("1. POS YES (pos_yes.zip)")
    print("2. POS NO (pos_no.zip)")
    print("3. Boshqa fayl")
    
    choice = input("\nTanlov (1/2/3): ").strip()
    
    if choice == "1":
        file_path = os.getenv('POS_YES_FILE_PATH', 'pos_yes.zip')
        caption = "POS tizimi mavjud bo'lgan do'konlar uchun dastur"
    elif choice == "2":
        file_path = os.getenv('POS_NO_FILE_PATH', 'pos_no.zip')
        caption = "POS tizimi mavjud bo'lmagan do'konlar uchun dastur"
    elif choice == "3":
        file_path = input("Fayl yo'lini kiriting: ").strip()
        caption = input("Izoh (ixtiyoriy): ").strip()
    else:
        print("❌ Noto'g'ri tanlov!")
        return
    
    await get_file_id(file_path, caption)


if __name__ == "__main__":
    asyncio.run(main())

