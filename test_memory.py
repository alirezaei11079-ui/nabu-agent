import os
import json

from memory_engine import (
    MEMORY_FILE,
    load_memory,
    save_memory,
    process_ai_event,
    format_memory_update,
)


FIRST_POST = {
    "summary": (
        "Hazels و Nabulines تعداد ۵۰ سهمیه WL "
        "برای یک Giveaway ارائه کرده‌اند."
    ),
    "meaning": (
        "کاربران با انجام تعاملات اجتماعی "
        "می‌توانند در Giveaway شرکت کنند."
    ),
    "category": "GIVEAWAY",
    "project": "Hazels و Nabulines",
    "event": "Giveaway 50 WL",
    "action_required": True,
    "actions": [
        "Like",
        "Repost",
        "Follow",
        "Submit EVM address"
    ],
    "urgency": "LOW",
    "deadline": "unknown",
    "cost": "unknown",
    "network": "unknown",
    "contract_address": "unknown",
    "wallet_required": "UNKNOWN",
    "financial_action": False,
    "eligibility": "unknown",
    "reward": "50 WL spots",
    "links": [],
    "requirements": [
        "Like",
        "Repost",
        "Follow",
        "EVM address"
    ],
    "unknowns": [
        "Deadline",
        "Network"
    ],
    "risk_notes": [],
    "user_steps": []
}


SECOND_POST = {
    "summary": (
        "Hazels و Nabulines اعلام کردند "
        "که برندگان WL فردا معرفی می‌شوند."
    ),
    "meaning": (
        "Giveaway قبلی وارد مرحله اعلام "
        "برندگان شده است."
    ),
    "category": "GIVEAWAY",
    "project": "Hazels و Nabulines",
    "event": "Giveaway 50 WL",
    "action_required": False,
    "actions": [],
    "urgency": "MEDIUM",
    "deadline": "2026-09-21",
    "cost": "unknown",
    "network": "unknown",
    "contract_address": "unknown",
    "wallet_required": "UNKNOWN",
    "financial_action": False,
    "eligibility": "unknown",
    "reward": "50 WL spots",
    "links": [],
    "requirements": [],
    "unknowns": [],
    "risk_notes": [],
    "user_steps": []
}


def main():

    print("")
    print("==============================")
    print("NABU MEMORY ENGINE TEST")
    print("==============================")
    print("")

    # Start with a clean test memory
    save_memory({
        "events": []
    })

    print("Creating first event...")

    result_1 = process_ai_event(
        FIRST_POST,
        "https://x.com/nabulines/status/test1"
    )

    print(
        format_memory_update(
            result_1
        )
    )

    print("")
    print("------------------------------")
    print("")

    print("Processing related update...")

    result_2 = process_ai_event(
        SECOND_POST,
        "https://x.com/nabulines/status/test2"
    )

    print(
        format_memory_update(
            result_2
        )
    )

    print("")
    print("==============================")
    print("FINAL MEMORY")
    print("==============================")
    print("")

    memory = load_memory()

    print(
        json.dumps(
            memory,
            ensure_ascii=False,
            indent=2
        )
    )

    print("")
    print("==============================")

    events = memory.get(
        "events",
        []
    )

    if len(events) != 1:

        raise RuntimeError(
            "Memory test failed: "
            "expected exactly one event."
        )

    event = events[0]

    if event.get(
        "deadline"
    ) != "2026-09-21":

        raise RuntimeError(
            "Memory test failed: "
            "deadline was not updated."
        )

    if len(
        event.get(
            "timeline",
            []
        )
    ) != 2:

        raise RuntimeError(
            "Memory test failed: "
            "timeline does not contain "
            "two entries."
        )

    print(
        "MEMORY TEST: SUCCESS"
    )


if __name__ == "__main__":
    main()



