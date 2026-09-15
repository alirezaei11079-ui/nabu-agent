import os
import re
import json
import requests
from bs4 import BeautifulSoup
from analyzer import analyze_message, format_alert
CHANNEL = "web3nabu"
STATE_FILE = "telegram_state.json"

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": message,
            "disable_web_page_preview": False,
        },
        timeout=20,
    )

    response.raise_for_status()


def get_latest_post():
    url = f"https://t.me/s/{CHANNEL}"

    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=20,
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    posts = soup.select(".tgme_widget_message")

    if not posts:
        return None

    post = posts[-1]

    data_post = post.get("data-post")

    if not data_post:
        return None

    post_id = int(data_post.split("/")[-1])

    text_element = post.select_one(".tgme_widget_message_text")

    text = text_element.get_text(
        "\n",
        strip=True
    ) if text_element else ""

    link = f"https://t.me/{CHANNEL}/{post_id}"

    return {
        "id": post_id,
        "text": text,
        "link": link
    }


def load_state():
    if not os.path.exists(STATE_FILE):
        return {"last_post_id": 0}

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {"last_post_id": 0}


def save_state(post_id):
    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(
            {"last_post_id": post_id},
            file,
            ensure_ascii=False,
            indent=2
        )


def main():
    latest = get_latest_post()

    if not latest:
        print("No Telegram post found.")
        return

    state = load_state()
    last_post_id = state.get("last_post_id", 0)

    print(f"Latest post: {latest['id']}")
    print(f"Previous post: {last_post_id}")

    # First run: establish baseline without sending old posts
    if last_post_id == 0:
        save_state(latest["id"])
        print("Initial Telegram state saved.")
        return

    # Nothing new
    if latest["id"] <= last_post_id:
        print("No new post.")
        return

    # New post detected
  analysis = analyze_message(
    latest["text"],
    latest["link"]
)

message = format_alert(analysis)

send_telegram(message)  

    send_telegram(message)

    save_state(latest["id"])

    print("New Nabu post sent to Telegram.")


if __name__ == "__main__":
    main()
