import os
import requests

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Spam Detection Bot is online."
    )


async def check_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    message_text = update.message.text

    try:
        response = requests.post(
            f"{API_URL}/predict",
            json={
                "message": message_text
            },
            timeout=10
        )

        response.raise_for_status()

        result = response.json()

        prediction = result["prediction"]
        decision_score = result["decision_score"]
        action = result["action"]

        # Block messages classified as spam
        if action == "BLOCKED":

            try:
                await update.message.delete()

                print(
                    f"SPAM BLOCKED | "
                    f"Score: {decision_score} | "
                    f"Message: {message_text}"
                )

            except Exception as delete_error:

                print(
                    f"Could not delete message: {delete_error}"
                )

        else:

            print(
                f"HAM ALLOWED | "
                f"Score: {decision_score} | "
                f"Message: {message_text}"
            )

    except requests.exceptions.RequestException as e:

        print(f"API error: {e}")

def main():

    if not TOKEN:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN is missing from .env"
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            check_message
        )
    )

    print("Telegram spam detection bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()