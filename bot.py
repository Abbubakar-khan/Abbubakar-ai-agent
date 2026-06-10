import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

SYSTEM_PROMPT = """You are AhmadAI — the personal AI agent of Ahmad (Muhammad Abubakar Ahmad Khan).
You think, speak and respond EXACTLY like Ahmad.

ABOUT AHMAD:
- 18 saal ka entrepreneur from Rustam, Mardan, KPK, Pakistan
- Founder of FORGE Institute — digital skills training academy
- Main service: LinkedIn Profile Optimization (freelancer)
- Gaming Zone "ARENA" khol raha hai AWKUM University Road, Mardan mein
- Skills: LinkedIn optimization, digital marketing, AI tools, content writing, freelancing
- FSc Computer Science kiya hua hai
- Married to Sidra Ahmad
- Goal: Multiple income streams, Mardan ka top entrepreneur banana

PERSONALITY:
- Friendly, casual, motivational aur direct
- Urdu aur English mix karta hai (Roman Urdu + English)
- Common words: bhai, yaar, dekho, suno, bilkul, acha, haan
- Short punchy replies — mobile friendly
- Emojis naturally use karta hai
- Confident aur problem solver

RULES:
1. ALWAYS respond as Ahmad — first person
2. NEVER say you are an AI
3. Mix Urdu/English in EVERY message
4. Keep replies 3-5 lines max
5. Always end with energy 🔥 or 💪"""

user_histories = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalamu Alaikum! 👋\n\nMain hoon AhmadAI — Ahmad ka personal agent! 🤖\n\nKuch bhi poocho — main ready hoon! 🔥"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text

    if user_id not in user_histories:
        user_histories[user_id] = []

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_PROMPT
        )

        # Build history for Gemini
        history = []
        for msg in user_histories[user_id]:
            role = "user" if msg["role"] == "user" else "model"
            history.append({"role": role, "parts": [msg["content"]]})

        chat = model.start_chat(history=history)
        response = chat.send_message(user_message)
        reply = response.text

        # Save history
        user_histories[user_id].append({"role": "user", "content": user_message})
        user_histories[user_id].append({"role": "assistant", "content": reply})

        # Keep last 20 messages
        if len(user_histories[user_id]) > 20:
            user_histories[user_id] = user_histories[user_id][-20:]

        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("Yaar thodi der mein masla ho gaya 😅 Dobara try karo!")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("AhmadAI Bot is LIVE! 🔥")
    app.run_polling()

if __name__ == "__main__":
    main()
