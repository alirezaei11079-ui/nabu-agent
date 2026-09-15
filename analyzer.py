import re


HIGH_PRIORITY = [
    "airdrop",
    "claim",
    "listing",
    "listed",
    "launch",
    "mainnet",
    "token launch",
    "snapshot",
    "deadline",
]

MEDIUM_PRIORITY = [
    "partnership",
    "partner",
    "funding",
    "testnet",
    "campaign",
    "whitelist",
    "reward",
    "rewards",
    "mint",
]

ACTION_WORDS = [
    "claim",
    "connect",
    "register",
    "sign up",
    "deposit",
    "withdraw",
    "mint",
    "stake",
    "bridge",
    "vote",
    "verify",
    "apply",
    "buy",
    "sell",
]


def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


def find_matches(text, keywords):
    text_lower = text.lower()

    return [
        keyword
        for keyword in keywords
        if keyword.lower() in text_lower
    ]


def analyze_message(text, link):
    text = clean_text(text)

    high_matches = find_matches(text, HIGH_PRIORITY)
    medium_matches = find_matches(text, MEDIUM_PRIORITY)
    action_matches = find_matches(text, ACTION_WORDS)

    if high_matches:
        priority = "🔴 HIGH"
    elif medium_matches:
        priority = "🟠 MEDIUM"
    else:
        priority = "🟢 LOW"

    if action_matches:
        action_required = True
    else:
        action_required = False

    if action_required:
        steps = build_steps(action_matches)
    else:
        steps = []

    return {
        "priority": priority,
        "action_required": action_required,
        "matched_keywords": high_matches + medium_matches,
        "action_keywords": action_matches,
        "steps": steps,
        "link": link,
        "text": text,
    }


def build_steps(actions):
    steps = []

    if "claim" in actions:
        steps.extend([
            "1. فقط از لینک رسمی پروژه وارد صفحه Claim شو.",
            "2. آدرس سایت و دامنه را بررسی کن.",
            "3. شرایط و مقدار Claim را بررسی کن.",
            "4. شبکه و Wallet درست را انتخاب کن.",
            "5. قبل از تأیید، متن تراکنش و مجوزها را بررسی کن.",
        ])

    if "connect" in actions:
        steps.extend([
            "1. فقط از وب‌سایت رسمی پروژه وارد شو.",
            "2. آدرس سایت را بررسی کن.",
            "3. Wallet را فقط در صورت معتبر بودن سایت متصل کن.",
        ])

    if "register" in actions or "sign up" in actions:
        steps.extend([
            "1. وارد صفحه رسمی ثبت‌نام شو.",
            "2. شرایط ثبت‌نام را بررسی کن.",
            "3. اطلاعات موردنیاز را وارد کن.",
            "4. ثبت‌نام را نهایی کن.",
        ])

    if "stake" in actions:
        steps.extend([
            "1. شبکه و قرارداد رسمی Staking را بررسی کن.",
            "2. نرخ سود و مدت قفل شدن دارایی را بررسی کن.",
            "3. کارمزدها و ریسک قرارداد را بررسی کن.",
            "4. فقط در صورت تأیید اطلاعات، اقدام کن.",
        ])

    if "bridge" in actions:
        steps.extend([
            "1. شبکه مبدأ و مقصد را بررسی کن.",
            "2. Bridge رسمی پروژه را پیدا کن.",
            "3. مقدار انتقال و کارمزد را بررسی کن.",
            "4. ابتدا با مقدار بسیار کم تست کن.",
        ])

    if "buy" in actions:
        steps.extend([
            "1. مشخص کن خرید در کدام صرافی یا شبکه انجام می‌شود.",
            "2. آدرس قرارداد رسمی توکن را بررسی کن.",
            "3. نقدشوندگی و کارمزد را بررسی کن.",
            "4. قبل از خرید، مقدار و قیمت را دوباره کنترل کن.",
        ])

    if "sell" in actions:
        steps.extend([
            "1. صرافی یا بازار موردنظر را بررسی کن.",
            "2. قیمت و نقدشوندگی را بررسی کن.",
            "3. مقدار فروش را مشخص کن.",
            "4. قبل از تأیید سفارش، قیمت نهایی را کنترل کن.",
        ])

    if not steps:
        steps = [
            "1. ابتدا منبع رسمی پیام را بررسی کن.",
            "2. مشخص کن آیا اقدام عملی لازم است.",
            "3. قبل از هر تراکنش، اطلاعات را دوباره بررسی کن.",
        ]

    return steps


def format_alert(result):
    message = "🤖 NABU INTELLIGENCE ALERT\n\n"

    message += f"اهمیت: {result['priority']}\n"

    if result["action_required"]:
        message += "⚡ اقدام لازم: بله\n"
    else:
        message += "ℹ️ اقدام فوری: خیر\n"

    if result["matched_keywords"]:
        message += (
            "\n📌 موارد شناسایی‌شده:\n"
            + ", ".join(result["matched_keywords"])
            + "\n"
        )

    message += "\n📝 پیام:\n"
    message += result["text"][:2500]

    if result["action_required"]:
        message += "\n\n🛠 مراحل پیشنهادی:\n"

        for step in result["steps"]:
            message += f"{step}\n"

    message += f"\n\n🔗 منبع:\n{result['link']}"

    message += (
        "\n\n⚠️ این تحلیل خودکار است. "
        "قبل از هر اقدام مالی یا اتصال Wallet، "
        "منبع رسمی و جزئیات تراکنش را بررسی کن."
    )

    return message
