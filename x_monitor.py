import os
import json
import requests
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime


FEED_URL = "https://fxtwitter.com/nabulines/feed.xml"

STATE_FILE = "x_state.json"


def get_posts():

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

    posts = []

    for item in root.findall(".//item"):

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

        posts.append(
            {
                "id": post_id,
                "text": description,
                "title": title,
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
            indent=2
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

    latest_post = posts[-1]

    print(
        f"Latest post: {latest_post['id']}"
    )

    print(
        f"Previous post: {last_post_id}"
    )

    if not last_post_id:

        save_state(
            latest_post["id"]
        )

        print(
            "Initial X state saved."
        )

        print(
            "\nLatest X post:"
        )

        print(
            latest_post["text"]
        )

        print(
            latest_post["link"]
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
        f"New X posts found: {len(new_posts)}"
    )

    for post in new_posts:

        print(
            "\n===================="
        )

        print(
            "NEW X POST"
        )

        print(
            "===================="
        )

        print(
            f"ID: {post['id']}"
        )

        print(
            f"Date: {post['pub_date']}"
        )

        print(
            f"Link: {post['link']}"
        )

        print(
            "Text:"
        )

        print(
            post["text"]
        )

    save_state(
        new_posts[-1]["id"]
    )

    print(
        "\nX monitor state updated."
    )


if __name__ == "__main__":

    main()
