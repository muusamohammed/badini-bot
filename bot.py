import telebot
from telebot import apihelper
import google.generativeai as genai

# --- زانیاریێن تە ---
TELEGRAM_TOKEN = '8736556946:AAHvSvyt6mH8V0LkVNgQ5SEQdD0RYk0dhjc'
GEMINI_API_KEY = 'AIzaSyAeB6cMnSRLFVAIYanprawJJ0OvcfcwLQk'

# ئەڤ دێڕە گەلەک گرنگە بۆ PythonAnywhere دا بوت کار بکەت
apihelper.proxy = {'https': 'http://proxy.server:3128'}

# ڕێکخستنا Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

SYSTEM_PROMPT = "تو هاریكارەكێ زیرەكی و شارەزایی د كۆدینگێ دا. ب شێوەزارێ بادینی بەرسڤێ بدە. ئەگەر كەسەكی سلاڤ كر یان پرسیارا حالێ تە كر، ب رێز ڤە بەرسڤ بدە."

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text.lower()
    
    # فلترا سادە بۆ سلاڤ و کودی
    coding_keywords = ['کود', 'کۆد', 'python', 'dart', 'flutter', 'html', 'css', 'javascript', 'سلاڤ', 'سڵاو', 'چەوان']
    is_valid = any(word in user_text for word in coding_keywords)

    if is_valid:
        try:
            bot.send_chat_action(message.chat.id, 'typing')
            prompt = f"{SYSTEM_PROMPT}\n\nپرسیارا بەکارهێنەری: {message.text}"
            response = model.generate_content(prompt)
            bot.reply_to(message, response.text)
        except Exception as e:
            print(f"Error: {e}")
            bot.reply_to(message, "ببورە، کێشەیەک د سێرڤەری دا هەبوو.")
    else:
        bot.reply_to(message, "ببورە بەس دشێم دەربارەی کودان هاری تە بکەم")

print("بوت ب پرۆکسی ڤە هاتە کارپێکرن...")
bot.infinity_polling()
