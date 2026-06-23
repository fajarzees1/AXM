import os
import threading
import logging

# ✅ Flask untuk Gunicorn — WAJIB
from flask import Flask, render_template_string

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import Conflict, NetworkError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

TOKEN_BOT = "8561070385:AAEJhLXMdeAK1Fol32YH9mMIRApuhyqeqYM"

# 🔑 ALL ACCESS KEYS AND CODES — TIDAK DIUBAH
KUNCI_DAFTAR = {
    "key1": "b5669fca-da1c-4e72-889b-0724d20f0290",
    "key2": "7c2a9d4b-8e1f-4c3d-a5b6-f1e2d3c4b5a6",
    "key3": "a1b2c3d4-e5f6-4g7h-8i9j-k0l1m2n3o4p5"
}

# ✅ Manual access codes — TETAP SAMA PERSIS
KODE_AKSES_MANUAL = {
    "Unlock 144 FPS V2.0 - AXM": "key1",
    "Unlock 144 FPS V3.0 - AXM": "key3"
}

OWNER = "@RixXze"

# ==============================================
# ✅ INTI: OBJEK `web` WAJIB AGAR GUNICORN BERJALAN
web = Flask(__name__)
WEB_PORT = int(os.environ.get("PORT", 8080))  # Ikuti aturan resmi Render

# ✅ HALAMAN UTAMA AXM — SUDAH BERJALAN BAIK
HALAMAN_AXM = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AXM Key System • Active</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); font-family: sans-serif;}
        .axm-grad {background: linear-gradient(90deg, #22d3ee, #0ea5e9);-webkit-background-clip: text;-webkit-text-fill-color: transparent;}
    </style>
</head>
<body class="min-h-screen flex items-center justify-center p-4 text-center">
    <div class="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-cyan-400/30 shadow-2xl max-w-md w-full">
        <h1 class="text-4xl font-extrabold axm-grad mb-3">AXM SYSTEM</h1>
        <p class="text-cyan-200/80 text-lg mb-2">✅ Bot & Key Server RUNNING NORMALLY</p>
        <p class="text-white/60 text-sm mt-4">Status: 🟢 ACTIVE 24/7<br>Developer: {{OWNER}}</p>
    </div>
</body>
</html>
"""

@web.route("/")
def utama():
    return render_template_string(HALAMAN_AXM, OWNER=OWNER)

@web.route("/ping")
def ping():
    return "Bot is running!"  # ✅ Tetap ada titik ping seperti aslinya
# ==============================================

# ❌ DIHAPUS: Kelas PingHandler + fungsi jalankan_server lama — SUDAH DIGANTI OLEH FLASK DI ATAS, TIDAK PERLU BEREBUT PORT LAGI

# --- ERROR HANDLER — TIDAK DIUBAH SATU KARAKTER ---
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    if isinstance(context.error, Conflict):
        logger.warning("Conflict — another instance is running.")
    elif isinstance(context.error, NetworkError):
        logger.warning(f"Network error: {context.error}")
    else:
        logger.error(f"Error: {context.error}")

# --- START COMMAND — SAMA PERSIS SEPERTI ASLI ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        kode_link = context.args[0].lower().strip()
        if kode_link in KUNCI_DAFTAR:
            await update.message.reply_text(
                "<b>✅ ACCESS GRANTED</b>\n\n"
                "🔐 <b>Your Unlock Code:</b>\n"
                f"<code>{KUNCI_DAFTAR[kode_link]}</code>\n\n"
                "⚠️ <i>Keep your code secure</i>\n"
                "📂 Extract ZIP → Paste Code → Done",
                parse_mode="HTML"
            )
            return

    await update.message.reply_text(
        "<b>👋 WELCOME TO AXM KEY BOT</b>\n\n"
        "<b>📌 How to Use:</b>\n"
        "Send your <b>access code</b> to get your unlock key\n\n"
        "<b>💡 Example Code:</b>\n"
        "<code>Unlock 144 FPS V2.0 - AXM</code>\n\n"
        f"👤 <b>Developer:</b> {OWNER}",
        parse_mode="HTML"
    )

# --- MESSAGE HANDLER — TETAP RAPI & UTUH ---
async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    txt = update.message.text.strip()

    if txt in KODE_AKSES_MANUAL:
        nama_kunci = KODE_AKSES_MANUAL[txt]
        await update.message.reply_text(
            "<b>✅ ACCESS GRANTED</b>\n\n"
            "🔐 <b>Your Unlock Code:</b>\n"
            f"<code>{KUNCI_DAFTAR[nama_kunci]}</code>\n\n"
            "⚠️ <i>Keep your code secure</i>\n"
            "📂 Extract ZIP → Paste Code → Done",
            parse_mode="HTML"
        )
    else:
        await update.message.reply_text(
            "<b>❌ INVALID CODE</b>\n\n"
            "The code you sent was not found.\n"
            "Please check and try again.\n\n"
            f"👤 <b>Contact:</b> {OWNER}",
            parse_mode="HTML"
        )

# --- MAIN — DITAMBAHKAN: JALANKAN WEB DI BENANG TANPA BENTROK ---
def run_flask_safely():
    web.run(host="0.0.0.0", port=WEB_PORT, debug=False, use_reloader=False)

def main():
    # 🧵 Jalankan peladen web di benang terpisah — AMAN & TIDAK BENTROK
    threading.Thread(target=run_flask_safely, daemon=True).start()

    app = Application.builder().token(TOKEN_BOT).build()
    app.add_error_handler(error_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    logger.info("✅ AXM SYSTEM STABIL DI RENDER — Bot + Web Siaga 24/7")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
