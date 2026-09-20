import os
import json

from google import genai
from google.genai import types


MODEL_NAME = "gemini-2.5-flash-lite"


def analyze_with_ai(text, source_url=""):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    client = genai.Client(
        api_key=api_key
    )

    prompt = f"""
تو تحلیلگر هوشمند یک Web3 Monitoring Agent هستی.

پست زیر را با دقت بسیار زیاد تحلیل کن.

مهم‌ترین قانون:
هرگز اطلاعاتی را که در متن وجود ندارد حدس نزن.

اگر اطلاعاتی در پست وجود ندارد:
- رشته خالی ""
- false
- آرایه خالی []
- یا "unknown"
استفاده کن.

هرگز این موارد را اختراع نکن:
- قیمت
- مهلت
- شبکه
- Contract Address
- نام پروژه
- مقدار پاداش
- شرایط احراز صلاحیت
- نیاز به Wallet
- هزینه Mint
- لینک

پست:

{text}

منبع:

{source_url}

تحلیل باید فارسی باشد.

category فقط یکی از این موارد باشد:

ANNOUNCEMENT
GIVEAWAY
WL
MINT
CLAIM
AIRDROP
QUEST
COMPETITION
PARTNERSHIP
TOKEN
NFT
UPDATE
OTHER

urgency فقط یکی از این موارد باشد:

LOW
MEDIUM
HIGH
CRITICAL

summary:
خلاصه کوتاه و دقیق فارسی.

meaning:
توضیح بده نویسنده دقیقاً چه چیزی می‌گوید.

actions:
فقط اقداماتی را بنویس که در متن صراحتاً درخواست شده یا به‌وضوح از متن قابل برداشت است.

requirements:
شرایط شرکت یا استفاده که در متن آمده.

unknowns:
اطلاعات مهمی که برای تصمیم‌گیری لازم هستند ولی در متن وجود ندارند.

risk_notes:
مواردی که قبل از اقدام باید بررسی شوند.

user_steps:
مراحل عملی بر اساس اطلاعات موجود.
اگر اطلاعات کافی نیست، مرحله‌ای را حدس نزن.

خروجی فقط JSON معتبر باشد.
"""


    response_schema = {
        "type": "OBJECT",
        "properties": {
            "summary": {
                "type": "STRING"
            },
            "meaning": {
                "type": "STRING"
            },
            "category": {
                "type": "STRING"
            },
            "project": {
                "type": "STRING"
            },
            "event": {
                "type": "STRING"
            },
            "action_required": {
                "type": "BOOLEAN"
            },
            "actions": {
                "type": "ARRAY",
                "items": {
                    "type": "STRING"
                }
            },
            "urgency": {
                "type": "STRING"
            },
            "deadline": {
                "type": "STRING"
            },
            "cost": {
                "type": "STRING"
            },
            "network": {
                "type": "STRING"
            },
            "contract_address": {
                "type": "STRING"
            },
            "wallet_required": {
                "type": "BOOLEAN"
            },
            "financial_action": {
                "type": "BOOLEAN"
            },
            "eligibility": {
                "type": "STRING"
            },
            "reward": {
                "type": "STRING"
            },
            "links": {
                "type": "ARRAY",
                "items": {
                    "type": "STRING"
                }
            },
            "requirements": {
                "type": "ARRAY",
                "items": {
                    "type": "STRING"
                }
            },
            "unknowns": {
                "type": "ARRAY",
                "items": {
                    "type": "STRING"
                }
            },
            "risk_notes": {
                "type": "ARRAY",
                "items": {
                    "type": "STRING"
                }
            },
            "user_steps": {
                "type": "ARRAY",
                "items": {
                    "type": "STRING"
                }
            }
        },
        "required": [
            "summary",
            "meaning",
            "category",
            "project",
            "event",
            "action_required",
            "actions",
            "urgency",
            "deadline",
            "cost",
            "network",
            "contract_address",
            "wallet_required",
            "financial_action",
            "eligibility",
            "reward",
            "links",
            "requirements",
            "unknowns",
            "risk_notes",
            "user_steps"
        ]
    }


    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
                response_mime_type="application/json",
                response_schema=response_schema,
            ),
        )

    except Exception as error:

        raise RuntimeError(
            f"Gemini API error: {error}"
        )


    if not response.text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )


    try:

        result = json.loads(
            response.text
        )

    except json.JSONDecodeError as error:

        raise RuntimeError(
            f"Gemini returned invalid JSON: {error}"
        )


    return result


def format_ai_analysis(result):

    lines = [
        "🤖 AI INTELLIGENCE",
        "",
        f"📌 موضوع: {result.get('category', 'UNKNOWN')}",
        f"🧠 پروژه: {result.get('project') or 'نامشخص'}",
        f"🎯 رویداد: {result.get('event') or 'نامشخص'}",
        f"⚡ فوریت: {result.get('urgency', 'LOW')}",
        "",
        "📝 خلاصه",
        result.get(
            "summary",
            "اطلاعات کافی وجود ندارد."
        ),
        "",
        "🔎 منظور پست",
        result.get(
            "meaning",
            "اطلاعات کافی وجود ندارد."
        ),
    ]


    if result.get("actions"):

        lines.extend([
            "",
            "🎯 اقدامات",
        ])

        for action in result["actions"]:

            lines.append(
                f"• {action}"
            )


    if result.get("requirements"):

        lines.extend([
            "",
            "📋 شرایط",
        ])

        for item in result["requirements"]:

            lines.append(
                f"• {item}"
            )


    if result.get("deadline"):

        lines.append(
            f"⏰ مهلت: {result['deadline']}"
        )


    if result.get("cost"):

        lines.append(
            f"💰 هزینه: {result['cost']}"
        )


    if result.get("network"):

        lines.append(
            f"🌐 شبکه: {result['network']}"
        )


    if result.get("contract_address"):

        lines.append(
            f"📜 قرارداد: {result['contract_address']}"
        )


    wallet_status = (
        "بله"
        if result.get("wallet_required")
        else "خیر/نامشخص"
    )

    lines.append(
        f"👛 نیاز به کیف پول: {wallet_status}"
    )


    if result.get("financial_action"):

        lines.append(
            "💸 اقدام مالی: بله"
        )


    if result.get("reward"):

        lines.append(
            f"🎁 پاداش: {result['reward']}"
        )


    if result.get("eligibility"):

        lines.append(
            f"👤 شرایط شرکت: {result['eligibility']}"
        )


    if result.get("unknowns"):

        lines.extend([
            "",
            "❓ اطلاعات نامشخص",
        ])

        for item in result["unknowns"]:

            lines.append(
                f"• {item}"
            )


    if result.get("risk_notes"):

        lines.extend([
            "",
            "⚠️ موارد قابل بررسی",
        ])

        for item in result["risk_notes"]:

            lines.append(
                f"• {item}"
            )


    if result.get("user_steps"):

        lines.extend([
            "",
            "📱 مراحل پیشنهادی",
        ])

        for index, step in enumerate(
            result["user_steps"],
            start=1
        ):

            lines.append(
                f"{index}. {step}"
            )


    return "\n".join(
        lines
    )
