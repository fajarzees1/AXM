import os
import threading
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import Conflict, NetworkError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

TOKEN_BOT = "8561070385:AAEJhLXMdeAK1Fol32YH9mMIRApuhyqeqYM"  # ← ganti ini

# 🔑 DAFTAR SEMUA SANDI & KODE AKSES
KUNCI_DAFTAR = {
    "key1": "b5669fca-da1c-4e72-889b-0724d20f0290",
    "key2": "7c2a9d4b-8e1f-4c3d-a5b6-f1e2d3c4b5a6"  # ← ganti password key2
}

# ✅ Kode akses ketikan manual
KODE_AKSES_MANUAL = {
    "Unlock 144 FPS V2.0 - AXM": "key1"
}

CHANNEL_NAME = "@aimxmodpubg"
OWNER = "@RixXze"

# --- WEB SERVER AGAR TIDAK MATI ---
class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")
    def log_message(self, format, *args):
        pass

def jalankan_server():
    try:
        server = HTTPServer(("0.0.0.0", 5000), PingHandler)
        server.serve_forever()
    except OSError:
        pass

threading.Thread(target=jalankan_server, daemon=True).start()

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    if isinstance(context.error, Conflict):
        logger.warning("Conflict — instance lain berjalan.")
    elif isinstance(context.error, NetworkError):
        logger.warning(f"Network error: {context.error}")
    else:
        logger.error(f"Error: {context.error}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        kode_link = context.args[0].lower().strip()
        if kode_link in KUNCI_DAFTAR:
            await update.message.reply_text(
                "✅ 𝗟𝗜𝗡𝗞 𝗔𝗖𝗖𝗘𝗦𝗦 𝗚𝗥𝗔𝗡𝗧𝗘𝗗 🎉\n\n"
                "🔐 𝗬𝗼𝘂𝗿 𝗨𝗻𝗹𝗼𝗰𝗸 𝗞𝗲𝘆:\n"
                f"`{KUNCI_DAFTAR[kode_link]}`\n\n"
                "⚠️ 𝗞𝗲𝗲𝗽 𝗽𝗿𝗶𝘃𝗮𝘁𝗲\n"
                "📂 𝗢𝗽𝗲𝗻 𝗭𝗜𝗣 → 𝗣𝗮𝘀𝘁𝗲 → 𝗗𝗼𝗻𝗲!",
                parse_mode="Markdown"
            )
            return

    await update.message.reply_text(
        "👋 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗔𝗶𝗺 𝗫 𝗠𝗼𝗱 𝗞𝗲𝘆 𝗕𝗼𝘁\n\n"
        "🔑 Send valid 𝗔𝗖𝗖𝗘𝗦𝗦 𝗖𝗢𝗗𝗘 𝘁𝗼 𝗴𝗲𝘁 𝘆𝗼𝘂𝗿 𝗸𝗲𝘆:\n"
        "👉 Example: example123\n\n"
        f"📢 {CHANNEL_NAME}\n"
        f"👤 {OWNER}"
    )

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    txt = update.message.text.strip()

    if txt in KODE_AKSES_MANUAL:
        nama_kunci = KODE_AKSES_MANUAL[txt]
        await update.message.reply_text(
            "✅ 𝗔𝗖𝗖𝗘𝗦𝗦 𝗚𝗥𝗔𝗡𝗧𝗘𝗗 🎉\n\n"
            "🔐 𝗬𝗼𝘂𝗿 𝗨𝗻𝗹𝗼𝗰𝗸 𝗞𝗲𝘆:\n"
            f"`{KUNCI_DAFTAR[nama_kunci]}`\n\n"
            "⚠️ 𝗞𝗲𝗲𝗽 𝗽𝗿𝗶𝘃𝗮𝘁𝗲\n"
            "📂 𝗢𝗽𝗲𝗻 𝗭𝗜𝗣 → 𝗣𝗮𝘀𝘁𝗲 → 𝗗𝗼𝗻𝗲!",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "❌ 𝗜𝗡𝗩𝗔𝗟𝗜𝗗 𝗖𝗢𝗗𝗘 🚫\n\n"
            "Send only the 𝗰𝗼𝗿𝗿𝗲𝗰𝘁 𝗔𝗰𝗰𝗲𝘀𝘀 𝗖𝗼𝗱𝗲.\n\n"
            f"📢 {CHANNEL_NAME}"
        )

def main():
    app = Application.builder().token(TOKEN_BOT).build()
    app.add_error_handler(error_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    logger.info("Bot mulai berjalan...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
