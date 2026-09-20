import requests
import xml.etree.ElementTree as ET
from html import unescape
import re

from analyzer import analyze_message, format_alert

from action_intelligence import (
    build_action_intelligence,
    format_action_intelligence,
)


FEED_URL = "https://fxtwitter.com/nabulines/feed.xml"

BOT_TOKEN = None
CHAT_ID = None


def clean_html(text):

    if not text:
        return ""

    text = unescape(text)

    text = text.replace(
        "<br>",
        "\n"
    )

    text = text.replace(
        "<br/>",
        "\n"
    )

    text = text.replace(
        "<br />",
        "\n"
    )

    text = text.replace(
        "</p>",
        "\n"
    )

    text = text.replace(
        "<p>",
        ""
    )

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


def get_latest_post():

    response = requests.get(
        FEED_URL,
        headers={
            "User-Agent": "Nabu-Agent/1.0"
        },
        timeout=30
    )

    response.raise_for_status()

    root = ET.fromstring(
        response.content
    )

    item = root.find(
        ".//item"
    )

    if item is None:

        raise RuntimeError(
            "No X post found."
        )

    link = item.findtext(
        "link",
        default=""
    )

    description = item.findtext(
        "description",
        default=""
    )

    title = item.findtext(
        "title",
        default=""
    )

    text = clean_html(
        description
    )

    if not text:

        text = clean_html(
            title
        )

    return {
        "text": text,
        "link": link
    }


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


def main():

    global BOT_TOKEN
    global CHAT_ID

    import os

    BOT_TOKEN = os.getenv(
        "TELEGRAM_BOT_TOKEN"
    )

    CHAT_ID = os.getenv(
        "TELEGRAM_CHAT_ID"
    )

    print(
        "Getting latest X post..."
    )

    post = get_latest_post()

    print(
        "X post received."
    )

    print(
        "\nPOST:"
    )

    print(
        post["text"]
    )

    print(
        "\nAnalyzing..."
    )

    analysis = analyze_message(
        post["text"],
        post["link"]
    )

    alert = format_alert(
        analysis
    )

    intelligence = build_action_intelligence(
        analysis
    )

    action_alert = (
        format_action_intelligence(
            intelligence
        )
    )

    header = (
        "𝕏 X TEST\n"
        "@nabulines\n\n"
    )

    send_telegram(
        header + alert
    )

    send_telegram(
        header + action_alert
    )

    print(
        "\nTelegram messages sent."
    )

    print(
        "X → Analyzer V4 → V5 → Telegram: SUCCESS"
    )


if __name__ == "__main__":

    main()


