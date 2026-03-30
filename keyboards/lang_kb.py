from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_lang_keyboard() -> InlineKeyboardMarkup:
    """Til juftligini tanlash klaviaturasini yaratadi"""
    
    buttons = [
        [
            InlineKeyboardButton(
                text="🇷🇺 → 🇬🇧  Rus → Ing",
                callback_data="lang:ru:en"       # ← bot oladigan ma'lumot
            ),
            InlineKeyboardButton(
                text="🇬🇧 → 🇷🇺  Ing → Rus",
                callback_data="lang:en:ru"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🇺🇿 → 🇷🇺  O'zb → Rus",
                callback_data="lang:uz:ru"
            ),
            InlineKeyboardButton(
                text="🇺🇿 → 🇬🇧  O'zb → Ing",
                callback_data="lang:uz:en"
            ),
        ],
        [
            InlineKeyboardButton(
                text="🇬🇧 → 🇺🇿  Ing → O'zb",
                callback_data="lang:en:uz"
            ),
            InlineKeyboardButton(
                text="🇷🇺 → 🇺🇿  Rus → O'zb",
                callback_data="lang:ru:uz"
            ),
        ],
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
