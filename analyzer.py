import re
from urllib.parse import urlparse


# =========================================================
# KEYWORDS
# =========================================================

TOPIC_KEYWORDS = {
    "MINT": [
        "mint",
        "minting",
        "minted",
    ],

    "CLAIM": [
        "claim",
        "claiming",
        "rewards",
        "reward",
    ],

    "GIVEAWAY": [
        "giveaway",
        "airdrop",
        "wl",
        "whitelist",
        "winner",
        "winners",
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
        "partner",
        "collab",
        "collaboration",
    ],
}


ACTION_KEYWORDS = {
    "CONNECT_WALLET": [
        "connect wallet",
        "connect your wallet",
        "wallet connect",
        "اتصال کیف پول",
    ],

    "MINT": [
        "mint now",
        "mint",
        "minting",
        "mint it",
        "مینت",
    ],

    "CLAIM": [
        "claim now",
        "claim",
        "claim your",
        "دریافت",
        "کلیم",
    ],

    "REGISTER": [
        "register",
        "registration",
        "ثبت نام",
        "ثبت‌نام",
    ],

    "JOIN": [
        "join",
        "join now",
        "participate",
        "شرکت کنید",
        "شرکت کن",
        "وارد مسابقه شوید",
        "وارد مسابقه شو",
        "در مسابقه شرکت",
    ],
}


# =========================================================
# SOURCE DATABASE
# =========================================================

TRUSTED_DOMAINS = {
    "telegram.org",
    "t.me",
    "x.com",
    "twitter.com",
    "github.com",
    "discord.com",
    "discord.gg",
}


TEST_DOMAINS = {
    "example.com",
}


URL_SHORTENERS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "is.gd",
    "cutt.ly",
    "shorturl.at",
    "rb.gy",
}


SUSPICIOUS_TLDS = {
    ".click",
    ".top",
    ".buzz",
    ".monster",
    ".shop",
    ".live",
    ".icu",
    ".cam",
}


# =========================================================
# URL EXTRACTION
# =========================================================

def extract_links(text):
    pattern = r"https?://[^\s<>\"]+"
    return re.findall(pattern, text)


# =========================================================
# DOMAIN HELPERS
# =========================================================

def normalize_domain(domain):

    domain = domain.lower().strip()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain


def is_ip_address(domain):

    ipv4 = r"^\d{1,3}(\.\d{1,3}){3}$"

    return bool(
        re.match(ipv4, domain)
    )


def is_punycode(domain):

    return "xn--" in domain.lower()


def is_trusted_domain(domain):

    domain = normalize_domain(domain)

    for trusted in TRUSTED_DOMAINS:

        if (
            domain == trusted
            or domain.endswith("." + trusted)
        ):
            return True

    return False


def is_test_domain(domain):

    domain = normalize_domain(domain)

    for test_domain in TEST_DOMAINS:

        if (
            domain == test_domain
            or domain.endswith("." + test_domain)
        ):
            return True

    return False


def is_shortener(domain):

    domain = normalize_domain(domain)

    return domain in URL_SHORTENERS


def has_suspicious_tld(domain):

    domain = normalize_domain(domain)

    return any(
        domain.endswith(tld)
        for tld in SUSPICIOUS_TLDS
    )


# =========================================================
# SOURCE ANALYSIS
# =========================================================

def analyze_source(url, text=""):

    parsed = urlparse(url)

    domain = normalize_domain(
        parsed.netloc
    )

    result = {
        "url": url,
        "domain": domain,
        "source_type": "UNKNOWN",
        "status": "UNKNOWN",
        "risk": "LOW",
        "warnings": [],
    }

    if not domain:

        result["source_type"] = "INVALID"
        result["status"] = "INVALID"
        result["risk"] = "HIGH"

        result["warnings"].append(
            "Invalid URL"
        )

        return result

    # -----------------------------------------------------
    # TEST SOURCE
    # -----------------------------------------------------

    if is_test_domain(domain):

        result["source_type"] = "TEST_SOURCE"
        result["status"] = "TEST"
        result["risk"] = "LOW"

        return result

    # -----------------------------------------------------
    # TRUSTED SOURCE
    # -----------------------------------------------------

    if is_trusted_domain(domain):

        result["source_type"] = "TRUSTED_PLATFORM"
        result["status"] = "KNOWN"
        result["risk"] = "LOW"

        return result

    # -----------------------------------------------------
    # URL SHORTENER
    # -----------------------------------------------------

    if is_shortener(domain):

        result["source_type"] = "URL_SHORTENER"
        result["status"] = "SUSPICIOUS"
        result["risk"] = "HIGH"

        result["warnings"].append(
            "Shortened URL hides the final destination"
        )

        return result

    # -----------------------------------------------------
    # IP ADDRESS
    # -----------------------------------------------------

    if is_ip_address(domain):

        result["source_type"] = "IP_ADDRESS"
        result["status"] = "SUSPICIOUS"
        result["risk"] = "HIGH"

        result["warnings"].append(
            "Website uses an IP address instead of a normal domain"
        )

        return result

    # -----------------------------------------------------
    # PUNYCODE
    # -----------------------------------------------------

    if is_punycode(domain):

        result["source_type"] = "PUNYCODE_DOMAIN"
        result["status"] = "SUSPICIOUS"
        result["risk"] = "HIGH"

        result["warnings"].append(
            "Punycode domain detected"
        )

        return result

    # -----------------------------------------------------
    # SUSPICIOUS TLD
    # -----------------------------------------------------

    if has_suspicious_tld(domain):

        result["source_type"] = "UNKNOWN_DOMAIN"
        result["status"] = "UNKNOWN"
        result["risk"] = "MEDIUM"

        result["warnings"].append(
            "Domain uses a potentially suspicious TLD"
        )

    # -----------------------------------------------------
    # UNKNOWN DOMAIN
    # -----------------------------------------------------

    else:

        result["source_type"] = "UNKNOWN_DOMAIN"
        result["status"] = "UNKNOWN"
        result["risk"] = "LOW"

        result["warnings"].append(
            "Domain is not in the trusted source list"
        )

    # -----------------------------------------------------
    # Sensitive crypto context
    # -----------------------------------------------------

    text_lower = text.lower()

    sensitive_words = [
        "claim",
        "mint",
        "connect wallet",
        "wallet",
        "airdrop",
        "reward",
        "verify",
        "verification",
        "claim your",
        "mint now",
    ]

    sensitive_context = any(
        word in text_lower
        for word in sensitive_words
    )

    if (
        sensitive_context
        and result["status"] == "UNKNOWN"
    ):

        result["risk"] = "MEDIUM"

        result["warnings"].append(
            "Sensitive crypto action detected on an unverified domain"
        )

    return result


# =========================================================
# SOURCE AGGREGATION
# =========================================================

def analyze_sources(text, links):

    sources = []

    for link in links:

        sources.append(
            analyze_source(
                link,
                text
            )
        )

    if not sources:

        return {
            "sources": [],
            "overall_status": "NO_LINK",
            "overall_risk": "LOW",
            "warnings": [],
        }

    risk_levels = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
    }

    highest_risk = max(
        sources,
        key=lambda source:
        risk_levels.get(
            source["risk"],
            1
        )
    )["risk"]

    warnings = []

    for source in sources:

        warnings.extend(
            source["warnings"]
        )

    warnings = list(
        dict.fromkeys(warnings)
    )

    statuses = [
        source["status"]
        for source in sources
    ]

    if "SUSPICIOUS" in statuses:

        overall_status = "SUSPICIOUS"

    elif "UNKNOWN" in statuses:

        overall_status = "UNVERIFIED"

    elif "KNOWN" in statuses:

        overall_status = "KNOWN"

    elif "TEST" in statuses:

        overall_status = "TEST"

    else:

        overall_status = statuses[0]

    return {
        "sources": sources,
        "overall_status": overall_status,
        "overall_risk": highest_risk,
        "warnings": warnings,
    }


# =========================================================
# TOPIC DETECTION
# =========================================================

def detect_topics(text):

    text_lower = text.lower()

    topics = []

    for topic, keywords in TOPIC_KEYWORDS.items():

        if any(
            keyword.lower() in text_lower
            for keyword in keywords
        ):

            topics.append(topic)

    # Prevent Minted_Mind from being interpreted as MINT
    if (
        "minted_mind" in text_lower
        or "minted-mind" in text_lower
    ):

        if "MINT" in topics:

            topics.remove("MINT")

    return topics


# =========================================================
# ACTION DETECTION
# =========================================================

def detect_actions(text):

    text_lower = text.lower()

    actions = []

    for action, keywords in ACTION_KEYWORDS.items():

        if any(
            keyword.lower() in text_lower
            for keyword in keywords
        ):

            actions.append(action)

    # Prevent Minted_Mind from becoming MINT
    if (
        "minted_mind" in text_lower
        or "minted-mind" in text_lower
    ):

        if "MINT" in actions:

            actions.remove("MINT")

    return actions


# =========================================================
# DEADLINE DETECTION
# =========================================================

def detect_deadlines(text):

    patterns = [
        r"\btoday\b",
        r"\btonight\b",
        r"\btomorrow\b",
        r"\bdeadline\b",
        r"\b\d+\s*minutes?\b",
        r"\b\d+\s*hours?\b",

        r"امروز",
        r"امشب",
        r"فردا",
        r"مهلت",

        r"ساعت\s*\d{1,2}",
        r"\d+\s*دقیقه",
        r"\d+\s*ساعت",
        r"تا\s+\d+",
    ]

    results = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        for match in matches:

            if match not in results:

                results.append(match)

    return results


# =========================================================
# EVENT DETECTION
# =========================================================

def detect_event(
    text,
    topics,
    deadlines
):

    text_lower = text.lower()

    event_keywords = [
        "competition",
        "contest",
        "tournament",
        "challenge",
        "مسابقه",
        "رقابت",
        "event",
        "رویداد",
        "مسابقه داریم",
    ]

    has_event = any(
        keyword in text_lower
        for keyword in event_keywords
    )

    if not has_event:

        return False

    if deadlines:

        return True

    if "COMPETITION" in topics:

        return True

    return False


# =========================================================
# RISK DETECTION
# =========================================================

def calculate_risk(
    text,
    topics,
    actions,
    sources
):

    score = 0

    text_lower = text.lower()

    # -----------------------------------------------------
    # Crypto actions
    # -----------------------------------------------------

    if "MINT" in topics:

        score += 20

    if "CLAIM" in topics:

        score += 20

    if "CONNECT_WALLET" in actions:

        score += 25

    if "MINT" in actions:

        score += 20

    if "CLAIM" in actions:

        score += 15

    # -----------------------------------------------------
    # Source risk
    # -----------------------------------------------------

    for source in sources:

        if source["risk"] == "MEDIUM":

            score += 10

        elif source["risk"] == "HIGH":

            score += 40

    # -----------------------------------------------------
    # Explicit scam indicators
    # -----------------------------------------------------

    scam_words = [
        "seed phrase",
        "private key",
        "recovery phrase",
        "send crypto",
        "send us",
        "deposit to claim",
    ]

    if any(
        word in text_lower
        for word in scam_words
    ):

        score += 50

    # -----------------------------------------------------
    # Competition is normally low risk
    # -----------------------------------------------------

    if (
        "COMPETITION" in topics
        and not any(
            action in actions
            for action in [
                "CONNECT_WALLET",
                "MINT",
                "CLAIM",
            ]
        )
    ):

        score = min(
            score,
            20
        )

    if score >= 70:

        return "HIGH"

    if score >= 35:

        return "MEDIUM"

    return "LOW"


# =========================================================
# PRIORITY
# =========================================================

def calculate_priority(
    risk,
    actions,
    deadlines,
    source_risk
):

    if risk == "HIGH":

        return "🔴 HIGH"

    if (
        source_risk == "HIGH"
        and any(
            action in actions
            for action in [
                "CONNECT_WALLET",
                "MINT",
                "CLAIM",
            ]
        )
    ):

        return "🔴 HIGH"

    if (
        "CLAIM" in actions
        or deadlines
    ):

        return "🔴 HIGH"

    if (
        actions
        or risk == "MEDIUM"
    ):

        return "🟠 MEDIUM"

    return "🟢 LOW"


# =========================================================
# CONFIDENCE
# =========================================================

def calculate_confidence(
    text,
    topics,
    actions,
    deadlines,
    event_detected,
    links,
    sources
):

    score = 50

    if topics:

        score += 10

    if actions:

        score += 15

    if len(actions) >= 2:

        score += 5

    if deadlines:

        score += 10

    if event_detected:

        score += 5

    if links:

        score += 5

    if sources:

        known_sources = [
            source
            for source in sources
            if source["status"] == "KNOWN"
        ]

        suspicious_sources = [
            source
            for source in sources
            if source["risk"] == "HIGH"
        ]

        if known_sources:

            score += 5

        if suspicious_sources:

            score -= 10

    return max(
        0,
        min(score, 100)
    )


# =========================================================
# MAIN ANALYZER
# =========================================================

def analyze_message(text, link):

    topics = detect_topics(text)

    actions = detect_actions(text)

    deadlines = detect_deadlines(text)

    event_detected = detect_event(
        text,
        topics,
        deadlines
    )

    links = extract_links(text)

    if (
        link
        and link not in links
    ):

        links.append(link)

    source_analysis = analyze_sources(
        text,
        links
    )

    sources = source_analysis[
        "sources"
    ]

    # -----------------------------------------------------
    # Competition automatically means JOIN
    # -----------------------------------------------------

    if (
        event_detected
        and "JOIN" not in actions
        and "COMPETITION" in topics
    ):

        actions.append("JOIN")

    # -----------------------------------------------------
    # Risk
    # -----------------------------------------------------

    risk = calculate_risk(
        text,
        topics,
        actions,
        sources
    )

    source_risk = source_analysis[
        "overall_risk"
    ]

    priority = calculate_priority(
        risk,
        actions,
        deadlines,
        source_risk
    )

    # -----------------------------------------------------
    # Financial action
    # -----------------------------------------------------

    financial_action = any(
        action in actions
        for action in [
            "CONNECT_WALLET",
            "MINT",
            "CLAIM",
        ]
    )

    # -----------------------------------------------------
    # Action required
    # -----------------------------------------------------

    action_required = bool(actions)

    # -----------------------------------------------------
    # Primary action
    # -----------------------------------------------------

    if actions:

        action_order = [
            "CONNECT_WALLET",
            "MINT",
            "CLAIM",
            "REGISTER",
            "JOIN",
        ]

        action = next(
            (
                item
                for item in action_order
                if item in actions
            ),
            actions[0]
        )

    else:

        action = None

    # -----------------------------------------------------
    # Confidence
    # -----------------------------------------------------

    confidence = calculate_confidence(
        text,
        topics,
        actions,
        deadlines,
        event_detected,
        links,
        sources
    )

    # -----------------------------------------------------
    # Explanation
    # -----------------------------------------------------

    reasons = []

    if topics:

        reasons.append(
            "موضوع مرتبط با Web3 شناسایی شد"
        )

    if actions:

        reasons.append(
            "اقدام قابل انجام شناسایی شد"
        )

    if event_detected:

        reasons.append(
            "رویداد یا مسابقه شناسایی شد"
        )

    if deadlines:

        reasons.append(
            "محدودیت زمانی شناسایی شد"
        )

    if source_analysis[
        "overall_status"
    ] == "UNVERIFIED":

        reasons.append(
            "لینک ناشناخته یا تأییدنشده است"
        )

    if source_analysis[
        "overall_status"
    ] == "SUSPICIOUS":

        reasons.append(
            "هشدار امنیتی برای منبع شناسایی شد"
        )

    if not reasons:

        reasons.append(
            "مورد مهمی برای اقدام شناسایی نشد"
        )

    reason = "؛ ".join(
        reasons
    )

    # -----------------------------------------------------
    # Final result
    # -----------------------------------------------------

    return {
        "priority": priority,

        "risk": risk,

        "confidence": confidence,

        "topics": topics,

        "actions": actions,

        "action": action,

        "action_required": action_required,

        "financial_action": financial_action,

        "deadlines": deadlines,

        "event": event_detected,

        "links": links,

        "sources": sources,

        "source_status": source_analysis[
            "overall_status"
        ],

        "source_risk": source_analysis[
            "overall_risk"
        ],

        "source_warnings": source_analysis[
            "warnings"
        ],

        "reason": reason,

        "text": text,

        "link": link,
    }


# =========================================================
# TELEGRAM FORMATTER
# =========================================================

def format_alert(result):

    lines = []

    lines.append(
        "🤖 NABU INTELLIGENCE ALERT"
    )

    lines.append("")

    lines.append(
        f"اهمیت: {result['priority']}"
    )

    lines.append(
        f"⚠️ ریسک: {result['risk']}"
    )

    lines.append(
        f"🎯 اطمینان تحلیل: "
        f"{result['confidence']}%"
    )

    lines.append("")

    lines.append(
        f"⚡ اقدام لازم: "
        f"{'بله' if result['action_required'] else 'خیر'}"
    )

    if result["action"]:

        lines.append(
            f"🎯 اقدام اصلی: "
            f"{result['action']}"
        )

    if result["actions"]:

        lines.append(
            "📋 همه اقدامات: "
            + ", ".join(
                result["actions"]
            )
        )

    if result["event"]:

        lines.append(
            "🎪 رویداد: شناسایی شد"
        )

    if result["deadlines"]:

        lines.append(
            "⏰ زمان‌ها: "
            + ", ".join(
                result["deadlines"]
            )
        )

    lines.append("")

    lines.append(
        "🔎 SOURCE ANALYSIS"
    )

    lines.append(
        f"وضعیت منبع: "
        f"{result['source_status']}"
    )

    lines.append(
        f"ریسک منبع: "
        f"{result['source_risk']}"
    )

    for source in result["sources"]:

        lines.append(
            f"🌐 {source['domain']} "
            f"→ {source['status']} / "
            f"{source['risk']}"
        )

    if result["source_warnings"]:

        lines.append("")

        lines.append(
            "🚨 هشدارهای امنیتی:"
        )

        for warning in result[
            "source_warnings"
        ]:

            lines.append(
                f"• {warning}"
            )

    lines.append("")

    lines.append(
        "📝 دلیل تحلیل:"
    )

    lines.append(
        result["reason"]
    )

    lines.append("")

    lines.append(
        f"💰 اقدام مالی/کیف پول: "
        f"{'بله' if result['financial_action'] else 'خیر'}"
    )

    lines.append("")

    lines.append(
        "🔗 لینک پست:"
    )

    lines.append(
        result["link"]
    )

    return "\n".join(lines)



2. حالا همان تست قبلی را اجرا کن


برو:


GitHub → Actions → Test Analyzer → Run workflow


این بار برای NORMAL ANNOUNCEMENT باید دیگر این حالت را نبینی:


🔴 HIGH



و برای مسابقه هم نباید صرفاً به خاطر example.com هشدار جدی بگیری.


اما برای چیزی مثل:


Connect your wallet and claim your reward
https://bit.ly/xxxxx



Agent باید لینک کوتاه‌شده را SUSPICIOUS / HIGH تشخیص بدهد.


مرحله بعدی


بعد از اینکه این تست سبز شد، می‌رویم سراغ مرحله مهم‌تر V3:


Live URL Verification


یعنی Agent دیگر فقط به اسم دامنه نگاه نمی‌کند؛ لینک را واقعاً بررسی می‌کند و نتیجه را در Alert می‌آورد:


URL → Domain → HTTPS → Redirect → Final Domain → Risk → Scam Warning


و این قسمت برای Agent نهایی خیلی مهم‌تر از allowlist ساده خواهد بود.

