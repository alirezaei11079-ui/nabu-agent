import json
import os
from datetime import datetime, timezone


MEMORY_FILE = "event_memory.json"


def now_iso():
    return datetime.now(
        timezone.utc
    ).isoformat()


def load_memory():

    if not os.path.exists(
        MEMORY_FILE
    ):
        return {
            "events": []
        }

    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return {
            "events": []
        }


def save_memory(memory):

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            memory,
            file,
            ensure_ascii=False,
            indent=2
        )


def normalize(value):

    if value is None:
        return ""

    return str(value).strip().lower()


def event_similarity(ai_result, event):

    score = 0

    project = normalize(
        ai_result.get("project")
    )

    old_project = normalize(
        event.get("project")
    )

    category = normalize(
        ai_result.get("category")
    )

    old_category = normalize(
        event.get("category")
    )

    event_name = normalize(
        ai_result.get("event")
    )

    old_event = normalize(
        event.get("event")
    )

    # Project match
    if (
        project
        and old_project
        and project == old_project
    ):
        score += 5

    # Category match
    if (
        category
        and old_category
        and category == old_category
    ):
        score += 2

    # Event similarity
    if (
        event_name
        and old_event
        and (
            event_name == old_event
            or event_name in old_event
            or old_event in event_name
        )
    ):
        score += 4

    # Reward match
    reward = normalize(
        ai_result.get("reward")
    )

    old_reward = normalize(
        event.get("reward")
    )

    if (
        reward
        and old_reward
        and reward != "unknown"
        and reward == old_reward
    ):
        score += 2

    return score


def find_related_event(
    ai_result,
    memory
):

    best_event = None
    best_score = 0

    for event in memory.get(
        "events",
        []
    ):

        score = event_similarity(
            ai_result,
            event
        )

        if score > best_score:

            best_score = score
            best_event = event

    if best_score >= 5:

        return best_event

    return None


def clean_value(value):

    if value is None:
        return "unknown"

    value = str(value).strip()

    if not value:
        return "unknown"

    return value


def create_event(
    ai_result,
    source_url
):

    timestamp = now_iso()

    return {
        "event_id": (
            f"event-"
            f"{int(datetime.now().timestamp())}"
        ),

        "project": clean_value(
            ai_result.get("project")
        ),

        "category": clean_value(
            ai_result.get("category")
        ),

        "event": clean_value(
            ai_result.get("event")
        ),

        "status": "ACTIVE",

        "first_seen": timestamp,

        "last_updated": timestamp,

        "deadline": clean_value(
            ai_result.get("deadline")
        ),

        "cost": clean_value(
            ai_result.get("cost")
        ),

        "network": clean_value(
            ai_result.get("network")
        ),

        "contract_address": clean_value(
            ai_result.get(
                "contract_address"
            )
        ),

        "wallet_required": clean_value(
            ai_result.get(
                "wallet_required"
            )
        ),

        "financial_action": bool(
            ai_result.get(
                "financial_action",
                False
            )
        ),

        "eligibility": clean_value(
            ai_result.get(
                "eligibility"
            )
        ),

        "reward": clean_value(
            ai_result.get(
                "reward"
            )
        ),

        "requirements": ai_result.get(
            "requirements",
            []
        ),

        "unknowns": ai_result.get(
            "unknowns",
            []
        ),

        "risk_notes": ai_result.get(
            "risk_notes",
            []
        ),

        "source_links": [
            source_url
        ] if source_url else [],

        "timeline": [
            {
                "timestamp": timestamp,
                "type": "FIRST_SEEN",
                "summary": ai_result.get(
                    "summary",
                    ""
                ),
                "source": source_url
            }
        ]
    }


def update_event(
    event,
    ai_result,
    source_url
):

    timestamp = now_iso()

    changed_fields = []

    fields = [
        "deadline",
        "cost",
        "network",
        "contract_address",
        "wallet_required",
        "eligibility",
        "reward"
    ]

    for field in fields:

        new_value = clean_value(
            ai_result.get(field)
        )

        old_value = clean_value(
            event.get(field)
        )

        # Never overwrite known information
        # with unknown information.
        if (
            new_value != "unknown"
            and new_value != old_value
        ):

            event[field] = new_value

            changed_fields.append(
                field
            )

    # Update boolean only when meaningful
    if ai_result.get(
        "financial_action"
    ):

        if not event.get(
            "financial_action",
            False
        ):

            event[
                "financial_action"
            ] = True

            changed_fields.append(
                "financial_action"
            )

    # Merge requirements
    for item in ai_result.get(
        "requirements",
        []
    ):

        if item not in event[
            "requirements"
        ]:

            event[
                "requirements"
            ].append(item)

    # Merge unknowns
    for item in ai_result.get(
        "unknowns",
        []
    ):

        if item not in event[
            "unknowns"
        ]:

            event[
                "unknowns"
            ].append(item)

    # Merge risks
    for item in ai_result.get(
        "risk_notes",
        []
    ):

        if item not in event[
            "risk_notes"
        ]:

            event[
                "risk_notes"
            ].append(item)

    # Add source
    if (
        source_url
        and source_url not in event[
            "source_links"
        ]
    ):

        event[
            "source_links"
        ].append(
            source_url
        )

    event[
        "last_updated"
    ] = timestamp

    timeline_entry = {
        "timestamp": timestamp,
        "type": "UPDATE",
        "summary": ai_result.get(
            "summary",
            ""
        ),
        "source": source_url,
        "changed_fields": changed_fields
    }

    event[
        "timeline"
    ].append(
        timeline_entry
    )

    return changed_fields


def process_ai_event(
    ai_result,
    source_url
):

    memory = load_memory()

    event = find_related_event(
        ai_result,
        memory
    )

    if event:

        changed_fields = update_event(
            event,
            ai_result,
            source_url
        )

        save_memory(
            memory
        )

        return {
            "type": "UPDATE",
            "event": event,
            "changed_fields": changed_fields
        }

    new_event = create_event(
        ai_result,
        source_url
    )

    memory.setdefault(
        "events",
        []
    ).append(
        new_event
    )

    save_memory(
        memory
    )

    return {
        "type": "NEW",
        "event": new_event,
        "changed_fields": []
    }


def format_memory_update(
    result
):

    event = result[
        "event"
    ]

    lines = [
        "🧠 NABU MEMORY",
        "",
        f"📌 پروژه: {event.get('project', 'unknown')}",
        f"🎯 رویداد: {event.get('event', 'unknown')}",
        f"📊 وضعیت: {event.get('status', 'ACTIVE')}",
        "",
    ]

    if result["type"] == "NEW":

        lines.extend([
            "🆕 رویداد جدید شناسایی شد.",
            "",
            "📅 اولین مشاهده:",
            event.get(
                "first_seen",
                ""
            )
        ])

    else:

        lines.extend([
            "🔄 ادامه یک رویداد قبلی شناسایی شد.",
            "",
            "🕐 آخرین بروزرسانی:",
            event.get(
                "last_updated",
                ""
            )
        ])

        changed = result.get(
            "changed_fields",
            []
        )

        if changed:

            lines.extend([
                "",
                "📝 اطلاعات جدید:"
            ])

            for field in changed:

                lines.append(
                    f"• {field}"
                )

        else:

            lines.extend([
                "",
                "ℹ️ اطلاعات جدید مهمی نسبت به "
                "رویداد قبلی پیدا نشد."
            ])

    lines.extend([
        "",
        "📌 وضعیت فعلی",
        f"⏰ مهلت: {event.get('deadline', 'unknown')}",
        f"💰 هزینه: {event.get('cost', 'unknown')}",
        f"🌐 شبکه: {event.get('network', 'unknown')}",
        f"📜 قرارداد: {event.get('contract_address', 'unknown')}",
        f"👛 کیف پول: {event.get('wallet_required', 'unknown')}",
        f"🎁 پاداش: {event.get('reward', 'unknown')}",
    ])

    return "\n".join(
        lines
    )


