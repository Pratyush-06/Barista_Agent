# backend/src/agent.py  (replace your current file with this)
import logging
import json
import os
from typing import Annotated

from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("voice-agent")
logging.basicConfig(level=logging.INFO)

# Attempt to import LiveKit agent components
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
except Exception as e:
    logger.exception("Failed to import livekit.agents - are the package deps installed?")
    raise

# Try to import plugins; provide safe fallbacks if imports fail
# murf
try:
    from livekit.plugins import murf
    MURF_AVAILABLE = True
except Exception:
    murf = None
    MURF_AVAILABLE = False
    logger.warning("livekit.plugins.murf not available; TTS will be disabled or fallback.")

# silero (VAD)
try:
    from livekit.plugins import silero
    SILERO_AVAILABLE = True
except Exception:
    silero = None
    SILERO_AVAILABLE = False
    logger.warning("livekit.plugins.silero not available; using simple VAD fallback.")

# deepgram (STT)
try:
    from livekit.plugins import deepgram
    DEEPGRAM_AVAILABLE = True
except Exception:
    deepgram = None
    DEEPGRAM_AVAILABLE = False
    logger.warning("livekit.plugins.deepgram not available; STT may be disabled.")

# google (LLM)
try:
    from livekit.plugins import google
    GOOGLE_AVAILABLE = True
except Exception:
    google = None
    GOOGLE_AVAILABLE = False
    logger.warning("livekit.plugins.google not available; LLM may be disabled.")

# --- TOOL: save_order ---
@function_tool
async def save_order(
    drink_type: Annotated[str, "The type of coffee (e.g., Latte, Cappuccino)"],
    size: Annotated[str, "The size (Small, Medium, Large)"],
    milk: Annotated[str, "Milk type (Whole, Oat, Almond, None)"],
    extras: Annotated[str, "Extras (Sugar, Syrup, None)"],
    name: Annotated[str, "Customer name"]
):
    """Save the order to a file once all details are collected."""
    # normalize extras into list
    extras_list = []
    if extras and extras.strip().lower() not in ("none", "no", ""):
        extras_list = [x.strip() for x in extras.split(",") if x.strip()]

    order_data = {
        "drinkType": drink_type.strip(),
        "size": size.strip(),
        "milk": milk.strip(),
        "extras": extras_list,
        "name": name.strip()
    }

    # ensure orders folder
    orders_dir = os.path.join(os.path.dirname(__file__), "..", "orders")
    os.makedirs(orders_dir, exist_ok=True)
    out_path = os.path.join(orders_dir, "latest_order.json")

    logger.info(f"Saving order to {out_path}: {order_data}")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(order_data, f, indent=2, ensure_ascii=False)

    return f"Order saved to {out_path}. It will be ready in about 5 minutes."

# --- AGENT ENTRYPOINT ---
async def entrypoint(ctx: JobContext):
    # Connect to the room
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    participant = await ctx.wait_for_participant()

    # Prepare tool list (we always include save_order)
    tools = [save_order]

    # Build agent instructions
    instructions = (
        "You are a friendly barista at 'Starbucks'. "
        "Collect these 5 pieces of info: Drink, Size, Milk, Extras, Name. "
        "Ask clarifying questions. Once you have ALL info, call 'save_order'."
    )

    agent = Agent(instructions=instructions, tools=tools)

    # Prepare session components with graceful fallbacks
    # VAD
    vad = None
    if SILERO_AVAILABLE:
        try:
            vad = silero.VAD.load()
        except Exception:
            logger.exception("silero.VAD.load() failed - falling back to None VAD")
            vad = None

    # STT
    stt = None
    if DEEPGRAM_AVAILABLE:
        try:
            stt = deepgram.STT()
        except Exception:
            logger.exception("Failed to initialize Deepgram STT")
            stt = None

    # LLM
    llm_plugin = None
    if GOOGLE_AVAILABLE:
        try:
            llm_plugin = google.LLM()
        except Exception:
            logger.exception("Failed to initialize Google LLM")
            llm_plugin = None

    # TTS (Murf Falcon) - use env var safely and fallback if missing
    murf_key = os.environ.get("MURF_API_KEY")
    tts_plugin = None
    if MURF_AVAILABLE and murf_key:
        try:
            # model name might vary; keep this generic
            tts_plugin = murf.TTS(model="en-US-falcon", api_key=murf_key)
        except Exception:
            logger.exception("Failed to initialize Murf TTS plugin; TTS disabled")
            tts_plugin = None
    else:
        if not MURF_AVAILABLE:
            logger.warning("Murf plugin not available; no TTS will be used.")
        if not murf_key:
            logger.warning("MURF_API_KEY missing; set it in backend/.env.local to enable TTS.")

    # If llm or stt are missing, agent can still run in text-only demo mode, but warn
    if not llm_plugin:
        logger.warning("LLM plugin not available. Agent may not produce full intelligent replies.")
    if not stt:
        logger.warning("STT plugin not available. You may need to use text input instead.")

    session = AgentSession(
        vad=vad,
        stt=stt,
        llm=llm_plugin,
        tts=tts_plugin,
    )

    # Start the session
    await session.start(agent=agent, room=ctx.room)

    # Greet
    await session.generate_reply(instructions="Greet the customer warmly and ask what they'd like to order")

if __name__ == "__main__":
    try:
        cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
    except Exception:
        logger.exception("Failed to run the agent app")
        raise
