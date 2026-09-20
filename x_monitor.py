import os
import json
import requests
import xml.etree.ElementTree as ET
from html import unescape
from email.utils import parsedate_to_datetime

from analyzer import analyze_message, format_alert

from action_intelligence import (
    build_action_intelligence,
    format_action_intelligence,
)


FEED_URL = "https://fxtwitter.com/nabulines/feed.xml"

STATE_FILE = "x_state.json"

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def clean_html(text):

    if not text:
        return ""

    text = unescape(text)

    replacements = {
        "<br>": "\n",
        "<br/>": "\n",
        "<br />": "\n",
        "</p>": "\n",
        "<p>": "",
    }

    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )

    import re

    text = re.sub(
        r"<[^>]+>",
        "",
        text
    )

    lines = [
        line.strip()
        for line in text.splitlines()
    ]

    lines = [
        line
        for line in lines
        if line
    ]

    return "\n".join(lines)


def send_telegram(message):

    if not BOT_TOKEN or not CHAT_ID:

        raise RuntimeError(
            "Telegram credentials are missing."
        )

    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage"
    )

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


def get_posts():

    response = requests.get(
        FEED_URL,
        headers={
            "User-Agent": "Nabu-Agent/1.0"
        },
        timeout=30,
    )

    response.raise_for_status()

    root = ET.fromstring(
        response.content
    )

    posts = []

    for item in root.findall(
        ".//item"
    ):

        title = item.findtext(
            "title",
            default=""
        )

        link = item.findtext(
            "link",
            default=""
        )

        guid = item.findtext(
            "guid",
            default=""
        )

        description = item.findtext(
            "description",
            default=""
        )

        pub_date = item.findtext(
            "pubDate",
            default=""
        )

        post_id = guid or link

        if not post_id:

            continue

        text = clean_html(
            description
        )

        posts.append(
            {
                "id": post_id,
                "text": text,
                "title": clean_html(
                    title
                ),
                "link": link,
                "pub_date": pub_date,
            }
        )

    return posts


def load_state():

    if not os.path.exists(
        STATE_FILE
    ):

        return {
            "last_post_id": ""
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
            "last_post_id": ""
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


def sort_posts(posts):

    def sort_key(post):

        try:

            return parsedate_to_datetime(
                post["pub_date"]
            )

        except Exception:

            return post["pub_date"]

    return sorted(
        posts,
        key=sort_key
    )


def process_post(post):

    print(
        f"Analyzing X post: {post['id']}"
    )

    text = post["text"]

    if not text:

        text = post["title"]

    analysis = analyze_message(
        text,
        post["link"]
    )

    message = format_alert(
        analysis
    )

    intelligence = build_action_intelligence(
        analysis
    )

    intelligence_message = (
        format_action_intelligence(
            intelligence
        )
    )

    x_header = (
        "𝕏 X / @nabulines\n\n"
    )

    send_telegram(
        x_header + message
    )

    send_telegram(
        x_header + intelligence_message
    )

    print(
        f"X post {post['id']} "
        "analyzed and sent to Telegram."
    )


def main():

    print(
        "Connecting to FxTwitter RSS..."
    )

    posts = get_posts()

    posts = sort_posts(
        posts
    )

    if not posts:

        print(
            "No X posts found."
        )

        return

    print(
        f"Posts received: {len(posts)}"
    )

    state = load_state()

    last_post_id = state.get(
        "last_post_id",
        ""
    )

    print(
        f"Previous post: {last_post_id}"
    )

    print(
        f"Latest post: {posts[-1]['id']}"
    )

    if not last_post_id:

        save_state(
            posts[-1]["id"]
        )

        print(
            "Initial X state saved."
        )

        return

    new_posts = []

    found_previous = False

    for post in posts:

        if post["id"] == last_post_id:

            found_previous = True

            continue

        if found_previous:

            new_posts.append(
                post
            )

    if not found_previous:

        new_posts = [
            post
            for post in posts
            if post["id"] != last_post_id
        ]

    if not new_posts:

        print(
            "No new X post."
        )

        return

    print(
        f"New X posts found: "
        f"{len(new_posts)}"
    )

    latest_processed_id = (
        last_post_id
    )

    for post in new_posts:

        try:

            process_post(
                post
            )

            latest_processed_id = (
                post["id"]
            )

        except Exception as error:

            print(
                f"X post {post['id']} "
                f"failed: {error}"
            )

            raise

    save_state(
        latest_processed_id
    )

    print(
        "X monitor state updated."
    )


if __name__ == "__main__":

    main()


