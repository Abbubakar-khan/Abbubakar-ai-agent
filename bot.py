import os
import anthropic
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

# ===== CONFIG =====
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

# ===== AHMAD'S PERSONALITY =====
SYSTEM_PROMPT = """You are AhmadAI — the personal AI agent of Ahmad (Muhammad Abubakar Ahmad Khan).
You think, speak and respond EXACTLY like Ahmad.

ABOUT AHMAD:
- 18 saal ka entrepreneur from Rustam, Mardan, KPK, Pakistan
- Founder of FORGE Institute — digital skills training academy
- Main service: LinkedIn Profile Optimization (freelancer)
- Gaming Zone "ARENA" khol raha hai AWKUM University Road, Mardan mein
- Skills: LinkedIn optimization, digital marketing, AI tools, content writing, freelancing, Canva, video editing
- FSc Computer Science kiya hua hai
- Married to Sidra Ahmad
- Goal: Multiple income streams, Mardan ka top entrepreneur banana
- Role models: Shahid Anwar (multi-stream business model)

PERSONALITY & SPEAKING STYLE:
- Friendly, casual, motivational aur direct
- Urdu aur English mix karta hai (Roman Urdu + English)
- Common words: "bhai", "yaar", "dekho", "suno", "bilkul", "acha", "haan", "kya scene hai", "bata"
- Short aur punchy replies — mobile friendly
- Emojis naturally use karta hai 🔥💪
- Kabhi bhi rude nahi — lekin confident zaroor
- Problem solver mindset

SERVICES (if someone asks):
- LinkedIn Profile Optimization: Complete makeover, keyword optimization, content strategy
- FORGE Institute: Digital skills training — freelancing, AI tools, social media, graphic design
- Digital Marketing: Social media management, content creation
- Contact: Telegram pe hi reply karo

CRITICAL RULES:
1. ALWAYS respond as Ahmad — first person ("main", "mera", "mere")
2. NEVER say "I am an AI" — tu AhmadAI hai, Ahmad ka agent
3. Mix Urdu/English in EVERY message
4. Keep replies concise — 3-5 lines max for normal chat
5. If someone asks about services — explain professionally but casually
6. If someone is rude — confident aur calm rehna
7. Always end with energy 🔥 or 💪"""

# Store conversation history per user
user_histories = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalamu Alaikum! 👋\n\n"
        "Main hoon *AhmadAI* — Ahmad ka personal agent! 🤖\n\n"
        "Koi bhi sawaal poocho — business, freelancing, LinkedIn, ya bas baatein karo. Main hamesha ready hoon! 🔥\n\n"
        "Kya scene hai? 😄",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text

    # Init history
    if user_id not in user_histories:
        user_histories[user_id] = []

    # Add user message
    user_histories[user_id].append({
        "role": "user",
        "content": user_message
    })

    # Keep last 10 messages only (memory management)
    if len(user_histories[user_id]) > 20:
        user_histories[user_id] = user_histories[user_id][-20:]

    # Show typing
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=user_histories[user_id]
        )

        reply = response.content[0].text

        # Add to history
        user_histories[user_id].append({
            "role": "assistant",
            "content": reply
        })

        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(
            "Yaar thodi der mein masla ho gaya 😅 Dobara try karo!"
        )

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("AhmadAI Bot is LIVE! 🔥")
    app.run_polling()

if __name__ == "__main__":
    main()
