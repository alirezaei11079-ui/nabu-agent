import re
from urllib.parse import urlparse


# =========================
# TOPICS
# =========================

TOPIC_KEYWORDS = {
    "AIRDROP": [
        "airdrop",
        "air drop",
        "airdrop eligibility",
        "eligible users",
    ],

    "CLAIM": [
        "claim",
        "claim now",
        "claim your",
        "claim rewards",
        "claim tokens",
    ],

    "MINT": [
        "mint is live",
        "mint now",
        "mint your",
        "mint nft",
        "minting is live",
        "free mint",
    ],

    "TESTNET": [
        "testnet",
        "test net",
        "test network",
    ],

    "MAINNET": [
        "mainnet",
        "main net",
        "mainnet launch",
    ],

    "LISTING": [
        "listing",
        "listed on",
        "now listed",
        "trading starts",
    ],

    "WHITELIST": [
        "whitelist",
        "allowlist",
        "allow list",
        "wl spot",
        "wl spots",
    ],

    "SNAPSHOT": [
        "snapshot",
        "snapshot taken",
        "snapshot date",
    ],

    "GIVEAWAY": [
        "giveaway",
        "give away",
        "winners",
        "winner",
    ],

    "QUEST": [
        "quest",
        "quests",
        "task",
        "tasks",
        "campaign",
    ],

    "COMPETITION": [
        "competition",
        "contest",
        "tournament",
        "challenge",
        "مسابقه",
        "مسابقه داریم",
        "رقابت",
    ],

    "PARTNERSHIP": [
        "partnership",
        "partnered",
        "partner",
    ],

    "FUNDING": [
        "funding",
        "raised",
        "investment",
        "investors",
    ],

    "ANNOUNCEMENT": [
        "announcement",
        "announcing",
        "introducing",
    ],
}


# =========================
# ACTION PATTERNS
# =========================

ACTION_PATTERNS = {

    "CLAIM": [
        r"\bclaim\b.{0,80}\b(now|today|rewards?|tokens?)\b",
        r"\bclaim your\b",
        r"\bclaim rewards?\b",
    ],

    "CONNECT_WALLET": [
        r"\bconnect\b.{0,40}\bwallet\b",
        r"\bconnect your wallet\b",
    ],

    "REGISTER": [
        r"\bregister\b",
        r"\bsign up\b",
        r"\bsignup\b",
        r"\bregistration\b",
        r"ثبت نام",
        r"ثبت‌نام",
    ],

    "DEPOSIT": [
        r"\bdeposit\b",
        r"\bdeposit funds\b",
    ],

    "WITHDRAW": [
        r"\bwithdraw\b",
        r"\bwithdrawal\b",
    ],

    "STAKE": [
        r"\bstake\b",
        r"\bstaking\b",
    ],

    "BRIDGE": [
        r"\bbridge\b",
        r"\bbridge your\b",
    ],

    "VOTE": [
        r"\bvote\b",
        r"\bvoting\b",
        r"\bgovernance vote\b",
    ],

    "VERIFY": [
        r"\bverify\b",
        r"\bverification\b",
    ],

    "APPLY": [
        r"\bapply\b",
        r"\bapplications?\b",
    ],

    "MINT": [
        r"\bmint\b.{0,50}\bnow\b",
        r"\bmint\b.{0,50}\blive\b",
        r"\bmint your\b",
        r"\bfree mint\b",
    ],

    "BUY": [
        r"\bbuy now\b",
        r"\bbuy\b.{0,40}\btoken\b",
        r"\bbuy\b.{0,40}\bcoin\b",
    ],

    "SELL": [
        r"\bsell now\b",
        r"\bsell\b.{0,40}\btoken\b",
        r"\bsell\b.{0,40}\bcoin\b",
    ],

    "JOIN": [
        r"\bjoin\b",
        r"\bjoin us\b",
        r"\bjoin the\b",
        r"شرکت کنید",
        r"شرکت کن",
        r"وارد مسابقه شوید",
        r"وارد مسابقه شو",
        r"در مسابقه شرکت",
    ],

    "FOLLOW": [
        r"\bfollow\b",
        r"\bfollow us\b",
    ],

    "LIKE": [
        r"\blike\b",
        r"\blike this\b",
    ],

    "REPOST": [
        r"\brepost\b",
        r"\bretweet\b",
        r"\bretweet this\b",
    ],
}


# =========================
# RISK
# =========================

HIGH_RISK_ACTIONS = {
    "DEPOSIT",
    "WITHDRAW",
    "BUY",
    "SELL",
}

MEDIUM_RISK_ACTIONS = {
    "CONNECT_WALLET",
    "MINT",
    "CLAIM",
    "STAKE",
    "BRIDGE",
    "VOTE",
}

LOW_RISK_ACTIONS = {
    "REGISTER",
    "VERIFY",
    "APPLY",
    "JOIN",
    "FOLLOW",
    "LIKE",
    "REPOST",
}


# =========================
# PRIORITY
# =========================

HIGH_PRIORITY_TOPICS = {
    "AIRDROP",
    "CLAIM",
    "MAINNET",
    "LISTING",
    "SNAPSHOT",
}

MEDIUM_PRIORITY_TOPICS = {
    "MINT",
    "TESTNET",
    "WHITELIST",
    "GIVEAWAY",
    "QUEST",
    "COMPETITION",
    "FUNDING",
    "PARTNERSHIP",
}


# =========================
# HELPERS
# =========================

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


def find_topics(text):

    text_lower = text.lower()

    topics = []

    for topic, keywords in TOPIC_KEYWORDS.items():

        for keyword in keywords:

            if keyword.lower() in text_lower:
                topics.append(topic)
                break

    return topics


def detect_actions(text):

    text_lower = text.lower()

    actions = []

    for action, patterns in ACTION_PATTERNS.items():

        for pattern in patterns:

            if re.search(pattern, text_lower):
                actions.append(action)
                break

    return actions


def extract_links(text):

    return re.findall(
        r"https?://[^\s]+",
        text
    )


def classify_links(links):

    result = []

    for link in links:

        try:

            domain = urlparse(link).netloc.lower()

            result.append({
                "url": link,
                "domain": domain,
            })

        except Exception:
            pass

    return result


# =========================
# DEADLINE DETECTION
# =========================

def detect_deadline(text):

    patterns = [

        # English
        r"\b\d{1,2}:\d{2}\s?(am|pm)?\b",
        r"\b(today|tonight|tomorrow)\b",
        r"\b\d{1,2}\s?(minutes?|hours?)\b",
        r"\bdeadline\b",
        r"\bends?\b",
        r"\bends?\s+\w+",

        # Persian
        r"امروز",
        r"امشب",
        r"فردا",
        r"ساعت\s*\d{1,2}",
        r"\d+\s*دقیقه",
        r"\d+\s*ساعت",
        r"مهلت",
        r"تا\s+\d+",
    ]

    matches = []

    for pattern in patterns:

        found = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        for item in found:

            if isinstance(item, tuple):

                item = " ".join(
                    x for x in item if x
                )

            matches.append(item)

    return list(dict.fromkeys(matches))


# =========================
# PRIORITY
# =========================

def determine_priority(topics, actions):

    if (
        "DEPOSIT" in actions
        or "WITHDRAW" in actions
        or "BUY" in actions
        or "SELL" in actions
    ):
        return "🔴 HIGH"

    if any(
        topic in HIGH_PRIORITY_TOPICS
        for topic in topics
    ):
        return "🔴 HIGH"

    if any(
        topic in MEDIUM_PRIORITY_TOPICS
        for topic in topics
    ):
        return "🟠 MEDIUM"

    if actions:
        return "🟠 MEDIUM"

    return "🟢 LOW"


# =========================
# RISK
# =========================

def determine_risk(actions):

    if any(
        action in HIGH_RISK_ACTIONS
        for action in actions
    ):
        return "🔴 HIGH"

    if any(
        action in MEDIUM_RISK_ACTIONS
        for action in actions
    ):
        return "🟠 MEDIUM"

    if any(
        action in LOW_RISK_ACTIONS
        for action in actions
    ):
        return "🟢 LOW"

    return "🟢 LOW"


# =========================
# PRIMARY ACTION
# =========================

def determine_action(actions):

    if not actions:
        return None

    priority = [
        "DEPOSIT",
        "WITHDRAW",
        "BUY",
        "SELL",
        "CONNECT_WALLET",
        "CLAIM",
        "MINT",
        "STAKE",
        "BRIDGE",
        "VOTE",
        "REGISTER",
        "VERIFY",
        "APPLY",
        "JOIN",
        "FOLLOW",
        "REPOST",
        "LIKE",
    ]

    for action in priority:

        if action in actions:
            return action

    return actions[0]


# =========================
# STEPS
# =========================

def build_steps(action):

    steps = {

        "CLAIM": [
            "1. فقط از لینک رسمی پروژه وارد صفحه Claim شو.",
            "2. دامنه سایت را بررسی کن.",
            "3. شرایط و مقدار Claim را بررسی کن.",
            "4. شبکه و Wallet صحیح را انتخاب کن.",
            "5. قبل از تأیید، جزئیات تراکنش را بررسی کن.",
        ],

        "CONNECT_WALLET": [
            "1. فقط از سایت رسمی پروژه وارد شو.",
            "2. دامنه سایت را دقیق بررسی کن.",
            "3. Wallet را فقط در صورت معتبر بودن سایت متصل کن.",
            "4. اگر درخواست امضای مشکوک بود، تأیید نکن.",
        ],

        "MINT": [
            "1. سایت رسمی پروژه را باز کن.",
            "2. قرارداد و شبکه را بررسی کن.",
            "3. قیمت Mint و Gas را بررسی کن.",
            "4. جزئیات تراکنش Wallet را قبل از امضا بررسی کن.",
        ],

        "STAKE": [
            "1. قرارداد رسمی Staking را پیدا کن.",
            "2. سود و مدت قفل را بررسی کن.",
            "3. کارمزدها و ریسک قرارداد را بررسی کن.",
            "4. فقط پس از تأیید اطلاعات اقدام کن.",
        ],

        "BRIDGE": [
            "1. شبکه مبدأ و مقصد را بررسی کن.",
            "2. Bridge رسمی را پیدا کن.",
            "3. کارمزد و مقدار دریافتی را بررسی کن.",
            "4. ابتدا با مقدار بسیار کم تست کن.",
        ],

        "DEPOSIT": [
            "1. پلتفرم رسمی را بررسی کن.",
            "2. شبکه و آدرس مقصد را کنترل کن.",
            "3. ابتدا مقدار بسیار کمی ارسال کن.",
            "4. پس از تأیید، انتقال اصلی را انجام بده.",
        ],

        "WITHDRAW": [
            "1. شبکه مقصد را بررسی کن.",
            "2. آدرس Wallet را چند بار کنترل کن.",
            "3. کارمزد را بررسی کن.",
            "4. ابتدا با مقدار کم تست کن.",
        ],

        "BUY": [
            "1. بازار و صرافی موردنظر را مشخص کن.",
            "2. قرارداد رسمی دارایی را بررسی کن.",
            "3. قیمت، نقدشوندگی و کارمزد را بررسی کن.",
            "4. قبل از تأیید سفارش، جزئیات را کنترل کن.",
        ],

        "SELL": [
            "1. بازار و صرافی را بررسی کن.",
            "2. قیمت و نقدشوندگی را بررسی کن.",
            "3. مقدار فروش را مشخص کن.",
            "4. قیمت نهایی سفارش را کنترل کن.",
        ],

        "JOIN": [
            "1. لینک رسمی فعالیت را بررسی کن.",
            "2. شرایط شرکت را بخوان.",
            "3. مراحل لازم را انجام بده.",
        ],

        "REGISTER": [
            "1. صفحه رسمی ثبت‌نام را باز کن.",
            "2. دامنه سایت را بررسی کن.",
            "3. اطلاعات لازم را تکمیل کن.",
        ],

        "FOLLOW": [
            "1. اکانت رسمی را بررسی کن.",
            "2. فقط اکانت تأییدشده یا رسمی را Follow کن.",
        ],

        "REPOST": [
            "1. مطمئن شو پست متعلق به اکانت رسمی است.",
            "2. در صورت معتبر بودن، Repost کن.",
        ],
    }

    return steps.get(
        action,
        [
            "1. منبع رسمی پیام را بررسی کن.",
            "2. مشخص کن آیا اقدام عملی لازم است.",
            "3. قبل از اقدام، اطلاعات را دوباره بررسی کن.",
        ],
    )


# =========================
# MAIN ANALYZER
# =========================

def analyze_message(text, link):

    text = clean_text(text)

    topics = find_topics(text)

    actions = detect_actions(text)

    action = determine_action(actions)

    links = extract_links(text)

    link_info = classify_links(links)

    deadlines = detect_deadline(text)

    priority = determine_priority(
        topics,
        actions
    )

    risk = determine_risk(actions)

    action_required = action is not None

    financial_action = any(
        action_name in actions
        for action_name in [
            "DEPOSIT",
            "WITHDRAW",
            "BUY",
            "SELL",
            "MINT",
            "CLAIM",
            "STAKE",
            "BRIDGE",
        ]
    )

    return {
        "priority": priority,
        "risk": risk,
        "topics": topics,
        "actions": actions,
        "action": action,
        "action_required": action_required,
        "financial_action": financial_action,
        "links": link_info,
        "deadlines": deadlines,
        "steps": (
            build_steps(action)
            if action_required
            else []
        ),
        "text": text,
        "link": link,
    }


# =========================
# TELEGRAM FORMAT
# =========================

def format_alert(result):

    message = (
        "🤖 NABU INTELLIGENCE ALERT\n\n"
        f"اهمیت: {result['priority']}\n"
        f"⚠️ ریسک: {result['risk']}\n"
    )

    if result["action_required"]:

        message += (
            "\n⚡ اقدام لازم: بله\n"
            f"🎯 اقدام: {result['action']}\n"
        )

    else:

        message += (
            "\nℹ️ اقدام لازم: خیر\n"
        )

    if result["topics"]:

        message += (
            "\n📌 موضوع:\n"
            + ", ".join(result["topics"])
            + "\n"
        )

    if result["deadlines"]:

        message += (
            "\n⏰ زمان/Deadline احتمالی:\n"
            + ", ".join(result["deadlines"])
            + "\n"
        )

    message += (
        "\n📝 پیام:\n"
        + result["text"][:2500]
        + "\n"
    )

    if result["action_required"]:

        message += (
            "\n🛠 مراحل پیشنهادی:\n"
        )

        for step in result["steps"]:

            message += step + "\n"

    message += (
        "\n💰 اقدام مالی/Wallet: "
        + (
            "بله"
            if result["financial_action"]
            else "خیر"
        )
        + "\n"
    )

    if result["links"]:

        message += "\n🔗 لینک‌های شناسایی‌شده:\n"

        for item in result["links"][:5]:

            message += (
                f"- {item['domain']}\n"
            )

    message += (
        "\n📎 منبع:\n"
        + result["link"]
    )

    message += (
        "\n\n⚠️ تحلیل خودکار است. "
        "قبل از هر اقدام مالی، اتصال Wallet "
        "یا امضای تراکنش، منبع رسمی و "
        "جزئیات را بررسی کن."
    )

    return message


