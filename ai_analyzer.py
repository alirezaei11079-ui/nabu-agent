import os
import json
import requests


API_URL = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/models/gemini-2.5-flash-lite:generateContent"
)

MODEL_NAME = "gemini-2.5-flash-lite"


def analyze_with_ai(text, source_url=""):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    prompt = f"""
You are the intelligence analyst of a Web3 monitoring agent.

Analyze the following social media post carefully.

Your job is NOT to guess.
Only report information that is directly supported by the post.

If information is missing, use an empty string, false, empty array,
or "unknown".

Never invent:
- prices
- deadlines
- contract addresses
- blockchain networks
- project names
- eligibility
- rewards
- wallet requirements

Determine what the post actually means and what a user would need
to do if they wanted to participate.

POST:
{text}

SOURCE:
{source_url}

Return ONLY valid JSON with exactly this structure:

{{
  "summary": "",
  "meaning": "",
  "category": "",
  "project": "",
  "event": "",
  "action_required": false,
  "actions": [],
  "urgency": "LOW",
  "deadline": "",
  "cost": "",
  "network": "",
  "contract_address": "",
  "wallet_required": false,
  "financial_action": false,
  "eligibility": "",
  "reward": "",
  "links": [],
  "requirements": [],
  "unknowns": [],
  "risk_notes": [],
  "user_steps": []
}}

Rules:

category must be one of:
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

urgency must be one of:
LOW
MEDIUM
HIGH
CRITICAL

summary:
Give a short Persian summary of the post.

meaning:
Explain in Persian what the author is actually saying.

actions:
List only actions explicitly required or clearly implied by the post.

requirements:
List requirements mentioned in the post.

unknowns:
List important information that is missing but would matter before taking action.

risk_notes:
List potential risks or things that require verification.
Do not claim something is a scam unless the text itself provides strong evidence.

user_steps:
Give practical Persian steps based ONLY on the information available.

The output must be valid JSON.
"""


    response = requests.post(
        f"{API_URL}?key={api_key}",
        headers={
            "Content-Type": "application/json"
        },
        json={
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "responseMimeType": "application/json"
            }
        },
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    try:

        text_response = (
            data["candidates"][0]
            ["content"]["parts"][0]["text"]
        )

    except (KeyError, IndexError):

        raise RuntimeError(
            f"Unexpected Gemini response: {data}"
        )

    try:

        return json.loads(
            text_response
        )

    except json.JSONDecodeError:

        raise RuntimeError(
            "Gemini returned invalid JSON."
        )


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

        lines.extend([
            "",
            f"⏰ مهلت: {result['deadline']}"
        ])

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

    lines.append(
        f"👛 نیاز به کیف پول: "
        f"{'بله' if result.get('wallet_required') else 'خیر/نامشخص'}"
    )

    if result.get("reward"):

        lines.append(
            f"🎁 پاداش: {result['reward']}"
        )

    if result.get("eligibility"):

        lines.append(
            f"👤 واجد شرایط بودن: "
            f"{result['eligibility']}"
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


