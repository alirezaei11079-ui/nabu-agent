import os

from analyzer import (
    analyze_message,
    format_alert,
)

from action_intelligence import (
    build_action_intelligence,
    format_action_intelligence,
)

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

TEST_URL = "https://x.com/nabulines"


def main():

    print("")
    print("================================")
    print("NABU AGENT INTEGRATION TEST")
    print("================================")
    print("")

    # =================================
    # V4 SECURITY
    # =================================

    print("Running V4 Security Analysis...")

    analysis = analyze_message(
        TEST_POST,
        TEST_URL
    )

    security_message = format_alert(
        analysis
    )

    print("V4: SUCCESS")

    # =================================
    # V5 ACTION INTELLIGENCE
    # =================================

    print("Running V5 Action Intelligence...")

    intelligence = build_action_intelligence(
        analysis
    )

    intelligence_message = (
        format_action_intelligence(
            intelligence
        )
    )

    print("V5: SUCCESS")

    # =================================
    # V6 AI
    # =================================

    print("Running V6 Gemini AI Analysis...")

    try:

        ai_result = analyze_with_ai(
            TEST_POST,
            TEST_URL
        )

        ai_message = format_ai_analysis(
            ai_result
        )

        print("V6: SUCCESS")

    except Exception as error:

        print("")
        print("V6: FAILED")
        print(error)
        print("")

        ai_message = (
            "🤖 NABU AI INTELLIGENCE\n\n"
            "⚠️ AI analysis unavailable.\n"
            "V4 and V5 remain operational."
        )

    # =================================
    # FINAL TELEGRAM MESSAGE
    # =================================

    final_message = (
        "𝕏 NABU X / @nabulines\n\n"

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

    print("")
    print("================================")
    print("FINAL TELEGRAM MESSAGE")
    print("================================")
    print("")

    print(final_message)

    print("")
    print("================================")
    print("INTEGRATION TEST: SUCCESS")
    print("================================")
    print("")


if __name__ == "__main__":
    main()


