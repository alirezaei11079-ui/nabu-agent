
import os
import requests


BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")

USERNAME = "nabulines"


def get_user_id(username):

    url = (
        "https://api.x.com/2/users/by/username/"
        + username
    )

    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    return data["data"]["id"]


def get_latest_posts(user_id):

    url = (
        f"https://api.x.com/2/users/"
        f"{user_id}/tweets"
    )

    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }

    params = {
        "max_results": 10,
        "tweet.fields": "created_at,text"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    return response.json()


def main():

    if not BEARER_TOKEN:

        print(
            "ERROR: X_BEARER_TOKEN is missing."
        )

        return

    print(
        "Connecting to X..."
    )

    user_id = get_user_id(
        USERNAME
    )

    print(
        f"X user ID: {user_id}"
    )

    data = get_latest_posts(
        user_id
    )

    posts = data.get(
        "data",
        []
    )

    print(
        f"Posts received: {len(posts)}"
    )

    for post in posts:

        print(
            "\n--- POST ---"
        )

        print(
            f"ID: {post['id']}"
        )

        print(
            f"Date: {post.get('created_at', 'N/A')}"
        )

        print(
            f"Text:\n{post['text']}"
        )


if __name__ == "__main__":

    main()
