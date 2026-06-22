import os
import threading
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import Conflict, NetworkError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

TOKEN_BOT = "8561070385:AAEJhLXMdeAK1Fol32YH9mMIRApuhyqeqYM"  # ← Replace with your token

# 🔑 ALL ACCESS KEYS AND CODES
KUNCI_DAFTAR = {
    "key1": "b5669fca-da1c-4e72-889b-0724d20f0290",
    "key2": "7c2a9d4b-8e1f-4c3d-a5b6-f1e2d3c4b5a6",  # ← Replace with your key2
    "key3": "a1b2c3d4-e5f6-4g7h-8i9j-k0l1m2n3o4p5"
}

# ✅ Manual access codes
KODE_AKSES_MANUAL = {
    "Unlock 144 FPS V2.0 - AXM": "key1",
    "Unlock 144 FPS V3.0 - AXM": "key3"
}

OWNER = "@RixXze"

# --- WEB SERVER TO KEEP BOT ALIVE ---
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
        logger.warning("Conflict — another instance is running.")
    elif isinstance(context.error, NetworkError):
        logger.warning(f"Network error: {context.error}")
    else:
        logger.error(f"Error: {context.error}")

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

def main():
    app = Application.builder().token(TOKEN_BOT).build()
    app.add_error_handler(error_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    logger.info("Bot is now running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
