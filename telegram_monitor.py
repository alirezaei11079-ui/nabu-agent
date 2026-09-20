import os
import json
import requests
from bs4 import BeautifulSoup

from analyzer import analyze_message, format_alert

from action_intelligence import (
    build_action_intelligence,
    format_action_intelligence,
)

from ai_analyzer import (
    analyze_with_ai,
    format_ai_analysis,
)


CHANNEL = "web3nabu"
STATE_FILE = "telegram_state.json"

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram(message):

    if not BOT_TOKEN or not CHAT_ID:
        raise RuntimeError(
            "Telegram credentials are missing."
        )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    # Telegram message limit protection
    max_length = 3900

    if len(message) <= max_length:

        response = requests.post(
            url,
            json={
                "chat_id": CHAT_ID,
                "text": message,
                "disable_web_page_preview": False,
            },
            timeout=30,
        )

        response.raise_for_status()

        return

    # Split long messages safely
    chunks = []

    while message:

        chunk = message[:max_length]

        # Try to split at a newline
        newline_position = chunk.rfind("\n")

        if newline_position > 1000:
            chunk = chunk[:newline_position]

        chunks.append(chunk)

        message = message[len(chunk):]

    for chunk in chunks:

        response = requests.post(
            url,
            json={
                "chat_id": CHAT_ID,
                "text": chunk,
                "disable_web_page_preview": False,
            },
            timeout=30,
        )

        response.raise_for_status()


def get_posts():

    url = f"https://t.me/s/{CHANNEL}"

    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=20,
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    posts = soup.select(
        ".tgme_widget_message"
    )

    results = []

    for post in posts:

        data_post = post.get(
            "data-post"
        )

        if not data_post:
            continue

        try:

            post_id = int(
                data_post.split("/")[-1]
            )

        except ValueError:

            continue

        text_element = post.select_one(
            ".tgme_widget_message_text"
        )

        text = (
            text_element.get_text(
                "\n",
                strip=True
            )
            if text_element
            else ""
        )

        link = (
            f"https://t.me/{CHANNEL}/{post_id}"
        )

        results.append(
            {
                "id": post_id,
                "text": text,
                "link": link,
            }
        )

    results.sort(
        key=lambda x: x["id"]
    )

    return results


def load_state():

    if not os.path.exists(
        STATE_FILE
    ):

        return {
            "last_post_id": 0
        }

    try:

        with open(
            STATE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return {
            "last_post_id": 0
        }


def save_state(post_id):

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            {
                "last_post_id": post_id
            },
            file,
            ensure_ascii=False,
            indent=2,
        )


def process_post(post):

    print(
        f"Analyzing Telegram post: {post['id']}"
    )

    # ==============================
    # V4 SECURITY ANALYSIS
    # ==============================

    analysis = analyze_message(
        post["text"],
        post["link"]
    )

    security_message = format_alert(
        analysis
    )

    # ==============================
    # V5 ACTION INTELLIGENCE
    # ==============================

    intelligence = build_action_intelligence(
        analysis
    )

    intelligence_message = (
        format_action_intelligence(
            intelligence
        )
    )

    # ==============================
    # V6 AI ANALYSIS
    # ==============================

    ai_message = None

    try:

        print(
            "Running Gemini AI analysis..."
        )

        ai_result = analyze_with_ai(
            post["text"],
            post["link"]
        )

        ai_message = format_ai_analysis(
            ai_result
        )

        print(
            "Gemini AI analysis completed."
        )

    except Exception as error:

        print(
            f"Gemini AI analysis failed: {error}"
        )

        ai_message = (
            "🤖 NABU AI INTELLIGENCE\n\n"
            "⚠️ تحلیل هوش مصنوعی در این اجرا "
            "در دسترس نبود.\n"
            "لایه‌های امنیتی V4 و V5 همچنان "
            "اجرا شده‌اند."
        )

    # ==============================
    # COMBINED REPORT
    # ==============================

    final_message = (
        "📡 NABU TELEGRAM\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🔐 V4 SECURITY ANALYSIS\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        + security_message
        + "\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🛡️ V5 ACTION INTELLIGENCE\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        + intelligence_message
        + "\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        + ai_message
    )

    send_telegram(
        final_message
    )

    print(
        f"Telegram post {post['id']} "
        "analyzed and sent."
    )


def main():

    posts = get_posts()

    if not posts:

        print(
            "No Telegram posts found."
        )

        return

    state = load_state()

    last_post_id = state.get(
        "last_post_id",
        0
    )

    print(
        f"Found posts: {len(posts)}"
    )

    print(
        f"Previous post: {last_post_id}"
    )

    print(
        f"Latest post: {posts[-1]['id']}"
    )

    # First run
    if last_post_id == 0:

        save_state(
            posts[-1]["id"]
        )

        print(
            "Initial Telegram state saved."
        )

        return

    new_posts = [
        post
        for post in posts
        if post["id"] > last_post_id
    ]

    if not new_posts:

        print(
            "No new post."
        )

        return

    print(
        f"New posts found: {len(new_posts)}"
    )

    latest_processed_id = last_post_id

    for post in new_posts:

        try:

            process_post(
                post
            )

            latest_processed_id = post[
                "id"
            ]

        except Exception as error:

            print(
                f"Post {post['id']} failed: {error}"
            )

            raise

    save_state(
        latest_processed_id
    )

    print(
        f"Monitor state updated to: "
        f"{latest_processed_id}"
    )


if __name__ == "__main__":
    main()
