# backend/src/agent.py  -- Day 3: Wellness agent
import logging
import json
import os
from datetime import datetime
from typing import Annotated, Optional, List, Dict, Any

from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("wellness-agent")
logging.basicConfig(level=logging.INFO)

# --- LiveKit agent API (no pipeline here) ---
try:
    from livekit.agents import (
        AutoSubscribe,
        JobContext,
        WorkerOptions,
        cli,
        llm,
        Agent,
        AgentSession,
        function_tool,
    )
except Exception:
    logger.exception("Failed to import livekit.agents. Are dependencies installed?")
    raise

# --- Plugins ---
try:
    from livekit.plugins import murf
    MURF_AVAILABLE = True
except Exception:
    murf = None
    MURF_AVAILABLE = False
    logger.warning("livekit.plugins.murf not available; TTS disabled.")

try:
    from livekit.plugins import silero
    SILERO_AVAILABLE = True
except Exception:
    silero = None
    SILERO_AVAILABLE = False
    logger.warning("livekit.plugins.silero not available; VAD disabled.")

try:
    from livekit.plugins import deepgram
    DEEPGRAM_AVAILABLE = True
except Exception:
    deepgram = None
    DEEPGRAM_AVAILABLE = False
    logger.warning("livekit.plugins.deepgram not available; STT disabled.")

try:
    from livekit.plugins import google
    GOOGLE_AVAILABLE = True
except Exception:
    google = None
    GOOGLE_AVAILABLE = False
    logger.warning("livekit.plugins.google not available; LLM disabled.")

# --- Paths & helpers ---
BASE_DIR = os.path.dirname(__file__)
WELLNESS_LOG = os.path.normpath(os.path.join(BASE_DIR, "..", "wellness_log.json"))


def now_ts() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def read_all_entries() -> List[Dict[str, Any]]:
    if not os.path.exists(WELLNESS_LOG):
        return []
    try:
        with open(WELLNESS_LOG, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def last_entry() -> Optional[Dict[str, Any]]:
    entries = read_all_entries()
    if not entries:
        return None
    return entries[-1]


def last_entry_summary_line() -> Optional[str]:
    """Return a short spoken line summarizing the last check-in."""
    entry = last_entry()
    if not entry:
        return None
    mood = entry.get("mood", "").strip() or "unspecified"
    energy = entry.get("energy", "").strip() or "unspecified"
    objs = entry.get("objectives", [])
    objs_str = ", ".join(objs) if objs else "no specific objectives"
    return (
        f"Last time we talked, you said you were feeling {mood} "
        f"with energy {energy}, and your main goals were {objs_str}."
    )


# --- Tool: log_checkin (used by LLM at the end) ---
@function_tool
async def log_checkin(
    mood: Annotated[str, "Short mood description"],
    energy: Annotated[str, "Energy level (low/medium/high or text)"],
    objectives: Annotated[str, "One to three objectives (comma separated)"],
    summary: Annotated[str, "Short assistant-generated recap sentence"],
):
    """
    Append a wellness check-in entry to wellness_log.json.
    """
    entry = {
        "timestamp": now_ts(),
        "mood": mood.strip(),
        "energy": energy.strip(),
        "objectives": [o.strip() for o in objectives.split(",") if o.strip()],
        "summary": summary.strip(),
    }

    try:
        entries = read_all_entries()
        entries.append(entry)
        with open(WELLNESS_LOG, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)
        logger.info("Saved wellness entry: %s", entry)
        return "Saved your check-in. I'll remember this next time we talk."
    except Exception:
        logger.exception("Failed to save wellness_log.json")
        return "Sorry, I couldn't save your check-in due to a server error."


# --- Main entrypoint ---
async def entrypoint(ctx: JobContext):
    """
    Wellness companion agent (Day 3).
    - Uses last wellness_log.json entry to reference previous talk.
    - Asks questions one by one: mood -> energy -> stress -> objectives -> recap.
    """
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    participant = await ctx.wait_for_participant()

    tools = [log_checkin]

    # Build system instructions: strongly enforce ONE-BY-ONE questions
    prev_line = last_entry_summary_line()
    if prev_line:
        history_text = prev_line + " "
    else:
        history_text = "This seems to be the first check-in with this user. "

    instructions = f"""
{history_text}
You are a supportive, grounded wellness companion.

Your job:
1. Ask about the user's mood with ONE clear question. Wait for the answer before asking anything else.
2. Then ask about energy with ONE question. Wait for the answer.
3. Then ask if there is anything stressing them or on their mind. One question. Wait for answer.
4. Then ask about 1–3 simple objectives/goals for today. One question. Wait for answer.
5. Offer exactly ONE small, realistic suggestion (for example: take a 5-minute walk, a short stretch, a small break, or break a task into smaller steps).
6. Recap today's mood, energy, stress, and objectives in a short paragraph.
7. Ask: "Does this sound right?" and wait for the answer.
8. After the user confirms, call the tool 'log_checkin' with:
   - mood
   - energy
   - objectives (comma separated)
   - a short summary sentence.
9. Avoid any medical, diagnostic, or treatment advice. You are not a doctor or therapist.

VERY IMPORTANT:
- Ask ONLY ONE question per message.
- Do not combine multiple questions in the same reply.
- Keep answers short, warm, and conversational.
"""

    # Create Agent with string instructions (no ChatContext)
    agent = Agent(instructions=instructions, tools=tools)

    # Build plugins
    murf_key = os.environ.get("MURF_API_KEY")
    tts_plugin = None
    if MURF_AVAILABLE and murf_key:
        try:
            tts_plugin = murf.TTS(model="en-US-falcon", api_key=murf_key)
        except Exception:
            logger.exception("Failed to init Murf TTS; continuing without TTS")
            tts_plugin = None
    else:
        if not MURF_AVAILABLE:
            logger.warning("Murf plugin not available; TTS disabled.")
        if not murf_key:
            logger.warning("MURF_API_KEY not set; TTS disabled.")

    vad_plugin = None
    if SILERO_AVAILABLE:
        try:
            vad_plugin = silero.VAD.load()
        except Exception:
            logger.exception("silero.VAD.load failed; no VAD used.")
            vad_plugin = None

    stt_plugin = None
    if DEEPGRAM_AVAILABLE:
        try:
            stt_plugin = deepgram.STT()
        except Exception:
            logger.exception("deepgram.STT init failed; no STT used.")
            stt_plugin = None

    llm_plugin = None
    if GOOGLE_AVAILABLE:
        try:
            llm_plugin = google.LLM()
        except Exception:
            logger.exception("google.LLM init failed; no LLM used.")
            llm_plugin = None

    # Create session
    session = AgentSession(
        vad=vad_plugin,
        stt=stt_plugin,
        llm=llm_plugin,
        tts=tts_plugin,
    )

    # Start agent session
    try:
        await session.start(agent=agent, room=ctx.room)
    except TypeError:
        session.start(agent=agent, room=ctx.room)

    # 1) If we have past data, say it explicitly first
    if prev_line:
        try:
            await session.say(prev_line, allow_interruptions=True)
        except Exception:
            logger.exception("Failed to speak previous summary (non-fatal).")

    # 2) Then ask the FIRST question only: mood
    # After this, the LLM will follow the instructions to ask questions one by one.
    try:
        await session.generate_reply(
            instructions="Greet the user briefly and ask only one question: 'How are you feeling today?'"
        )
    except Exception:
        try:
            await session.say(
                "Hi, I'm your wellness companion. How are you feeling today?",
                allow_interruptions=True,
            )
        except Exception:
            logger.exception("Failed to send greeting / first question.")


if __name__ == "__main__":
    try:
        cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
    except Exception:
        logger.exception("Failed to run wellness agent")
        raise
