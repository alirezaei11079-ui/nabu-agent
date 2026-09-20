import os
import json

from google import genai


MODEL_NAME = "gemini-3.5-flash-lite"


RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {
            "type": "string"
        },
        "meaning": {
            "type": "string"
        },
        "category": {
            "type": "string"
        },
        "project": {
            "type": "string"
        },
        "event": {
            "type": "string"
        },
        "action_required": {
            "type": "boolean"
        },
        "actions": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "urgency": {
            "type": "string"
        },
        "deadline": {
            "type": "string"
        },
        "cost": {
            "type": "string"
        },
        "network": {
            "type": "string"
        },
        "contract_address": {
            "type": "string"
        },
        "wallet_required": {
            "type": "boolean"
        },
        "financial_action": {
            "type": "boolean"
        },
        "eligibility": {
            "type": "string"
        },
        "reward": {
            "type": "string"
        },
        "links": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "requirements": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "unknowns": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "risk_notes": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "user_steps": {
            "type": "array",
            "items": {
                "type": "string"
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


def analyze_with_ai(text, source_url=""):

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )


    client = genai.Client(
        api_key=api_key
    )


    prompt = f"""
تو تحلیلگر هوشمند یک Web3 Intelligence Agent هستی.

پست زیر را با دقت بسیار زیاد تحلیل کن.

هدف تو این است که به کاربر توضیح بدهی:
1. این پست دقیقاً چه می‌گوید؟
2. موضوع چیست؟
3. آیا کاربر باید کاری انجام دهد؟
4. اگر باید کاری انجام دهد، دقیقاً چه کاری؟
5. چه اطلاعات مهمی هنوز مشخص نیست؟
6. قبل از اقدام چه چیزهایی باید بررسی شوند؟

قانون بسیار مهم:

هرگز چیزی را که در متن وجود ندارد حدس نزن.

اگر اطلاعاتی در پست وجود ندارد، آن را unknown در نظر بگیر.

هرگز این موارد را اختراع نکن:
- قیمت
- هزینه
- Deadline
- شبکه
- Contract Address
- نام پروژه
- مقدار پاداش
- شرایط احراز صلاحیت
- نیاز به Wallet
- لینک
- امنیت قرارداد

اگر متن فقط یک اطلاعیه است، آن را به عنوان اقدام فوری معرفی نکن.

اگر متن درخواست Follow، Like، Repost، Comment یا ارسال آدرس EVM دارد،
فقط همان اقدامات را گزارش کن.

اگر متن درخواست اتصال Wallet، Mint، Claim یا پرداخت دارد،
آن را به‌عنوان اقدام حساس مشخص کن.

اگر متن درخواست Seed Phrase، Recovery Phrase یا Private Key دارد،
ریسک بسیار بالا را گزارش کن.

اگر اطلاعات کافی برای تصمیم‌گیری وجود ندارد،
صراحتاً بگو چه اطلاعاتی کم است.

پست:

{text}

منبع:

{source_url}


دسته‌بندی category فقط یکی از این موارد باشد:

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


تمام توضیحات باید فارسی باشند.

summary:
خلاصه کوتاه و دقیق.

meaning:
منظور واقعی نویسنده را توضیح بده.

actions:
فقط اقداماتی که در متن درخواست شده یا به‌وضوح از متن قابل برداشت است.

requirements:
شرایط شرکت یا استفاده که در متن آمده.

unknowns:
اطلاعات مهمی که وجود ندارد.

risk_notes:
مواردی که قبل از اقدام باید بررسی شوند.

user_steps:
مراحل عملی فقط بر اساس اطلاعات موجود.


فقط JSON معتبر تولید کن.
"""


    try:

        interaction = client.interactions.create(

            model=MODEL_NAME,

            input=prompt,

            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": RESPONSE_SCHEMA
            }
        )

    except Exception as error:

        raise RuntimeError(
            f"Gemini API error: {error}"
        )


    output = getattr(
        interaction,
        "output_text",
        None
    )


    if not output:

        raise RuntimeError(
            "Gemini returned an empty response."
        )


    try:

        return json.loads(
            output
        )

    except json.JSONDecodeError as error:

        raise RuntimeError(
            f"Gemini returned invalid JSON: {error}"
        )


def format_ai_analysis(result):

    lines = [

        "🤖 AI INTELLIGENCE",
        "",

        f"📌 موضوع: "
        f"{result.get('category', 'UNKNOWN')}",

        f"🧠 پروژه: "
        f"{result.get('project') or 'نامشخص'}",

        f"🎯 رویداد: "
        f"{result.get('event') or 'نامشخص'}",

        f"⚡ فوریت: "
        f"{result.get('urgency', 'LOW')}",

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
        )
    ]


    if result.get("actions"):

        lines.extend([
            "",
            "🎯 اقدامات"
        ])

        for action in result["actions"]:

            lines.append(
                f"• {action}"
            )


    if result.get("requirements"):

        lines.extend([
            "",
            "📋 شرایط"
        ])

        for item in result["requirements"]:

            lines.append(
                f"• {item}"
            )


    if result.get("deadline"):

        lines.append(
            f"⏰ مهلت: "
            f"{result['deadline']}"
        )


    if result.get("cost"):

        lines.append(
            f"💰 هزینه: "
            f"{result['cost']}"
        )


    if result.get("network"):

        lines.append(
            f"🌐 شبکه: "
            f"{result['network']}"
        )


    if result.get("contract_address"):

        lines.append(
            f"📜 قرارداد: "
            f"{result['contract_address']}"
        )


    if result.get("wallet_required"):

        lines.append(
            "👛 نیاز به کیف پول: بله"
        )

    else:

        lines.append(
            "👛 نیاز به کیف پول: خیر/نامشخص"
        )


    if result.get("financial_action"):

        lines.append(
            "💸 اقدام مالی: بله"
        )


    if result.get("reward"):

        lines.append(
            f"🎁 پاداش: "
            f"{result['reward']}"
        )


    if result.get("eligibility"):

        lines.append(
            f"👤 شرایط شرکت: "
            f"{result['eligibility']}"
        )


    if result.get("unknowns"):

        lines.extend([
            "",
            "❓ اطلاعات نامشخص"
        ])

        for item in result["unknowns"]:

            lines.append(
                f"• {item}"
            )


    if result.get("risk_notes"):

        lines.extend([
            "",
            "⚠️ موارد قابل بررسی"
        ])

        for item in result["risk_notes"]:

            lines.append(
                f"• {item}"
            )


    if result.get("user_steps"):

        lines.extend([
            "",
            "📱 مراحل پیشنهادی"
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
