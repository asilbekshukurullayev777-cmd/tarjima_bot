from utils.translator import translate_text

# Test 1: ruscha → inglizcha
print(translate_text("Привет, как дела?", "ru", "en"))
# Kutilgan natija: Hello, how are you?

# Test 2: inglizcha → ruscha
print(translate_text("Hello world", "en", "ru"))
# Kutilgan natija: Привет мир

# Test 3: avtomatik aniqlash → o'zbekcha
print(translate_text("Привет", "auto", "uz"))
# Kutilgan natija: Salom