"""
Day 6 – Fraud Alert Voice Agent (MongoDB version, Slice Bank)

Agent Name: Akash
Bank Name: Slice Bank

Flow:
  1. Introduce as Akash from Slice Bank Fraud Prevention Team
  2. Ask for FULL NAME
  3. Ask for SECURITY IDENTIFIER
  4. If verified, read suspicious transaction from MongoDB
  5. Ask if transaction is legitimate (yes/no)
  6. Update MongoDB status: confirmed_safe / confirmed_fraud / verification_failed
"""

import logging
import os
from dataclasses import dataclass
from typing import Optional, Annotated

from dotenv import load_dotenv
from pydantic import Field
from pymongo import MongoClient

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    RoomInputOptions,
    WorkerOptions,
    cli,
    function_tool,
    RunContext,
)

from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("slice_fraud_agent")
load_dotenv(".env.local")

BANK_NAME = "Slice Bank"
AGENT_NAME = "Akash"

# -----------------------------
# MongoDB connection helpers
# -----------------------------
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://127.0.0.1:27017")
DB_NAME = os.environ.get("MONGO_DB", "fraud_demo")
COLLECTION_NAME = os.environ.get("MONGO_COLLECTION", "fraud_cases")


def get_collection():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[COLLECTION_NAME]


# -----------------------------
# Create sample case (if missing)
# -----------------------------
def init_mongo_demo_case():
    col = get_collection()

    if col.find_one({"id": "case_001"}):
        return

    demo_case = {
        "id": "case_001",
        "userName": "Rahul Sharma",
        "securityIdentifier": "PW-78351",
        "cardEnding": "7742",
        "amount": "₹6,299",
        "merchant": "UrbanTech Gadgets",
        "timestamp": "2025-11-23 11:45",
        "location": "Mumbai (online)",
        "category": "electronics",
        "source": "urbantech.in",
        "status": "pending_review",
        "notes": "",
    }

    col.insert_one(demo_case)
    print(f"[Mongo] Inserted demo fraud case into {DB_NAME}.{COLLECTION_NAME}")


def load_case(case_id="case_001"):
    col = get_collection()
    return col.find_one({"id": case_id}, {"_id": 0})


def update_case_status(case_id, status, note):
    col = get_collection()
    col.update_one({"id": case_id}, {"$set": {"status": status, "notes": note}})
    logger.info("[Mongo] Updated case %s -> %s (%s)", case_id, status, note)


# -----------------------------
# Runtime State
# -----------------------------
@dataclass
class FraudState:
    case_id: str
    current_case: dict
    verified: bool = False


@dataclass
class Userdata:
    fraud_state: FraudState
    agent_session: Optional[AgentSession] = None


# -----------------------------
# Tool: mark_fraud_case
# -----------------------------
@function_tool
async def mark_fraud_case(
    ctx: RunContext[Userdata],
    status: Annotated[str, Field(description="confirmed_safe | confirmed_fraud | verification_failed")],
    note: Annotated[str, Field(description="Outcome summary note")],
):
    state = ctx.userdata.fraud_state
    status = status.lower().strip()

    if status not in ("confirmed_safe", "confirmed_fraud", "verification_failed"):
        return "Invalid status."

    update_case_status(state.case_id, status, note.strip())

    if status == "confirmed_safe":
        return "Case updated as safe."
    elif status == "confirmed_fraud":
        return "Case updated as fraud."
    return "Verification failed recorded."


# -----------------------------
# Agent Definition
# -----------------------------
class FraudAlertAgent(Agent):
    def __init__(self, case):
        user_name = case.get("userName", "")
        sec_id = case.get("securityIdentifier", "")
        card_ending = case.get("cardEnding", "XXXX")
        amount = case.get("amount", "")
        merchant = case.get("merchant", "")
        tx_time = case.get("timestamp", "")
        tx_loc = case.get("location", "")
        category = case.get("category", "")
        source = case.get("source", "")

        instructions = f"""
You are {AGENT_NAME}, a calm and professional Fraud Prevention Officer from {BANK_NAME}.

You MUST follow this call flow strictly:

------------------------------------------------------------
1. INTRODUCTION
------------------------------------------------------------
- Start the call with:
  "Hello, this is {AGENT_NAME} calling from the Fraud Prevention Team at {BANK_NAME}."
- Explain:
  "We're reaching out regarding a suspicious transaction on your card ending with {card_ending}."

------------------------------------------------------------
2. IDENTITY VERIFICATION (TWO STEPS)
------------------------------------------------------------

STEP 1 — FULL NAME:
- Say: "For verification, may I know your full name as per your account?"
- Expected name: "{user_name}" (INTERNAL ONLY – DO NOT speak this)
- Accept minor variations like spelling mistakes or missing last name.
- If mismatch continues → politely stop the call:
  - Call tool mark_fraud_case with:
      status="verification_failed"
      note="Name verification failed; call ended."

STEP 2 — SECURITY IDENTIFIER:
- Say: "Thank you. Could you please confirm your security identifier?"
- Expected: "{sec_id}" (INTERNAL ONLY – DO NOT speak this)
- Accept minor pauses or hyphens.
- If mismatch → verification_failed via tool.

------------------------------------------------------------
3. FRAUD EXPLANATION (IF VERIFIED)
------------------------------------------------------------
- Summarize the suspicious transaction:
  - Amount: {amount}
  - Merchant: {merchant}
  - Category: {category}
  - Location: {tx_loc}
  - Time: {tx_time}
  - Source: {source}
- Ask:
  "Did you make this transaction?"

------------------------------------------------------------
4. DECISION LOGIC
------------------------------------------------------------

IF user says YES (legitimate):
- Reassure them.
- Call mark_fraud_case:
    status="confirmed_safe"
    note="Customer confirmed the transaction as legitimate."

IF user says NO (fraud):
- Calmly say you will block the card and begin a dispute (demo).
- Call mark_fraud_case:
    status="confirmed_fraud"
    note="Customer denied transaction; card blocked (demo)."

------------------------------------------------------------
5. SAFETY RULES
------------------------------------------------------------
NEVER ask for:
- Full card number
- PIN
- OTP
- Password
- Net banking details

------------------------------------------------------------
6. END
------------------------------------------------------------
- Give a final short summary.
- Say goodbye politely.
"""

        super().__init__(instructions=instructions, tools=[mark_fraud_case])


# -----------------------------
# Prewarm
# -----------------------------
def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()
    init_mongo_demo_case()


# -----------------------------
# Entrypoint
# -----------------------------
async def entrypoint(ctx: JobContext):
    print(f"Starting Slice Bank - Fraud Alert Voice Agent (Agent: {AGENT_NAME})")

    init_mongo_demo_case()
    case = load_case("case_001")

    fraud_state = FraudState(case_id=case["id"], current_case=case)
    userdata = Userdata(fraud_state=fraud_state)

    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=murf.TTS(voice="en-US-matthew", style="Promo", text_pacing=True),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        userdata=userdata,
    )

    userdata.agent_session = session

    await session.start(
        agent=FraudAlertAgent(case),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC()
        ),
    )
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
