"""
Day 10 – Improv Battle Voice Agent
Single-player voice improv game show host.

Game: "Improv Battle"
- AI is the high-energy host.
- Runs N rounds (e.g. 3).
- Each round:
  1) Host gives a fun scenario.
  2) Player improvises in character.
  3) Host reacts (sometimes praise, sometimes light critique).
- Keeps simple state (player_name, current_round, rounds info).
"""

import logging
import os
from dataclasses import dataclass, field
from typing import Annotated, Optional, List, Dict, Any

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

from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("improv_battle_agent")
logging.basicConfig(level=logging.INFO)

load_dotenv(".env.local")

SHOW_NAME = "Improv Battle"

# -----------------------------
# Improv Scenarios
# -----------------------------

SCENARIOS: List[Dict[str, str]] = [
    {
        "id": "s1",
        "title": "Time-Travel Phone Demo",
        "prompt": (
            "You are a time-traveling tour guide trying to explain modern smartphones "
            "to someone from the 1800s who thinks it's dark magic."
        ),
    },
    {
        "id": "s2",
        "title": "Escaped Order",
        "prompt": (
            "You are a restaurant waiter who has to calmly explain to a customer "
            "that their main course has escaped the kitchen and is running through the streets."
        ),
    },
    {
        "id": "s3",
        "title": "Cursed Return Counter",
        "prompt": (
            "You are a customer trying to return an obviously cursed object "
            "to a very skeptical shop owner who insists it's 'perfectly normal'."
        ),
    },
    {
        "id": "s4",
        "title": "Portal Latte",
        "prompt": (
            "You are a barista who has to tell a regular customer that their latte "
            "is actually a portal to another dimension, but try to keep them calm."
        ),
    },
    {
        "id": "s5",
        "title": "Over-Honest AI Assistant",
        "prompt": (
            "You are an AI assistant that suddenly becomes brutally honest during a product demo "
            "in front of investors."
        ),
    },
]

# -----------------------------
# State
# -----------------------------


@dataclass
class ImprovRound:
    scenario_id: str
    scenario_title: str
    scenario_prompt: str
    host_reaction: Optional[str] = None


@dataclass
class ImprovState:
    player_name: Optional[str] = None
    current_round: int = 0
    max_rounds: int = 3
    phase: str = "intro"  # "intro" | "awaiting_improv" | "reacting" | "done"
    rounds: List[ImprovRound] = field(default_factory=list)


@dataclass
class Userdata:
    improv_state: ImprovState
    agent_session: Optional[AgentSession] = None


# -----------------------------
# Tools
# -----------------------------


@function_tool
async def set_player_name(
    ctx: RunContext[Userdata],
    name: Annotated[str, Field(description="The contestant's name as they want to be introduced on the show")],
) -> str:
    """
    Save/override the player's name for this improv session.
    """
    state = ctx.userdata.improv_state
    name = name.strip()
    if not name:
        return "Name was empty, keep using the previous one or ask again."
    state.player_name = name
    logger.info("Player name set to %s", name)
    return f"Got it. The contestant's name is {name}. Introduce them with energy."


@function_tool
async def start_next_round(
    ctx: RunContext[Userdata],
) -> str:
    """
    Advance to the next round, pick a scenario, and return instructions for the host.
    """
    state = ctx.userdata.improv_state

    if state.current_round >= state.max_rounds:
        state.phase = "done"
        return (
            "All rounds are already complete. Move to the closing summary and end the show gracefully."
        )

    state.current_round += 1
    idx = (state.current_round - 1) % len(SCENARIOS)
    sc = SCENARIOS[idx]

    state.phase = "awaiting_improv"
    round_obj = ImprovRound(
        scenario_id=sc["id"],
        scenario_title=sc["title"],
        scenario_prompt=sc["prompt"],
    )
    state.rounds.append(round_obj)

    logger.info("Starting round %s with scenario %s", state.current_round, sc["id"])

    player = state.player_name or "our contestant"

    return (
        f"Round {state.current_round} of {state.max_rounds}.\n"
        f"Scenario title: {sc['title']}.\n"
        f"Scenario prompt: {sc['prompt']}\n\n"
        f"Address {player} directly, explain the scenario in a fun way, "
        f"and tell them to improvise in character for a short scene. "
        f"Ask them to say 'End scene' when they are finished."
    )


@function_tool
async def finish_round(
    ctx: RunContext[Userdata],
    reaction_summary: Annotated[
        str,
        Field(
            description=(
                "1–3 sentences summarizing how the player performed in this scene, "
                "including a mix of positive and lightly critical feedback."
            )
        ),
    ],
) -> str:
    """
    Mark the current round as reacted to and store the host's reaction.
    """
    state = ctx.userdata.improv_state

    if not state.rounds:
        return "There is no active round. Just continue the conversation."

    last_round = state.rounds[-1]
    last_round.host_reaction = reaction_summary.strip()
    state.phase = "reacting"

    logger.info(
        "Finished round %s with reaction: %s",
        state.current_round,
        last_round.host_reaction,
    )

    if state.current_round >= state.max_rounds:
        state.phase = "done"
        return (
            "Stored the reaction. All rounds are complete. "
            "Now move to a closing segment where you summarize the player's overall improv style, "
            "call out one or two specific scenes, and end the show."
        )

    # More rounds to go
    state.phase = "intro"
    return (
        "Stored the reaction for this round. "
        "Tell the player how many rounds are left, then smoothly transition into setting up the next round. "
        "You may call 'start_next_round' again when you are ready."
    )


@function_tool
async def early_exit(
    ctx: RunContext[Userdata],
    reason: Annotated[str, Field(description="Short reason why the player wanted to stop the game")],
) -> str:
    """
    Mark the game as ended early.
    """
    state = ctx.userdata.improv_state
    state.phase = "done"

    logger.info("Early exit requested: %s", reason)
    return (
        "Mark the game as ended early. Briefly acknowledge the reason, "
        "thank the player for playing Improv Battle, and end the show warmly."
    )


# -----------------------------
# Agent Definition
# -----------------------------


class ImprovBattleAgent(Agent):
    def __init__(self):
        instructions = f"""
You are the high-energy host of a TV improv show called "{SHOW_NAME}".

TONE & STYLE:
- You are witty, energetic, and keep the vibe fun.
- You explain the rules clearly.
- Your reactions are realistic and varied:
  - Sometimes amused, sometimes unimpressed, sometimes pleasantly surprised.
  - You may lightly tease or critique, but always stay respectful, safe, and constructive.
- Keep replies concise enough for a spoken experience (usually 2–5 sentences).

GAME FLOW (SINGLE PLAYER):
- There is exactly one player (contestant) connected by voice.
- Start the show by:
  1) Welcoming the audience and the player.
  2) Briefly explaining the rules: there will be multiple short improv scenarios, they play the character, then you react.
  3) Asking the player for their name if you don't know it yet, then call 'set_player_name'.

ROUNDS:
- The backend holds an improv_state object with:
  - player_name, current_round, max_rounds, rounds, and phase.
- You MUST use the tools to manage state, instead of inventing it yourself:
  - Use 'set_player_name' to record or change the contestant's name.
  - Use 'start_next_round' to start each new scenario.
  - Use 'finish_round' after you have reacted to a scene.
  - Use 'early_exit' if the player clearly wants to stop the game.

PER ROUND:
1) Call 'start_next_round' to get a scenario.
2) Announce it as "Round N", describe the scenario with enthusiasm.
3) Instruct the player:
   - to act in character,
   - to improvise a short scene,
   - and to say "End scene" when they are done.
4) Listen to the player's performance.
5) When they are clearly finished (they say "End scene", or explicitly say they're done):
   - Give a reaction that mentions specific things you heard.
   - Include a mix of positive and lightly critical feedback (pacing, commitment, character, creativity).
   - Then call 'finish_round' with a short text summary of your reaction.

VARIED REACTIONS:
- Randomly vary your tone across scenes:
  - Sometimes very supportive and excited.
  - Sometimes honest and slightly critical ("felt a bit rushed", "could lean more into character").
  - Sometimes mixed ("great premise, but you could build more detail").
- Never be abusive, insulting, or mean. This should feel like a friendly show.

CLOSING:
- After 'finish_round' tells you all rounds are complete, or after an 'early_exit':
  - Give a short closing monologue:
    - Summarize what kind of improviser the player seems to be
      (e.g. stronger at character, absurdity, emotional range, etc.).
    - Mention 1–2 specific funny or interesting moments from the rounds.
    - Thank them for playing "{SHOW_NAME}" and say goodbye.

EARLY EXIT:
- If the user says things like "stop game", "end show", or "I'm done" before all rounds are complete:
  - Confirm that they want to end.
  - If they confirm, call 'early_exit' with a short reason (e.g. "player chose to stop after round 2").
  - Then do a short, polite outro and end the conversation.

KEEP THE CONVERSATION CLEAR:
- End most of your turns with a clear prompt to the player:
  - e.g. "Ready for the next scenario?" or "Whenever you're ready, start your scene and say 'End scene' when you're done."
"""
        super().__init__(
            instructions=instructions,
            tools=[set_player_name, start_next_round, finish_round, early_exit],
        )


# -----------------------------
# Prewarm
# -----------------------------


def prewarm(proc: JobProcess):
    # Load VAD once and reuse
    proc.userdata["vad"] = silero.VAD.load()


# -----------------------------
# Entrypoint
# -----------------------------


async def entrypoint(ctx: JobContext):
    ctx.log_context_fields = {"room": ctx.room.name}
    print(f"Starting {SHOW_NAME} – Day 10 Improv Battle Agent")

    improv_state = ImprovState(
        player_name=None,
        current_round=0,
        max_rounds=3,
        phase="intro",
        rounds=[],
    )
    userdata = Userdata(improv_state=improv_state)

    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=murf.TTS(
            model="en-US-falcon",
            api_key=os.environ.get("MURF_API_KEY", ""),
        ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        userdata=userdata,
    )

    userdata.agent_session = session

    await session.start(
        agent=ImprovBattleAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
