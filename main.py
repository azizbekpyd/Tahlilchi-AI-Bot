import os
import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

# Environment variables ni yuklash
load_dotenv()

# Logging sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Bot token va dispatcher
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable topilmadi!")

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Admin ID
ADMIN_ID = os.getenv('ADMIN_ID')
if ADMIN_ID:
    try:
        ADMIN_ID = int(ADMIN_ID)
    except ValueError:
        ADMIN_ID = None
        logger.warning("ADMIN_ID noto'g'ri formatda. Butun son bo'lishi kerak.")

# File ID larni saqlash uchun JSON fayl
FILE_IDS_JSON = 'file_ids.json'


# FSM holatlari
class UserState(StatesGroup):
    waiting_for_pos_answer = State()


class AdminState(StatesGroup):
    waiting_for_pos_yes_file = State()
    waiting_for_pos_no_file = State()


# Yordamchi funksiyalar
def is_admin(user_id: int) -> bool:
    """Foydalanuvchi admin ekanligini tekshirish"""
    if not ADMIN_ID:
        return False
    return user_id == ADMIN_ID


def load_file_ids() -> dict:
    """File ID larni JSON fayldan yuklash"""
    if os.path.exists(FILE_IDS_JSON):
        try:
            with open(FILE_IDS_JSON, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"File ID larni yuklashda xatolik: {e}")
            return {}
    return {}


def save_file_id(file_type: str, file_id: str):
    """File ID ni JSON faylga saqlash"""
    file_ids = load_file_ids()
    file_ids[file_type] = file_id
    try:
        with open(FILE_IDS_JSON, 'w', encoding='utf-8') as f:
            json.dump(file_ids, f, indent=2, ensure_ascii=False)
        logger.info(f"File ID saqlandi: {file_type} = {file_id}")
        return True
    except Exception as e:
        logger.error(f"File ID ni saqlashda xatolik: {e}")
        return False


def get_file_id(file_type: str) -> str:
    """File ID ni olish (avval JSON dan, keyin .env dan)"""
    # Avval JSON fayldan
    file_ids = load_file_ids()
    if file_type in file_ids:
        return file_ids[file_type]
    
    # Keyin .env dan
    env_key = f'{file_type.upper()}_FILE_ID'
    return os.getenv(env_key, '')


# Inline klaviatura yaratish
def get_pos_keyboard():
    """POS sistemasi haqida savol uchun klaviatura"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Ha", callback_data="pos_yes"),
            InlineKeyboardButton(text="❌ Yo'q", callback_data="pos_no")
        ]
    ])
    return keyboard


# /start buyrug'i
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    """Botni boshlash va xush kelibsiz xabari"""
    user_name = message.from_user.first_name or "Foydalanuvchi"
    
    welcome_text = (
        f"Assalomu alaykum, {user_name}!\n\n"
        "Bizning dasturni yuklab olish uchun, iltimos, javob bering:\n\n"
        "❓ <b>Sizda POS sistemasi bormi?</b>"
    )
    
    await message.answer(
        welcome_text,
        reply_markup=get_pos_keyboard(),
        parse_mode="HTML"
    )
    
    # Foydalanuvchi holatini belgilash
    await state.set_state(UserState.waiting_for_pos_answer)
    logger.info(f"Foydalanuvchi {message.from_user.id} botni boshladi")


# POS sistemasi haqida javoblar
@dp.callback_query(lambda c: c.data in ["pos_yes", "pos_no"])
async def handle_pos_answer(callback: types.CallbackQuery, state: FSMContext):
    """POS sistemasi haqida javobni qayta ishlash"""
    await callback.answer()
    
    user_id = callback.from_user.id
    
    if callback.data == "pos_yes":
        # POS sistemasi bor
        await callback.message.edit_text(
            "✅ Rahmat! Sizning javobingiz qabul qilindi.\n\n"
            "POS tizimi mavjud bo'lgan do'konlar uchun mo'ljallangan dastur yuborilmoqda..."
        )
        
        # File ID ni olish (avval JSON dan, keyin .env dan)
        pos_file_id = get_file_id('pos_yes')
        
        if pos_file_id:
            # File_id orqali fayl yuborish (tezroq)
            await callback.message.answer_document(
                document=pos_file_id,
                caption="📦 POS tizimi mavjud bo'lgan do'konlar uchun dastur"
            )
        else:
            # Agar file_id bo'lmasa, fayl yo'lini ko'rsating
            pos_file_path = os.getenv('POS_YES_FILE_PATH', 'pos_yes.zip')
            if os.path.exists(pos_file_path):
                await callback.message.answer_document(
                    document=types.FSInputFile(pos_file_path),
                    caption="📦 POS tizimi mavjud bo'lgan do'konlar uchun dastur"
                )
            else:
                await callback.message.answer(
                    "⚠️ Kechirasiz, fayl hozircha mavjud emas. "
                    "Iltimos, administrator bilan bog'laning."
                )
        
        logger.info(f"Foydalanuvchi {user_id} 'Ha' javobini berdi")
        
    elif callback.data == "pos_no":
        # POS sistemasi yo'q
        await callback.message.edit_text(
            "✅ Rahmat! Sizning javobingiz qabul qilindi.\n\n"
            "POS tizimi mavjud bo'lmagan do'konlar uchun mo'ljallangan dastur yuborilmoqda..."
        )
        
        # File ID ni olish (avval JSON dan, keyin .env dan)
        pos_no_file_id = get_file_id('pos_no')
        
        if pos_no_file_id:
            # File_id orqali fayl yuborish (tezroq)
            await callback.message.answer_document(
                document=pos_no_file_id,
                caption="📦 POS tizimi mavjud bo'lmagan do'konlar uchun dastur"
            )
        else:
            # Agar file_id bo'lmasa, fayl yo'lini ko'rsating
            pos_no_file_path = os.getenv('POS_NO_FILE_PATH', 'pos_no.zip')
            if os.path.exists(pos_no_file_path):
                await callback.message.answer_document(
                    document=types.FSInputFile(pos_no_file_path),
                    caption="📦 POS tizimi mavjud bo'lmagan do'konlar uchun dastur"
                )
            else:
                await callback.message.answer(
                    "⚠️ Kechirasiz, fayl hozircha mavjud emas. "
                    "Iltimos, administrator bilan bog'laning."
                )
        
        logger.info(f"Foydalanuvchi {user_id} 'Yo'q' javobini berdi")
    
    # Holatni tozalash
    await state.clear()


# Admin buyruqlari
@dp.message(Command("admin"))
async def cmd_admin(message: types.Message):
    """Admin panel"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda admin huquqi yo'q!")
        return
    
    admin_text = (
        "👨‍💼 <b>Admin Panel</b>\n\n"
        "Quyidagi buyruqlardan foydalaning:\n\n"
        "/set_pos_yes - POS bor bo'lganlar uchun fayl yuborish\n"
        "/set_pos_no - POS yo'q bo'lganlar uchun fayl yuborish\n"
        "/file_ids - Hozirgi file ID larni ko'rish\n\n"
        "Yoki to'g'ridan-to'g'ri ZIP faylni yuboring va bot uni qabul qiladi."
    )
    
    await message.answer(admin_text, parse_mode="HTML")


@dp.message(Command("set_pos_yes"))
async def cmd_set_pos_yes(message: types.Message, state: FSMContext):
    """POS YES faylini o'rnatish"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda admin huquqi yo'q!")
        return
    
    await message.answer(
        "📤 Iltimos, POS sistemasi bor bo'lgan do'konlar uchun ZIP faylni yuboring:"
    )
    await state.set_state(AdminState.waiting_for_pos_yes_file)


@dp.message(Command("set_pos_no"))
async def cmd_set_pos_no(message: types.Message, state: FSMContext):
    """POS NO faylini o'rnatish"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda admin huquqi yo'q!")
        return
    
    await message.answer(
        "📤 Iltimos, POS sistemasi yo'q bo'lgan do'konlar uchun ZIP faylni yuboring:"
    )
    await state.set_state(AdminState.waiting_for_pos_no_file)


@dp.message(Command("file_ids"))
async def cmd_file_ids(message: types.Message):
    """Hozirgi file ID larni ko'rish"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda admin huquqi yo'q!")
        return
    
    file_ids = load_file_ids()
    pos_yes_id = file_ids.get('pos_yes', 'Mavjud emas')
    pos_no_id = file_ids.get('pos_no', 'Mavjud emas')
    
    info_text = (
        "📋 <b>Hozirgi File ID lar:</b>\n\n"
        f"<b>POS YES:</b> <code>{pos_yes_id}</code>\n"
        f"<b>POS NO:</b> <code>{pos_no_id}</code>\n\n"
        "Yangi fayl yuborish uchun /set_pos_yes yoki /set_pos_no buyrug'laridan foydalaning."
    )
    
    await message.answer(info_text, parse_mode="HTML")


# Admin fayl yuborish
@dp.message(lambda m: m.document and is_admin(m.from_user.id))
async def handle_admin_document(message: types.Message, state: FSMContext):
    """Admin fayl yuborganda"""
    current_state = await state.get_state()
    
    if current_state == AdminState.waiting_for_pos_yes_file:
        # POS YES fayl
        file_id = message.document.file_id
        file_name = message.document.file_name or "Noma'lum"
        
        if save_file_id('pos_yes', file_id):
            await message.answer(
                f"✅ <b>Muvaffaqiyatli saqlandi!</b>\n\n"
                f"📁 Fayl: {file_name}\n"
                f"🆔 File ID: <code>{file_id}</code>\n\n"
                f"Endi foydalanuvchilar 'Ha' javobini berganida bu fayl yuboriladi.",
                parse_mode="HTML"
            )
        else:
            await message.answer("❌ File ID ni saqlashda xatolik yuz berdi!")
        
        await state.clear()
        
    elif current_state == AdminState.waiting_for_pos_no_file:
        # POS NO fayl
        file_id = message.document.file_id
        file_name = message.document.file_name or "Noma'lum"
        
        if save_file_id('pos_no', file_id):
            await message.answer(
                f"✅ <b>Muvaffaqiyatli saqlandi!</b>\n\n"
                f"📁 Fayl: {file_name}\n"
                f"🆔 File ID: <code>{file_id}</code>\n\n"
                f"Endi foydalanuvchilar 'Yo'q' javobini berganida bu fayl yuboriladi.",
                parse_mode="HTML"
            )
        else:
            await message.answer("❌ File ID ni saqlashda xatolik yuz berdi!")
        
        await state.clear()
    
    else:
        # Holat bo'lmasa, admin panelni ko'rsatish
        await message.answer(
            "📤 Fayl qabul qilindi!\n\n"
            "Faylni saqlash uchun quyidagi buyruqlardan birini yuboring:\n"
            "/set_pos_yes - POS bor bo'lganlar uchun\n"
            "/set_pos_no - POS yo'q bo'lganlar uchun"
        )


# Boshqa xabarlarni qayta ishlash
@dp.message()
async def handle_other_messages(message: types.Message, state: FSMContext):
    """Boshqa xabarlarni qayta ishlash"""
    current_state = await state.get_state()
    
    if current_state == UserState.waiting_for_pos_answer:
        # Agar foydalanuvchi holatda bo'lsa, klaviaturadan foydalanishni eslatish
        await message.answer(
            "Iltimos, quyidagi tugmalardan birini tanlang:",
            reply_markup=get_pos_keyboard()
        )
    elif current_state in [AdminState.waiting_for_pos_yes_file, AdminState.waiting_for_pos_no_file]:
        # Admin holatda bo'lsa, fayl kutish
        await message.answer(
            "⏳ ZIP fayl kutilyapti. Iltimos, ZIP faylni yuboring yoki /admin buyrug'i bilan bekor qiling."
        )
    else:
        # Agar holat bo'lmasa, /start buyrug'ini eslatish
        await message.answer(
            "Botni qayta boshlash uchun /start buyrug'ini yuboring."
        )


# Botni ishga tushirish
async def main():
    """Botni ishga tushirish"""
    logger.info("Bot ishga tushmoqda...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Xatolik yuz berdi: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

