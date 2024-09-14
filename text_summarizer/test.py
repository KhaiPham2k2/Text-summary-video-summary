from googletrans import Translator

# Tạo đối tượng Translator
translator = Translator()

# Dịch từ tiếng Việt sang tiếng Anh
text_vi = "Tôi đang học Python."
translated_text_en = translator.translate(text_vi, src='vi', dest='en')
print(translated_text_en.text)  # Output: "I am learning Python."

# Dịch từ tiếng Anh sang tiếng Việt
text_en = "I am writing a Python application."
translated_text_vi = translator.translate(text_en, src='en', dest='vi')
print(translated_text_vi.text)  # Output: "Tôi đang viết một ứng dụng Python."
