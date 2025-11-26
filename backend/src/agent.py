import os
import json
import logging
from typing import Annotated, Optional, Dict
from difflib import SequenceMatcher
from dataclasses import dataclass

from dotenv import load_dotenv

from livekit.agents import (
    AutoSubscribe,
    JobContext,
    Agent,
    AgentSession,
    WorkerOptions,
    cli,
    function_tool
)

from livekit.plugins import google, deepgram, murf, silero

load_dotenv()
logger = logging.getLogger("zomato-sdr")

BASE = os.path.dirname(__file__)
ROOT = os.path.normpath(os.path.join(BASE, "..", ".."))
CONTENT_FILE = os.path.join(ROOT, "shared-data", "day5_company_content.json")
LEADS_FILE = os.path.join(BASE, "..", "day5_zomato_leads.json")


# ------------------------------------------------------
# Load Company Data
# ------------------------------------------------------
def load_company():
    if not os.path.exists(CONTENT_FILE):
        raise FileNotFoundError("Zomato SDR content missing.")
    with open(CONTENT_FILE, "r") as f:
        return json.load(f)


COMPANY = load_company()


# ------------------------------------------------------
# Lead State
# ------------------------------------------------------
@dataclass
class LeadState:
    data: Dict[str, Optional[str]]

    def __init__(self):
        self.data = {field: None for field in COMPANY["lead_fields"]}

    def set(self, key, val):
        if key in self.data:
            self.data[key] = val

    def missing_fields(self):
        return [k for k, v in self.data.items() if not v]

    def is_complete(self):
        return all(self.data.values())

    def summary(self):
        return "; ".join([f"{k}: {v}" for k, v in self.data.items()])


# ------------------------------------------------------
# FAQ Answer Retrieval
# ------------------------------------------------------
def find_faq_answer(q: str) -> Optional[str]:
    q = q.lower()
    best = None
    best_ratio = 0.0

    for item in COMPANY["faq"]:
        ratio = SequenceMatcher(None, q, item["q"].lower()).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best = item["a"]

    return best if best_ratio >= 0.35 else None


# ------------------------------------------------------
# Tool: Save Lead
# ------------------------------------------------------
@function_tool
async def save_lead(
    lead_data: Annotated[dict, "Lead data to save"]
) -> str:
    """Save final lead to JSON file."""
    existing = []
    if os.path.exists(LEADS_FILE):
        try:
            with open(LEADS_FILE, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except Exception:
            existing = []

    existing.append(lead_data)

    with open(LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    return "Saved lead successfully."


# ------------------------------------------------------
# SDR Instructions
# ------------------------------------------------------
INSTRUCTIONS = f"""
You are a Sales Development Representative for {COMPANY["company"]}.

Your job:
1. Greet the user warmly.
2. Ask what they are looking for.
3. Use FAQ to answer questions about {COMPANY["company"]}. DO NOT invent anything outside the FAQ.
4. Ask for lead details one by one (only one question at a time):
   {", ".join(COMPANY["lead_fields"])}
5. Understand signals like: “that's all”, “done”, “nothing else”, “thanks”.
6. When user is done:
   - Give a short verbal summary of all collected lead details.
   - Call save_lead to store the JSON.
7. Keep replies friendly, short, and clear.
"""


# ------------------------------------------------------
# Entrypoint
# ------------------------------------------------------
async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    participant = await ctx.wait_for_participant()

    lead = LeadState()

    agent = Agent(
        instructions=INSTRUCTIONS,
        tools=[save_lead]
    )

    session = AgentSession(
        stt=deepgram.STT(),
        llm=google.LLM(),
        tts=murf.TTS(model="en-US-falcon", api_key=os.getenv("MURF_API_KEY")),
        vad=silero.VAD.load(),
        userdata={"lead": lead},
    )

    await session.start(agent=agent, room=ctx.room)

    await session.say(
        f"Hi! I'm the SDR from {COMPANY['company']}. How can I help you today?",
        allow_interruptions=True
    )


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
