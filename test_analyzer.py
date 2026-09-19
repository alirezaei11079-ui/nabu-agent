from analyzer import analyze_message, format_alert


TEST_MESSAGES = [

    {
        "name": "REAL MINT",
        "text": """
        Mint is live!
        Connect your wallet and mint now.
        Limited supply.
        """,
    },

    {
        "name": "REAL CLAIM",
        "text": """
        Eligible users can now claim their rewards.
        Claim is available until tomorrow.
        """,
    },

    {
        "name": "COMPETITION",
        "text": """
        امروز ساعت ۷ مسابقه داریم 🏆
        LangGraph Part 2
        جزوه در بخش Learn آماده است.
        کد ورود ۲۰ دقیقه قبل از شروع همینجا قرار می‌گیرد.
        """,
    },

    {
        "name": "NORMAL ANNOUNCEMENT",
        "text": """
        We are excited to announce our new partnership.
        More details coming soon.
        """,
    },

    {
        "name": "FAKE MINT WORD",
        "text": """
        Today we have a competition with Minted_Mind.
        Join us tonight.
        """,
    },
]


def run_tests():

    print("=" * 60)
    print("NABU ANALYZER TEST")
    print("=" * 60)

    for test in TEST_MESSAGES:

        print("\n")
        print("=" * 60)
        print(f"TEST: {test['name']}")
        print("=" * 60)

        result = analyze_message(
            test["text"],
            "https://example.com/test"
        )

        print(format_alert(result))

        print("\n--- RAW ANALYSIS ---")

        print(
            "Priority:",
            result["priority"]
        )

        print(
            "Risk:",
            result["risk"]
        )

        print(
            "Topics:",
            result["topics"]
        )

        print(
            "Actions:",
            result["actions"]
        )

        print(
            "Selected action:",
            result["action"]
        )

        print(
            "Action required:",
            result["action_required"]
        )

        print(
            "Financial action:",
            result["financial_action"]
        )

        print(
            "Deadlines:",
            result["deadlines"]
        )


if __name__ == "__main__":
    run_tests()
