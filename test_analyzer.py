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

    {
        "name": "SEED PHRASE SCAM",
        "text": """
        Your wallet is eligible for a free reward.
        Connect your wallet and enter your seed phrase
        to verify ownership and claim your tokens.
        """,
        "link": "https://example.net/claim",
    },

    {
        "name": "PRIVATE KEY SCAM",
        "text": """
        Security verification required.
        Import your wallet and provide your private key
        to receive the reward.
        """,
        "link": "https://example.net/verify",
    },

    {
        "name": "RECOVERY PHRASE SCAM",
        "text": """
        Your wallet needs to be synchronized.
        Restore wallet using your recovery phrase
        before claiming the airdrop.
        """,
        "link": "https://example.net/airdrop",
    },

    {
        "name": "CRYPTO TRANSFER SCAM",
        "text": """
        Send 0.05 ETH to verify your wallet.
        After confirmation you will receive the reward.
        """,
        "link": "https://example.net/verify",
    },

    {
        "name": "DEPOSIT TO CLAIM SCAM",
        "text": """
        Deposit 0.1 ETH to claim your free tokens.
        Limited time offer.
        """,
        "link": "https://example.net/claim",
    },

    {
        "name": "VERIFY WALLET SCAM",
        "text": """
        Urgent!
        Verify your wallet immediately.
        Connect wallet to continue and claim your rewards.
        """,
        "link": "https://example.net/verify",
    },

    {
        "name": "FREE MINT SCAM",
        "text": """
        FREE MINT is now live!
        Connect wallet and mint your NFT.
        Claim before tonight.
        """,
        "link": "https://example.net/free-mint",
    },

    {
        "name": "NABU IMPERSONATION",
        "text": """
        Official Nabu reward claim.
        Connect your wallet and claim your Nabu rewards.
        Verify wallet to continue.
        """,
        "link": "https://nabu-claim.example.net/verify",
    },

    {
        "name": "METAMASK IMPERSONATION",
        "text": """
        MetaMask security verification required.
        Connect your wallet and verify your recovery phrase.
        """,
        "link": "https://metamask-security.example.net/verify",
    },

    {
        "name": "MULTI SIGNAL PHISHING",
        "text": """
        URGENT WALLET VERIFICATION

        Connect wallet.
        Verify your wallet.
        Enter your seed phrase.
        Send crypto to complete verification.
        Claim your reward immediately.
        """,
        "link": "https://wallet-verify.example.net/claim",
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

        phishing = source.get(
            "phishing"
        )

        if phishing:

            print(
                "Phishing risk:",
                phishing.get("risk")
            )

            print(
                "Phishing score:",
                phishing.get("score")
            )

            print(
                "Brand impersonation:",
                phishing.get(
                    "brand_impersonation"
                )
            )

            print(
                "Brands:",
                phishing.get(
                    "brands"
                )
            )

            print(
                "Wallet risk:",
                phishing.get(
                    "wallet_risk"
                )
            )

            print(
                "Financial risk:",
                phishing.get(
                    "financial_risk"
                )
            )

            print(
                "Phishing flags:",
                phishing.get(
                    "flags"
                )
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
    print("NABU ANALYZER V4")
    print("SCAM / PHISHING SECURITY TEST")
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
            "✅ ALL V4 TESTS COMPLETED SUCCESSFULLY"
        )

    else:

        print(
            "⚠️ SOME V4 TESTS FAILED"
        )


if __name__ == "__main__":
    run_tests()
