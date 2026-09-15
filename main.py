import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": message,
        },
        timeout=15,
    )

    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    send_telegram(
        "🤖 Nabu Agent فعال شد!\n\n"
        "اولین تست با موفقیت انجام شد."
    )

    print("Telegram notification sent successfully.")
