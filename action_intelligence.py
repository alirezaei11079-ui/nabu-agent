def build_action_intelligence(result):
    actions = result.get("actions", [])
    risk = result.get("risk", "LOW")
    priority = result.get("priority", "🟢 LOW")
    deadlines = result.get("deadlines", [])
    event = result.get("event", False)

    sources = result.get("sources", [])
    source_risk = result.get("source_risk", "LOW")
    source_status = result.get("source_status", "NONE")

    financial_action = result.get(
        "financial_action",
        False
    )

    recommendations = []
    warnings = []

    wallet_required = any(
        action in actions
        for action in [
            "CONNECT_WALLET",
            "MINT",
            "CLAIM"
        ]
    )

    transfer_requested = any(
        keyword in result.get("text", "").lower()
        for keyword in [
            "send crypto",
            "send us",
            "deposit to claim",
            "send eth",
            "send usdt",
            "send btc",
            "ارسال ارز",
            "واریز کنید"
        ]
    )

    secret_requested = any(
        keyword in result.get("text", "").lower()
        for keyword in [
            "seed phrase",
            "recovery phrase",
            "private key",
            "secret phrase",
            "عبارت بازیابی",
            "کلید خصوصی"
        ]
    )

    phishing_detected = False
    phishing_score = 0
    brand_impersonation = False
    impersonated_brands = []

    for source in sources:

        phishing = source.get(
            "phishing",
            {}
        )

        if phishing:

            phishing_score = max(
                phishing_score,
                phishing.get(
                    "score",
                    0
                )
            )

            if phishing.get(
                "risk"
            ) == "HIGH":

                phishing_detected = True

            if phishing.get(
                "brand_impersonation"
            ):

                brand_impersonation = True

                for brand in phishing.get(
                    "brands",
                    []
                ):

                    if brand not in impersonated_brands:

                        impersonated_brands.append(
                            brand
                        )

    if secret_requested:

        warnings.append(
            "هرگز Seed Phrase، Recovery Phrase یا Private Key را وارد نکن."
        )

    if transfer_requested:

        warnings.append(
            "انتقال ارز درخواست شده؛ قبل از هر انتقال متوقف شو و منبع را مستقل بررسی کن."
        )

    if phishing_detected:

        warnings.append(
            "نشانه‌های جدی فیشینگ شناسایی شده است."
        )

    if brand_impersonation:

        brands = ", ".join(
            impersonated_brands
        )

        warnings.append(
            f"احتمال جعل هویت برند شناسایی شد: {brands}"
        )

    if source_status in [
        "SUSPICIOUS",
        "UNVERIFIED"
    ]:

        warnings.append(
            "منبع تأییدشده نیست؛ قبل از هر اقدام، دامنه مقصد را مستقل بررسی کن."
        )

    if source_risk == "HIGH":

        warnings.append(
            "ریسک منبع HIGH است؛ اقدام مالی یا اتصال کیف پول توصیه نمی‌شود."
        )

    if wallet_required:

        recommendations.append(
            "اگر قرار است کیف پول متصل شود، ابتدا دامنه و قرارداد/پروژه را مستقل بررسی کن."
        )

        recommendations.append(
            "برای آزمایش از کیف پول اصلی و دارایی اصلی استفاده نکن."
        )

    if "CLAIM" in actions:

        recommendations.append(
            "ابتدا شرایط Claim، آدرس قرارداد و منبع رسمی پروژه را بررسی کن."
        )

    if "MINT" in actions:

        recommendations.append(
            "قبل از Mint، قرارداد، شبکه، هزینه Gas و دامنه رسمی را بررسی کن."
        )

    if "JOIN" in actions or event:

        recommendations.append(
            "اگر رویداد صرفاً اجتماعی/رقابتی است، فقط مراحل اعلام‌شده توسط منبع معتبر را انجام بده."
        )

    if "REGISTER" in actions:

        recommendations.append(
            "برای ثبت‌نام، فقط از لینک رسمی و معتبر استفاده کن."
        )

    if not actions:

        recommendations.append(
            "اقدام فوری شناسایی نشد؛ فقط اطلاع‌رسانی را دنبال کن."
        )

    if deadlines:

        deadline_text = ", ".join(
            deadlines
        )

        recommendations.insert(
            0,
            f"⏰ زمان/مهلت شناسایی‌شده: {deadline_text}"
        )

    if transfer_requested:

        safety_status = "STOP"

    elif secret_requested:

        safety_status = "STOP"

    elif phishing_detected:

        safety_status = "STOP"

    elif source_risk == "HIGH":

        safety_status = "CAUTION"

    elif source_status == "UNVERIFIED":

        safety_status = "CAUTION"

    elif financial_action:

        safety_status = "CAUTION"

    else:

        safety_status = "NORMAL"

    if safety_status == "STOP":

        decision = (
            "فعلاً هیچ اقدام مالی، اتصال کیف پول یا ورود اطلاعات حساس انجام نده."
        )

    elif safety_status == "CAUTION":

        decision = (
            "قبل از هر اقدام، منبع و مقصد را مستقل بررسی کن."
        )

    elif event and not financial_action:

        decision = (
            "اقدام مالی شناسایی نشد؛ می‌توانی مراحل غیرمالی رویداد را بررسی کنی."
        )

    elif actions:

        decision = (
            "اقدام شناسایی شده است؛ قبل از اجرا بررسی‌های امنیتی بالا را انجام بده."
        )

    else:

        decision = (
            "اقدام خاصی لازم نیست."
        )

    return {
        "safety_status": safety_status,
        "decision": decision,
        "wallet_required": wallet_required,
        "transfer_requested": transfer_requested,
        "secret_requested": secret_requested,
        "phishing_detected": phishing_detected,
        "phishing_score": phishing_score,
        "brand_impersonation": brand_impersonation,
        "impersonated_brands": impersonated_brands,
        "warnings": warnings,
        "recommendations": recommendations,
        "deadline": deadlines,
        "actions": actions,
        "risk": risk,
        "priority": priority,
    }


def format_action_intelligence(
    intelligence
):

    safety_status = intelligence[
        "safety_status"
    ]

    if safety_status == "STOP":

        header = "🚨 SECURITY ALERT"

    elif safety_status == "CAUTION":

        header = "⚠️ ACTION INTELLIGENCE"

    else:

        header = "🧠 ACTION INTELLIGENCE"

    wallet = (
        "بله"
        if intelligence[
            "wallet_required"
        ]
        else "خیر"
    )

    transfer = (
        "بله"
        if intelligence[
            "transfer_requested"
        ]
        else "خیر"
    )

    secret = (
        "بله"
        if intelligence[
            "secret_requested"
        ]
        else "خیر"
    )

    phishing = (
        "بله"
        if intelligence[
            "phishing_detected"
        ]
        else "خیر"
    )

    lines = [

        header,
        "",
        f"🛡️ وضعیت امنیتی: {safety_status}",
        f"⚠️ ریسک: {intelligence['risk']}",
        f"📌 اولویت: {intelligence['priority']}",
        "",
        "🔍 ACTION CHECK",
        f"👛 نیاز به کیف پول: {wallet}",
        f"💸 درخواست انتقال ارز: {transfer}",
        f"🔑 اطلاعات حساس درخواست شده: {secret}",
        f"🎣 نشانه فیشینگ: {phishing}",
        f"🧠 امتیاز فیشینگ: {intelligence['phishing_score']}",
    ]

    if intelligence[
        "brand_impersonation"
    ]:

        brands = ", ".join(
            intelligence[
                "impersonated_brands"
            ]
        )

        lines.append(
            f"🎭 جعل احتمالی برند: {brands}"
        )

    deadlines = intelligence[
        "deadline"
    ]

    if deadlines:

        lines.extend([
            "",
            "⏰ DEADLINE",
        ])

        for deadline in deadlines:

            lines.append(
                f"• {deadline}"
            )

    warnings = intelligence[
        "warnings"
    ]

    if warnings:

        lines.extend([
            "",
            "🚨 هشدارها",
        ])

        for warning in warnings:

            lines.append(
                f"• {warning}"
            )

    recommendations = intelligence[
        "recommendations"
    ]

    if recommendations:

        lines.extend([
            "",
            "📋 مراحل پیشنهادی",
        ])

        for index, recommendation in enumerate(
            recommendations,
            start=1
        ):

            lines.append(
                f"{index}. {recommendation}"
            )

    lines.extend([
        "",
        "🧠 نتیجه",
        intelligence["decision"],
    ])

    return "\n".join(
        lines
  )
