from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from utils.translator import translate_text
from keyboards.lang_kb import get_lang_keyboard

router = Router()

# -----------------------------------------------------------
# Foydalanuvchilar sozlamalari xotirasi
# Kalit: user_id (son), Qiymat: lug'at {"source": ..., "target": ...}
# -----------------------------------------------------------
user_settings: dict[int, dict] = {}


def get_user_langs(user_id: int) -> tuple[str, str]:
    """Foydalanuvchining til juftligini qaytaradi (source, target)"""
    settings = user_settings.get(user_id, {"source": "ru", "target": "en"})
    return settings["source"], settings["target"]


# Chiroyli chiqish uchun til nomlari
LANG_NAMES = {
    "ru": "🇷🇺 Ruscha",
    "en": "🇬🇧 Inglizcha",
    "uz": "🇺🇿 O'zbekcha",
    "auto": "🔄 Avto aniqlash",
}


# -----------------------------------------------------------
# Handler: /start
# -----------------------------------------------------------
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "👋 Salom! Men tarjimon-botman.\n\n"
        "Avval tarjima yo'nalishini tanlang, keyin matn yuboring.\n\n"
        "📌 Buyruqlar:\n"
        "/start — bu xabarni ko'rsatish\n"
        "/lang — tarjima tillarini tanlash\n"
        "/current — hozirgi til juftligi\n\n"
        "Standart holat: 🇷🇺 Ruscha → 🇬🇧 Inglizcha",
        reply_markup=get_lang_keyboard()
    )


# -----------------------------------------------------------
# Handler: /lang — til tanlash klaviaturasini ko'rsatish
# -----------------------------------------------------------
@router.message(Command("lang"))
async def cmd_lang(message: Message):
    await message.answer(
        "🌍 Tarjima uchun til juftligini tanlang:",
        reply_markup=get_lang_keyboard()
    )


# -----------------------------------------------------------
# Handler: /current — hozirgi sozlamalarni ko'rsatish
# -----------------------------------------------------------
@router.message(Command("current"))
async def cmd_current(message: Message):
    source, target = get_user_langs(message.from_user.id)
    source_name = LANG_NAMES.get(source, source)
    target_name = LANG_NAMES.get(target, target)
    
    await message.answer(
        f"⚙️ Hozirgi sozlama:\n\n"
        f"Tarjima: {source_name} → {target_name}\n\n"
        f"O'zgartirish uchun — /lang"
    )


# -----------------------------------------------------------
# Handler: til tanlash tugmasi bosilganda
# F.data.startswith("lang:") — filtr: faqat bizning tugmalarni ushlaymiz
# -----------------------------------------------------------
@router.callback_query(F.data.startswith("lang:"))
async def on_lang_chosen(callback: CallbackQuery):
    # callback_data ni ajratamiz: "lang:ru:en" → ["lang", "ru", "en"]
    parts = callback.data.split(":")
    source = parts[1]   # "ru"
    target = parts[2]   # "en"
    
    # Foydalanuvchi tanlovini saqlaymiz
    user_settings[callback.from_user.id] = {
        "source": source,
        "target": target
    }
    
    source_name = LANG_NAMES.get(source, source)
    target_name = LANG_NAMES.get(target, target)
    
    # Foydalanuvchiga javob beramiz (tugmadagi "soatcha"ni olib tashlaymiz)
    await callback.answer(f"✅ Tanlandi: {source_name} → {target_name}")
    
    # Asl xabarni tahrirlaymiz
    await callback.message.edit_text(
        f"✅ Til juftligi o'zgartirildi!\n\n"
        f"Endi tarjima qilaman: {source_name} → {target_name}\n\n"
        f"Menga biror matn yuboring 👇"
    )


# -----------------------------------------------------------
# Handler: har qanday matnli xabar → tarjima
# MUHIM: bu handler eng OXIRIDA bo'lishi kerak!
# -----------------------------------------------------------
@router.message()
async def handle_text(message: Message):
    # Bo'sh va buyruqlarni e'tiborsiz qoldiramiz
    if not message.text or message.text.startswith("/"):
        return
    
    # Foydalanuvchining til juftligini olamiz
    source, target = get_user_langs(message.from_user.id)
    
    # Tarjima qilamiz
    result = translate_text(
        text=message.text,
        source=source,
        target=target
    )
    
    source_name = LANG_NAMES.get(source, source)
    target_name = LANG_NAMES.get(target, target)
    
    # Natijani yuboramiz
    await message.answer(
        f"🔄 {source_name} → {target_name}\n\n"
        f"{result}"
    )
