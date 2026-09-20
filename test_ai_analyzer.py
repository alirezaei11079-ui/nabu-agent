import os

from ai_analyzer import (
    analyze_with_ai,
    format_ai_analysis,
)


TEST_POST = """
Hazels x Nabulines 👁⃤

50 WL spots up for grabs.

How to enter:
❤️ Like
🔁 Repost
👥 Follow @nabulines & @0xhazels

Drop your EVM address below.

50 winners.
Good luck.
"""


def main():

    if not os.getenv("GEMINI_API_KEY"):

        raise RuntimeError(
            "GEMINI_API_KEY is missing."
        )

    print(
        "Starting Gemini AI analysis..."
    )

    result = analyze_with_ai(
        TEST_POST,
        "https://x.com/nabulines"
    )

    print(
        "\n=============================="
    )

    print(
        "AI ANALYSIS RESULT"
    )

    print(
        "==============================\n"
    )

    print(
        format_ai_analysis(
            result
        )
    )

    print(
        "\n=============================="
    )

    print(
        "RAW JSON"
    )

    print(
        "==============================\n"
    )

    import json

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2
        )
    )

    print(
        "\nAI ANALYZER TEST: SUCCESS"
    )


if __name__ == "__main__":

    main()


