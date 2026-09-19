from analyzer import analyze_message, format_alert


TEST_MESSAGES = [

    {
        "name": "REAL MINT",
        "text": """
        Mint is live!
        Connect your wallet and mint now.
        Limited supply.
        """,
        "link": "https://example.com/test",
    },

    {
        "name": "REAL CLAIM",
        "text": """
        Eligible users can now claim their rewards.
        Claim is available until tomorrow.
        """,
        "link": "https://example.com/test",
    },

    {
        "name": "COMPETITION",
        "text": """
        امروز ساعت ۷ مسابقه داریم 🏆
        LangGraph Part 2
        جزوه در بخش Learn آماده است.
        کد ورود ۲۰ دقیقه قبل از شروع همینجا قرار می‌گیرد.
        """,
        "link": "https://example.com/test",
    },

    {
        "name": "NORMAL ANNOUNCEMENT",
        "text": """
        We are excited to announce our new partnership.
        More details coming soon.
        """,
        "link": "https://example.com/test",
    },

    {
        "name": "FAKE MINT WORD",
        "text": """
        Today we have a competition with Minted_Mind.
        Join us tonight.
        """,
        "link": "https://example.com/test",
    },

    {
        "name": "TRUSTED GITHUB",
        "text": """
        New update is available.
        Check the official repository:
        https://github.com/alirezaei11079-ui/nabu-agent
        """,
        "link": "https://github.com/alirezaei11079-ui/nabu-agent",
    },

    {
        "name": "TRUSTED TELEGRAM",
        "text": """
        Official Telegram channel:
        https://t.me/web3nabu
        """,
        "link": "https://t.me/web3nabu",
    },

    {
        "name": "UNKNOWN CRYPTO DOMAIN",
        "text": """
        Claim your rewards here:
        https://example.net/claim
        """,
        "link": "https://example.net/claim",
    },

    {
        "name": "SHORTENER",
        "text": """
        Mint now:
        https://bit.ly/example
        """,
        "link": "https://bit.ly/example",
    },

    {
        "name": "HTTP URL",
        "text": """
        Visit the website:
        http://example.com
        """,
        "link": "http://example.com",
    },

    {
        "name": "BROKEN URL",
        "text": """
        Claim here:
        https://this-domain-should-not-exist-987654321.com/claim
        """,
        "link": "https://this-domain-should-not-exist-987654321.com/claim",
    },
]


def print_source_details(result):

    print("\n--- SOURCE DETAILS ---")

    sources = result.get(
        "sources",
        []
    )

    if not sources:

        print("No sources found.")

        return

    for source in sources:

        print(
            "Domain:",
            source.get("domain")
        )

        print(
            "Status:",
            source.get("status")
        )

        print(
            "Risk:",
            source.get("risk")
        )

        live = source.get("live")

        if live:

            print(
                "Live reachable:",
                live.get("reachable")
            )

            print(
                "HTTPS:",
                live.get("https")
            )

            print(
                "Redirected:",
                live.get("redirected")
            )

            print(
                "HTTP status:",
                live.get("status_code")
            )

            print(
                "Final domain:",
                live.get("final_domain")
            )

            if live.get("error"):

                print(
                    "Live error:",
                    live.get("error")
                )

        warnings = source.get(
            "warnings",
            []
        )

        if warnings:

            print(
                "Warnings:",
                warnings
            )

        print("-" * 40)


def run_tests():

    print("=" * 60)
    print("NABU ANALYZER V3")
    print("LIVE URL SECURITY TEST")
    print("=" * 60)

    total = len(
        TEST_MESSAGES
    )

    passed = 0

    for index, test in enumerate(
        TEST_MESSAGES,
        start=1
    ):

        print("\n")
        print("=" * 60)
        print(
            f"TEST {index}/{total}: {test['name']}"
        )
        print("=" * 60)

        try:

            result = analyze_message(
                test["text"],
                test["link"]
            )

            print(
                format_alert(result)
            )

            print_source_details(
                result
            )

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

            print(
                "Source status:",
                result["source_status"]
            )

            print(
                "Source risk:",
                result["source_risk"]
            )

            passed += 1

        except Exception as error:

            print("\n❌ TEST FAILED")

            print(
                "Error:",
                error
            )

    print("\n")
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    print(
        f"Passed: {passed}/{total}"
    )

    if passed == total:

        print(
            "✅ ALL TESTS COMPLETED SUCCESSFULLY"
        )

    else:

        print(
            "⚠️ SOME TESTS FAILED"
        )


if __name__ == "__main__":
    run_tests()

  
