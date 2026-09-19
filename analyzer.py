import re
import requests
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
# URL HELPERS
# =========================================================

def extract_links(text):
    if not text:
        return []

    pattern = r"https?://[^\s<>\"]+"

    links = re.findall(pattern, text)

    cleaned = []

    for link in links:
        link = link.rstrip(".,!?;:)]}")

        if link not in cleaned:
            cleaned.append(link)

    return cleaned


def normalize_domain(domain):
    domain = domain.lower().strip()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain


def is_ip_address(domain):
    ipv4_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"

    return bool(
        re.match(
            ipv4_pattern,
            domain
        )
    )


def is_punycode(domain):
    return "xn--" in domain.lower()


def is_trusted_domain(domain):
    domain = normalize_domain(domain)

    if domain in TRUSTED_DOMAINS:
        return True

    for trusted in TRUSTED_DOMAINS:

        if domain.endswith("." + trusted):
            return True

    return False


def is_test_domain(domain):
    domain = normalize_domain(domain)

    return domain in TEST_DOMAINS


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

    result = {
        "url": url,
        "domain": "",
        "status": "UNKNOWN",
        "risk": "LOW",
        "warnings": [],
    }

    try:
        parsed = urlparse(url)

        if not parsed.netloc:

            result["status"] = "INVALID"
            result["risk"] = "HIGH"

            result["warnings"].append(
                "Invalid URL"
            )

            return result

        domain = normalize_domain(
            parsed.netloc
        )

        result["domain"] = domain

        if is_test_domain(domain):

            result["status"] = "TEST"
            result["risk"] = "LOW"

            return result

        if is_ip_address(domain):

            result["status"] = "SUSPICIOUS"
            result["risk"] = "HIGH"

            result["warnings"].append(
                "URL uses an IP address"
            )

            return result

        if is_punycode(domain):

            result["status"] = "SUSPICIOUS"
            result["risk"] = "HIGH"

            result["warnings"].append(
                "Punycode domain detected"
            )

            return result

        if is_shortener(domain):

            result["status"] = "SUSPICIOUS"
            result["risk"] = "HIGH"

            result["warnings"].append(
                "URL shortener detected"
            )

            return result

        if has_suspicious_tld(domain):

            result["status"] = "UNKNOWN"
            result["risk"] = "MEDIUM"

            result["warnings"].append(
                "Suspicious top-level domain"
            )

            return result

        if is_trusted_domain(domain):

            result["status"] = "KNOWN"
            result["risk"] = "LOW"

            return result

        result["status"] = "UNKNOWN"
        result["risk"] = "LOW"

        sensitive_words = [
            "claim",
            "mint",
            "connect wallet",
            "wallet",
            "airdrop",
            "reward",
            "verify",
            "crypto",
            "token",
        ]

        lower_text = text.lower()

        if any(
            word in lower_text
            for word in sensitive_words
        ):

            result["risk"] = "MEDIUM"

            result["warnings"].append(
                "Unknown domain used in sensitive crypto context"
            )

    except Exception as error:

        result["status"] = "INVALID"
        result["risk"] = "HIGH"

        result["warnings"].append(
            str(error)
        )

    return result


# =========================================================
# LIVE URL VERIFICATION
# =========================================================

def verify_url_live(url):

    result = {
        "url": url,
        "reachable": False,
        "final_url": url,
        "final_domain": "",
        "https": False,
        "redirected": False,
        "status_code": None,
        "error": None,
    }

    try:

        parsed = urlparse(url)

        if parsed.scheme != "https":
            result["https"] = False
        else:
            result["https"] = True

        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 Nabu-Agent"
            },
            timeout=10,
            allow_redirects=True,
            stream=True,
        )

        result["reachable"] = True

        result["status_code"] = response.status_code

        result["final_url"] = response.url

        final_parsed = urlparse(
            response.url
        )

        result["final_domain"] = normalize_domain(
            final_parsed.netloc
        )

        result["redirected"] = (
            response.url.rstrip("/")
            != url.rstrip("/")
        )

        response.close()

    except requests.exceptions.Timeout:

        result["error"] = "Timeout"

    except requests.exceptions.RequestException as error:

        result["error"] = str(error)

    except Exception as error:

        result["error"] = str(error)

    return result


def live_source_security_check(source):

    url = source["url"]

    live = verify_url_live(url)

    source["live"] = live

    if not live["reachable"]:

        source["warnings"].append(
            "Live URL verification failed"
        )

        if source["risk"] == "LOW":
            source["risk"] = "MEDIUM"

        return source

    if not live["https"]:

        source["warnings"].append(
            "URL does not use HTTPS"
        )

        source["risk"] = "HIGH"

    if live["redirected"]:

        source["warnings"].append(
            "URL redirects to another destination"
        )

        source["redirected_to"] = (
            live["final_url"]
        )

        final_domain = live["final_domain"]

        original_domain = source["domain"]

        if (
            final_domain
            and final_domain != original_domain
        ):

            source["warnings"].append(
                "Final destination uses a different domain"
            )

            source["risk"] = "HIGH"

    status_code = live["status_code"]

    if status_code:

        if status_code >= 400:

            source["warnings"].append(
                f"HTTP error status: {status_code}"
            )

            if source["risk"] == "LOW":
                source["risk"] = "MEDIUM"

    return source


def analyze_sources(text, links):

    sources = []

    for link in links:

        source = analyze_source(
            link,
            text
        )

        # Live verification only for real URLs
        if source["status"] != "TEST":

            source = live_source_security_check(
                source
            )

        sources.append(source)

    if not sources:

        return {
            "sources": [],
            "status": "NONE",
            "risk": "LOW",
            "warnings": [],
        }

    risks = [
        source["risk"]
        for source in sources
    ]

    warnings = []

    for source in sources:

        for warning in source["warnings"]:

            if warning not in warnings:
                warnings.append(warning)

    if "HIGH" in risks:

        overall_risk = "HIGH"

    elif "MEDIUM" in risks:

        overall_risk = "MEDIUM"

    else:

        overall_risk = "LOW"

    statuses = [
        source["status"]
        for source in sources
    ]

    if "SUSPICIOUS" in statuses:

        overall_status = "SUSPICIOUS"

    elif "INVALID" in statuses:

        overall_status = "SUSPICIOUS"

    elif "UNKNOWN" in statuses:

        overall_status = "UNVERIFIED"

    elif "KNOWN" in statuses:

        overall_status = "KNOWN"

    elif "TEST" in statuses:

        overall_status = "TEST"

    else:

        overall_status = "UNKNOWN"

    return {
        "sources": sources,
        "status": overall_status,
        "risk": overall_risk,
        "warnings": warnings,
    }


# =========================================================
# TOPIC DETECTION
# =========================================================

def detect_topics(text):

    lower_text = text.lower()

    topics = []

    for topic, keywords in TOPIC_KEYWORDS.items():

        for keyword in keywords:

            if keyword in lower_text:

                if topic not in topics:
                    topics.append(topic)

                break

    # Prevent false MINT detection
    if (
        "minted_mind" in lower_text
        or "minted-mind" in lower_text
    ):

        if "MINT" in topics:
            topics.remove("MINT")

    return topics


# =========================================================
# ACTION DETECTION
# =========================================================

def detect_actions(text):

    lower_text = text.lower()

    actions = []

    for action, keywords in ACTION_KEYWORDS.items():

        for keyword in keywords:

            if keyword in lower_text:

                if action not in actions:
                    actions.append(action)

                break

    # Prevent false MINT detection
    if (
        "minted_mind" in lower_text
        or "minted-mind" in lower_text
    ):

        if "MINT" in actions:
            actions.remove("MINT")

    return actions


# =========================================================
# DEADLINE DETECTION
# =========================================================

def detect_deadlines(text):

    deadlines = []

    patterns = [

        r"\btoday\b",
        r"\btonight\b",
        r"\btomorrow\b",

        r"\bdeadline\b",

        r"\b\d+\s*(?:minutes?|mins?)\b",
        r"\b\d+\s*(?:hours?|hrs?)\b",

        r"امروز",
        r"امشب",
        r"فردا",
        r"مهلت",

        r"ساعت\s*\d+",

        r"\d+\s*دقیقه",
        r"\d+\s*ساعت",
    ]

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        for match in matches:

            value = match.strip()

            if value not in deadlines:
                deadlines.append(value)

    return deadlines


# =========================================================
# EVENT DETECTION
# =========================================================

def detect_event(
    text,
    topics,
    deadlines
):

    lower_text = text.lower()

    event_words = [
        "competition",
        "contest",
        "tournament",
        "challenge",
        "event",
        "مسابقه",
        "رقابت",
        "رویداد",
    ]

    event_found = any(
        word in lower_text
        for word in event_words
    )

    if "COMPETITION" in topics:
        event_found = True

    if event_found and deadlines:
        return True

    if "COMPETITION" in topics:
        return True

    return False


# =========================================================
# RISK CALCULATION
# =========================================================

def calculate_risk(
    text,
    topics,
    actions,
    sources
):

    score = 0

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

    source_risk = sources.get(
        "risk",
        "LOW"
    )

    if source_risk == "MEDIUM":
        score += 10

    elif source_risk == "HIGH":
        score += 40

    scam_words = [
        "seed phrase",
        "private key",
        "recovery phrase",
        "send crypto",
        "send us",
        "deposit to claim",
    ]

    lower_text = text.lower()

    for word in scam_words:

        if word in lower_text:
            score += 50

    event = (
        "COMPETITION" in topics
        or "JOIN" in actions
    )

    sensitive_actions = {
        "CONNECT_WALLET",
        "MINT",
        "CLAIM",
    }

    if event and not any(
        action in sensitive_actions
        for action in actions
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

    # Security or sensitive financial action
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

    # Claim is usually time-sensitive
    if "CLAIM" in actions:
        return "🔴 HIGH"

    # Normal competition should not become HIGH
    if (
        "JOIN" in actions
        and "CLAIM" not in actions
        and "MINT" not in actions
        and "CONNECT_WALLET" not in actions
    ):
        return "🟠 MEDIUM"

    if risk == "MEDIUM":
        return "🟠 MEDIUM"

    if actions:
        return "🟠 MEDIUM"

    return "🟢 LOW"


# =========================================================
# CONFIDENCE
# =========================================================

def calculate_confidence(
    topics,
    actions,
    deadlines,
    event,
    links,
    sources
):

    confidence = 50

    if topics:
        confidence += 10

    if actions:
        confidence += 15

    if len(actions) >= 2:
        confidence += 5

    if deadlines:
        confidence += 10

    if event:
        confidence += 5

    if links:
        confidence += 5

    source_list = sources.get(
        "sources",
        []
    )

    if any(
        source["status"] == "KNOWN"
        for source in source_list
    ):
        confidence += 5

    if any(
        source["status"] == "SUSPICIOUS"
        or source["risk"] == "HIGH"
        for source in source_list
    ):
        confidence -= 10

    confidence = max(
        0,
        min(
            confidence,
            100
        )
    )

    return confidence


# =========================================================
# MAIN ANALYSIS
# =========================================================

def analyze_message(
    text,
    link
):

    if not text:
        text = ""

    topics = detect_topics(
        text
    )

    actions = detect_actions(
        text
    )

    deadlines = detect_deadlines(
        text
    )

    event = detect_event(
        text,
        topics,
        deadlines
    )

    links = extract_links(
        text
    )

    if link and link not in links:
        links.append(link)

    source_analysis = analyze_sources(
        text,
        links
    )

    # Competition automatically means JOIN
    if (
        event
        and "JOIN" not in actions
    ):

        actions.append("JOIN")

    risk = calculate_risk(
        text,
        topics,
        actions,
        source_analysis
    )

    priority = calculate_priority(
        risk,
        actions,
        deadlines,
        source_analysis["risk"]
    )

    financial_actions = {
        "CONNECT_WALLET",
        "MINT",
        "CLAIM",
    }

    financial_action = any(
        action in financial_actions
        for action in actions
    )

    action_required = bool(
        actions
    )

    primary_action = (
        actions[0]
        if actions
        else "NONE"
    )

    confidence = calculate_confidence(
        topics,
        actions,
        deadlines,
        event,
        links,
        source_analysis
    )

    reasons = []

    if topics:
        reasons.append(
            "Detected topics: "
            + ", ".join(topics)
        )

    if actions:
        reasons.append(
            "Detected actions: "
            + ", ".join(actions)
        )

    if deadlines:
        reasons.append(
            "Detected deadline/time: "
            + ", ".join(deadlines)
        )

    if event:
        reasons.append(
            "Event or competition detected"
        )

    if source_analysis["status"] != "NONE":

        reasons.append(
            "Source status: "
            + source_analysis["status"]
        )

    if source_analysis["risk"] != "LOW":

        reasons.append(
            "Source risk: "
            + source_analysis["risk"]
        )

    reason = (
        " | ".join(reasons)
        if reasons
        else "No significant action or event detected"
    )

    return {
        "priority": priority,
        "risk": risk,
        "confidence": confidence,
        "topics": topics,
        "actions": actions,
        "action": primary_action,
        "action_required": action_required,
        "financial_action": financial_action,
        "deadlines": deadlines,
        "event": event,
        "links": links,
        "sources": source_analysis["sources"],
        "source_status": source_analysis["status"],
        "source_risk": source_analysis["risk"],
        "source_warnings": source_analysis["warnings"],
        "reason": reason,
        "text": text,
        "link": link,
    }


# =========================================================
# TELEGRAM ALERT FORMAT
# =========================================================

def format_alert(result):

    priority = result["priority"]

    risk = result["risk"]

    confidence = result["confidence"]

    action_required = (
        "بله"
        if result["action_required"]
        else "خیر"
    )

    financial_action = (
        "بله"
        if result["financial_action"]
        else "خیر"
    )

    event = (
        "بله"
        if result["event"]
        else "خیر"
    )

    action = result["action"]

    actions = (
        ", ".join(result["actions"])
        if result["actions"]
        else "NONE"
    )

    deadlines = (
        ", ".join(result["deadlines"])
        if result["deadlines"]
        else "NONE"
    )

    lines = [

        "🤖 NABU INTELLIGENCE ALERT",
        "",
        f"اهمیت: {priority}",
        f"⚠️ ریسک: {risk}",
        f"🎯 اطمینان تحلیل: {confidence}%",
        "",
        f"⚡ اقدام لازم: {action_required}",
        f"🎯 اقدام اصلی: {action}",
        f"📋 همه اقدامات: {actions}",
        "",
        f"🎪 رویداد: {event}",
        f"⏰ زمان‌ها: {deadlines}",
        "",
        "🔎 SOURCE ANALYSIS",
        f"وضعیت منبع: {result['source_status']}",
        f"ریسک منبع: {result['source_risk']}",
    ]

    # Source details
    for source in result["sources"]:

        domain = source.get(
            "domain",
            "UNKNOWN"
        )

        status = source.get(
            "status",
            "UNKNOWN"
        )

        source_risk = source.get(
            "risk",
            "LOW"
        )

        lines.append(
            f"🌐 {domain} → {status} / {source_risk}"
        )

        live = source.get(
            "live"
        )

        if live:

            reachable = (
                "YES"
                if live.get("reachable")
                else "NO"
            )

            https = (
                "YES"
                if live.get("https")
                else "NO"
            )

            redirected = (
                "YES"
                if live.get("redirected")
                else "NO"
            )

            status_code = live.get(
                "status_code"
            )

            lines.append(
                f"   Live: {reachable} | HTTPS: {https}"
            )

            lines.append(
                f"   Redirect: {redirected} | HTTP: {status_code}"
            )

            final_domain = live.get(
                "final_domain"
            )

            if final_domain:

                lines.append(
                    f"   Final domain: {final_domain}"
                )

            error = live.get(
                "error"
            )

            if error:

                lines.append(
                    f"   Error: {error}"
                )

    warnings = result[
        "source_warnings"
    ]

    if warnings:

        lines.extend([
            "",
            "🚨 هشدارهای امنیتی:",
        ])

        for warning in warnings:

            lines.append(
                f"• {warning}"
            )

    lines.extend([
        "",
        "📝 دلیل تحلیل:",
        result["reason"],
        "",
        f"💰 اقدام مالی/کیف پول: {financial_action}",
        "",
        "🔗 لینک پست:",
        result["link"],
    ])

    return "\n".join(
        lines)

