"""
Coding Tutor Agent
Company: Physics Wallah

This file mirrors the Day 4 Teach-the-Tutor pattern but for Programming/Coding.
Features:
- Small JSON knowledge base (coding_tutor_content.json) auto-created on first run.
- Three modes: learn (Matthew), quiz (Alicia), teach_back (Ken).
- LiveKit agent integration placeholders and Murf TTS configuration.

Run: python coding_tutor_agent.py
"""

import logging
import json
import os
from dataclasses import dataclass
from typing import Literal, Optional, Annotated

from dotenv import load_dotenv
from pydantic import Field
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

# Plugins
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("coding_tutor_agent")
load_dotenv(".env.local")

# -----------------------------
# Company name
# -----------------------------
COMPANY_NAME = "Physics Wallah"

# -----------------------------
# Content file
# -----------------------------
DATA_DIR = "shared-data"
CONTENT_FILE = os.path.join(DATA_DIR, "coding_tutor_content.json")

DEFAULT_CONTENT = [
    {
        "id": "variables",
        "title": "Variables & Data Types",
        "summary": "Variables are containers for storing data values. In Python, you create a variable the moment you assign a value to it. Common data types include Integers (whole numbers), Floats (decimals), Strings (text), and Booleans (True/False).",
        "sample_question": "What is the difference between an Integer and a String?"
    },
    {
        "id": "loops",
        "title": "Loops",
        "summary": "Loops allow you to repeat a block of code. A 'for' loop is used for iterating over a sequence (like a list, tuple, or string). A 'while' loop repeats as long as a specific condition remains true.",
        "sample_question": "When would you use a 'for' loop instead of a 'while' loop?"
    },
    {
        "id": "functions",
        "title": "Functions",
        "summary": "A function is a block of code which only runs when it is called. You can pass data, known as parameters, into a function. A function can return data as a result. In Python, they are defined using the 'def' keyword.",
        "sample_question": "Why do we use functions in programming instead of writing the same code twice?"
    },
    {
        "id": "conditionals",
        "title": "Conditionals (If/Else)",
        "summary": "Conditionals support logical conditions from mathematics. They allow the program to make decisions. Python uses 'if', 'elif', and 'else' keywords to execute code only if certain conditions are met.",
        "sample_question": "Explain how an 'if-else' statement controls the flow of a program."
    }
]


def ensure_content_file():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CONTENT_FILE):
        with open(CONTENT_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONTENT, f, indent=2)
        print(f"Created sample content at {CONTENT_FILE}")


def load_content():
    ensure_content_file()
    with open(CONTENT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

COURSE_CONTENT = load_content()

# -----------------------------
# State
# -----------------------------
@dataclass
class TutorState:
    current_topic_id: Optional[str] = None
    current_topic_data: Optional[dict] = None
    mode: Literal["learn", "quiz", "teach_back"] = "learn"

    def set_topic(self, topic_id: str) -> bool:
        topic_id = topic_id.lower()
        topic = next((t for t in COURSE_CONTENT if t["id"] == topic_id), None)
        if topic:
            self.current_topic_id = topic_id
            self.current_topic_data = topic
            return True
        return False

@dataclass
class Userdata:
    tutor_state: TutorState
    agent_session: Optional[AgentSession] = None

# -----------------------------
# Tools
# -----------------------------
@function_tool
async def select_topic(
    ctx: RunContext[Userdata],
    topic_id: Annotated[str, Field(description="topic id to select")]
) -> str:
    state = ctx.userdata.tutor_state
    ok = state.set_topic(topic_id)
    if ok:
        return f"Topic set to {state.current_topic_data['title']}. Ask me to 'learn', 'quiz', or 'teach_back'."
    avail = ", ".join([t["id"] for t in COURSE_CONTENT])
    return f"Topic not found. Available topics: {avail}"

@function_tool
async def set_learning_mode(
    ctx: RunContext[Userdata],
    mode: Annotated[str, Field(description="learn | quiz | teach_back")]
) -> str:
    state = ctx.userdata.tutor_state
    mode = mode.lower()
    if mode not in ("learn", "quiz", "teach_back"):
        return "Mode must be one of: learn, quiz, teach_back"
    state.mode = mode

    s = ""
    session = ctx.userdata.agent_session
    if session:
        if mode == "learn":
            session.tts.update_options(voice="en-US-matthew", style="Promo")
            s = f"Mode LEARN. Ready to explain: {state.current_topic_data.get('title') if state.current_topic_data else 'no topic selected'}"
        elif mode == "quiz":
            session.tts.update_options(voice="en-US-alicia", style="Conversational")
            s = "Mode QUIZ. I will ask a question to test your coding knowledge."
        else:
            session.tts.update_options(voice="en-US-ken", style="Promo")
            s = "Mode TEACH_BACK. Ask the user to explain the code concept back to you."
    else:
        s = "Mode set locally. No active session for voice change."

    return f"Switched to {mode} mode. {s}"

@function_tool
async def evaluate_teaching(
    ctx: RunContext[Userdata],
    user_explanation: Annotated[str, Field(description="user's teach-back explanation")]
) -> str:
    # Very simple scoring: overlap with summary keywords
    topic = ctx.userdata.tutor_state.current_topic_data or {}
    summary = topic.get("summary", "")
    expected_words = set(w.strip('.,?!').lower() for w in summary.split())
    answer_words = set(w.strip('.,?!').lower() for w in user_explanation.split())
    if not expected_words:
        return "No topic selected to evaluate."
    overlap = expected_words & answer_words
    score = int( (len(overlap) / max(1, len(expected_words))) * 10 )
    if score >= 8:
        feedback = "Excellent — you covered the technical definitions perfectly."
    elif score >= 5:
        feedback = "Good — you understood the core logic."
    elif score >= 3:
        feedback = "A start — try to use more specific programming terminology."
    else:
        feedback = "Needs work — try reviewing the concept definition again."
    return f"Score: {score}/10. {feedback}"

# -----------------------------
# Agent
# -----------------------------
class CodingTutorAgent(Agent):
    def __init__(self):
        topic_list = ", ".join([f"{t['id']} ({t['title']})" for t in COURSE_CONTENT])
        super().__init__(
            instructions=f"""
            You are a Coding and Programming Tutor for {COMPANY_NAME}.

            AVAILABLE TOPICS: {topic_list}

            MODES:
              - LEARN (voice: Matthew): explain the coding concept simply and give one code example (describe the code verbally).
              - QUIZ (voice: Alicia): ask the sample_question from content and wait for a short answer.
              - TEACH_BACK (voice: Ken): ask the user to explain the concept back (like variables or loops) and provide corrective feedback.

            BEHAVIOR:
              - Start by asking which coding topic the user wants to study.
              - Use the tools select_topic, set_learning_mode, evaluate_teaching to manage state and scoring.
            """,
            tools=[select_topic, set_learning_mode, evaluate_teaching],
        )

# -----------------------------
# Entrypoint
# -----------------------------

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

async def entrypoint(ctx: JobContext):
    ctx.log_context_fields = {"room": ctx.room.name}
    print(f"Starting {COMPANY_NAME} - Coding Tutor")
    userdata = Userdata(tutor_state=TutorState())

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
        agent=CodingTutorAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(noise_cancellation=noise_cancellation.BVC()),
    )

    await ctx.connect()

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))