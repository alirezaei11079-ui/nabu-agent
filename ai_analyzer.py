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
            "type": "string"
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

پست زیر را دقیق و Evidence-Based تحلیل کن.

قانون اصلی:

هر چیزی که گزارش می‌کنی باید یکی از این سه حالت را داشته باشد:

1. EXPLICIT
اطلاعات مستقیماً در متن آمده است.

2. IMPLIED
اطلاعات از متن به‌صورت منطقی قابل برداشت است.

3. UNKNOWN
اطلاعات در متن وجود ندارد و نباید حدس زده شود.

اگر مطمئن نیستی، UNKNOWN انتخاب کن.

هرگز اطلاعات زیر را اختراع نکن:

- قیمت
- هزینه
- Deadline
- شبکه
- Contract Address
- نام پروژه
- مقدار پاداش
- شرایط شرکت
- نیاز به Wallet
- امنیت قرارداد
- اعتبار پروژه
- لینک رسمی

تفاوت بسیار مهم:

داشتن یا ارسال EVM Address
به معنی اتصال Wallet نیست.

اگر متن فقط درخواست EVM Address دارد:

wallet_required = "UNKNOWN"

اگر صراحتاً نوشته:
Connect Wallet
یا
Connect your wallet

آنگاه:

wallet_required = "YES"

اگر صراحتاً گفته باشد Wallet لازم نیست:

wallet_required = "NO"


financial_action فقط زمانی true باشد که متن صراحتاً
پرداخت، خرید، ارسال ارز، Deposit، Mint پولی یا اقدام مالی
را درخواست کرده باشد.


در مورد امنیت:

اگر پست فقط یک Giveaway ساده است،
آن را Scam اعلام نکن.

اگر اطلاعات امنیتی کافی نیست،
بنویس که نیاز به بررسی دارد.


درباره Eligibility:

اگر شرایط دقیق در متن نیست،
ننویس "عمومی".

بنویس:
"unknown"


درباره Deadline:

اگر تاریخ یا زمان مشخص نشده،
"unknown"


درباره Cost:

اگر قیمت یا هزینه مشخص نشده،
"unknown"


درباره Network:

اگر شبکه مشخص نشده،
"unknown"


درباره Contract:

اگر Contract Address وجود ندارد،
"unknown"


پست:

{text}

منبع:

{source_url}


category فقط یکی از این موارد:

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


urgency:

LOW
MEDIUM
HIGH
CRITICAL


تمام توضیحات باید فارسی باشند.


summary:
خلاصه دقیق و کوتاه.


meaning:
منظور واقعی پست را توضیح بده.


actions:
فقط اقداماتی که در متن درخواست شده یا
به‌صورت کاملاً واضح قابل برداشت هستند.


requirements:
شرایطی که صراحتاً در متن آمده.


unknowns:
اطلاعات مهمی که در متن وجود ندارد.


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

        "🤖 NABU AI INTELLIGENCE",
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
        "━━━━━━━━━━━━",
        "📝 چی شده؟",
        "━━━━━━━━━━━━",

        result.get(
            "summary",
            "اطلاعات کافی وجود ندارد."
        ),

        "",
        "━━━━━━━━━━━━",
        "🔎 منظور پست",
        "━━━━━━━━━━━━",

        result.get(
            "meaning",
            "اطلاعات کافی وجود ندارد."
        )
    ]


    if result.get("actions"):

        lines.extend([
            "",
            "━━━━━━━━━━━━",
            "🎯 برای شرکت/اقدام",
            "━━━━━━━━━━━━"
        ])

        for index, action in enumerate(
            result["actions"],
            start=1
        ):

            lines.append(
                f"{index}️⃣ {action}"
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


    lines.extend([
        "",
        f"⏰ مهلت: "
        f"{result.get('deadline') or 'نامشخص'}",

        f"💰 هزینه: "
        f"{result.get('cost') or 'نامشخص'}",

        f"🌐 شبکه: "
        f"{result.get('network') or 'نامشخص'}",

        f"📜 قرارداد: "
        f"{result.get('contract_address') or 'نامشخص'}",

        f"👛 اتصال کیف پول: "
        f"{result.get('wallet_required') or 'نامشخص'}",

        f"💸 اقدام مالی: "
        f"{'بله' if result.get('financial_action') else 'خیر/نامشخص'}",

        f"🎁 پاداش: "
        f"{result.get('reward') or 'نامشخص'}",

        f"👤 شرایط شرکت: "
        f"{result.get('eligibility') or 'نامشخص'}"
    ])


    if result.get("unknowns"):

        lines.extend([
            "",
            "━━━━━━━━━━━━",
            "❓ چه چیزهایی مشخص نیست؟",
            "━━━━━━━━━━━━"
        ])

        for item in result["unknowns"]:

            lines.append(
                f"• {item}"
            )


    if result.get("risk_notes"):

        lines.extend([
            "",
            "━━━━━━━━━━━━",
            "⚠️ موارد قابل بررسی",
            "━━━━━━━━━━━━"
        ])

        for item in result["risk_notes"]:

            lines.append(
                f"• {item}"
            )


    if result.get("user_steps"):

        lines.extend([
            "",
            "━━━━━━━━━━━━",
            "📱 مراحل پیشنهادی",
            "━━━━━━━━━━━━"
        ])

        for index, step in enumerate(
            result["user_steps"],
            start=1
        ):

            lines.append(
                f"{index}. {step}"
            )


    lines.extend([
        "",
        "━━━━━━━━━━━━",
        "🧠 نتیجه",
        "━━━━━━━━━━━━"
    ])


    if result.get("financial_action"):

        lines.append(
            "⚠️ قبل از هر اقدام مالی، "
            "اطلاعات پروژه و مقصد را مستقل بررسی کن."
        )

    elif result.get("action_required"):

        lines.append(
            "اقدام غیرمالی از متن شناسایی شده؛ "
            "قبل از انجام مراحل حساس، اطلاعات نامشخص را بررسی کن."
        )

    else:

        lines.append(
            "اقدام فوری از متن شناسایی نشد."
        )


    return "\n".join(
        lines
    )
