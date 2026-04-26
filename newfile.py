import telebot
from telebot import types
from groq import Groq
from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run():
    # Render အတွက် Port ကို ဒီနေရာမှာ သတ်မှတ်ရပါမယ်
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ဒီ Function ကို Define လုပ်ပေးရပါမယ်
def keep_alive():
    t = Thread(target=run)
    t.start()


# --- Bot Setup အပိုင်း ---
# သင့်ရဲ့ API Keys များကို ဒီမှာထည့်ပါ
client = Groq(api_key="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")
bot = telebot.TeleBot("8730208154:AAFVzoeHqMqLGXd-vokHRuSfpTpgm2Rh0ko")

SYSTEM_PROMPT = """
You are a friendly and funny Myanmar AI assistant. 
Your name is 'Takaa'. 
You must always reply in Myanmar and Englis language. 
Use a friendly tone like a close friend, and use emojis.
"""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('🤖 AI နဲ့ စကားပြောမယ်')
    itembtn2 = types.KeyboardButton('📜 အသုံးပြုနည်း')
    itembtn3 = types.KeyboardButton('💡 ဟာသပြောပြပါ')
    markup.add(itembtn1, itembtn2, itembtn3)
    
    welcome_text = "မင်္ဂလာပါဗျာ! ကျွန်တော်က Zay Yar AI ပါ။ \nအောက်က ခလုတ်တွေကို နှိပ်ပြီး ခိုင်းလို့ရပါတယ်!"
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if message.text == '📜 အသုံးပြုနည်း':
        bot.reply_to(message, "ကျွန်တော့်ဆီကို ဘာမဆို မေးလို့ရပါတယ်။ မြန်မာလိုပဲဖြစ်ဖြစ်၊ အင်္ဂလိပ်လိုပဲဖြစ်ဖြစ် ဖြေပေးနိုင်ပါတယ်ဗျ!")
        
    elif message.text == '💡 ဟာသပြောပြပါ':
        bot.send_chat_action(message.chat.id, 'typing')
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "ဟာသတစ်ခုလောက် ပြောပြပါဦး"}
            ],
            model="llama-3.3-70b-versatile",
        )
        bot.reply_to(message, chat_completion.choices[0].message.content)

    else:
        bot.send_chat_action(message.chat.id, 'typing')
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message.text}
                ],
                model="llama-3.3-70b-versatile",
            )
            bot.reply_to(message, chat_completion.choices[0].message.content)
        except Exception as e:
            bot.reply_to(message, "အခုလောလောဆယ် AI အလုပ်မလုပ်သေးလို့ ခဏနေမှ ပြန်မေးပေးပါနော်။")

# --- Program စတင် Run သည့်အပိုင်း ---
if __name__ == "__main__":
    try:
        # Flask Web Server ကို Background မှာ အရင်နှိုးမယ်
        keep_alive()
        print("Web server started...")
        
        # Bot ကို စတင် Run မယ် (Error တက်ရင် ပြန်စအောင် loop ပတ်ထားမယ်)
        print("Bot is starting...")
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
        
    except Exception as e:
        print(f"Main Error: {e}")
