from deep_translator import GoogleTranslator

# Tarjima uchun matnning maksimal uzunligi
MAX_TEXT_LENGTH = 4000


def translate_text(text: str, source: str = "auto", target: str = "en") -> str:
    """
    Matnni bir tildan boshqasiga tarjima qiladi.
    
    Argumentlar:
        text   — tarjima qilinadigan matn
        source — asl til ("ru", "en", "uz", "auto")
        target — tarjima tili ("ru", "en", "uz")
    
    Qaytaradi:
        Tarjima qilingan matn yoki xato xabari
    """
    
    # Tekshirish: matn bo'sh emas
    if not text or not text.strip():
        return "⚠️ Bo'sh xabar. Tarjima uchun matn yuboring."
    
    # Tekshirish: matn juda uzun emas
    if len(text) > MAX_TEXT_LENGTH:
        return (
            f"⚠️ Matn juda uzun!\n"
            f"Maksimum: {MAX_TEXT_LENGTH} belgi.\n"
            f"Sizning matn: {len(text)} belgi."
        )
    
    try:
        translator = GoogleTranslator(source=source, target=target)
        result = translator.translate(text)
        
        # Google ba'zan None qaytaradi
        if result is None:
            return "⚠️ Tarjima qilib bo'lmadi. Boshqa matn yuboring."
        
        return result
        
    except Exception as e:
        return f"❌ Tarjima xatosi: {e}"