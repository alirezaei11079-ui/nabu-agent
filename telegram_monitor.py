import os
import json
import requests
from bs4 import BeautifulSoup

from analyzer import analyze_message, format_alert

from action_intelligence import (
    build_action_intelligence,
    format_action_intelligence,
)


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

            return json.load(
                file
            )

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
        f"Analyzing post: {post['id']}"
    )

    analysis = analyze_message(
        post["text"],
        post["link"]
    )

    message = format_alert(
        analysis
    )

    intelligence = build_action_intelligence(
        analysis
    )

    intelligence_message = format_action_intelligence(
        intelligence
    )

    send_telegram(
        message
    )

    send_telegram(
        intelligence_message
    )

    print(
        f"Post {post['id']} analyzed and sent."
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
        f"Monitor state updated to: {latest_processed_id}"
    )


if __name__ == "__main__":

    main()
