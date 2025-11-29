"""
Day 8 – Solo Leveling Inspired Voice Game Master (Short Demo Version)

Theme:
- Modern world with Gates & Dungeons (Solo Leveling style).
- You are a low-rank Hunter entering a dangerous dungeon.
- A mysterious "System" tracks your HP and Inventory and evaluates your actions.

Designed as a SHORT DEMO (4–6 turns) for LinkedIn video:
- Shows storytelling + dice checks + HP change + optional loot.
"""

import logging
import os
import random
from dataclasses import dataclass, field
from typing import List, Optional, Annotated

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

logger = logging.getLogger("day8_solo_gm")
logging.basicConfig(level=logging.INFO)
load_dotenv(".env.local")


# ---------------------------------------------------------
# Player / Game State
# ---------------------------------------------------------
@dataclass
class PlayerState:
    name: Optional[str] = None
    max_hp: int = 20
    hp: int = 20
    inventory: List[str] = field(default_factory=list)


@dataclass
class GameState:
    player: PlayerState
    location: str = "Standing at the entrance of a low-rank Gate."
    last_roll: Optional[dict] = None  # {"roll": int, "difficulty": str, "outcome": str, "action": str}


@dataclass
class Userdata:
    game: GameState
    agent_session: Optional[AgentSession] = None


# ---------------------------------------------------------
# Tools – used by the LLM as the "System"
# ---------------------------------------------------------
@function_tool
async def roll_check(
    ctx: RunContext[Userdata],
    action: Annotated[str, Field(
        description="Short description of what the Hunter is attempting, "
                    "e.g. 'slash the goblin', 'dodge the attack', 'sneak past the sentry'"
    )],
    difficulty: Annotated[str, Field(description="One of: 'easy', 'normal', 'hard'")],
) -> str:
    """
    Perform a d20 roll for a risky action.
    Interpreted as a 'System Check' in the Solo Leveling–style narrative.
    """
    diff = difficulty.lower().strip()
    if diff not in ("easy", "normal", "hard"):
        diff = "normal"

    roll = random.randint(1, 20)

    # thresholds
    if diff == "easy":
        if roll >= 10:
            outcome = "success"
        elif roll >= 5:
            outcome = "partial"
        else:
            outcome = "fail"
    elif diff == "hard":
        if roll >= 16:
            outcome = "success"
        elif roll >= 10:
            outcome = "partial"
        else:
            outcome = "fail"
    else:  # normal
        if roll >= 13:
            outcome = "success"
        elif roll >= 8:
            outcome = "partial"
        else:
            outcome = "fail"

    ctx.userdata.game.last_roll = {
        "roll": roll,
        "difficulty": diff,
        "outcome": outcome,
        "action": action,
    }

    return (
        f"System Check for action '{action}': d20 = {roll}, "
        f"difficulty = {diff}, outcome = {outcome}. "
        "Describe this as a Solo Leveling–style result: clean success, close call, or painful failure."
    )


@function_tool
async def modify_hp(
    ctx: RunContext[Userdata],
    amount: Annotated[int, Field(
        description="Positive to heal, negative for damage, e.g. -5 for damage, +3 for healing"
    )],
    reason: Annotated[str, Field(
        description="Short explanation like 'goblin slash', 'healing potion', 'trap explosion'"
    )],
) -> str:
    """
    Modify the Hunter's HP (damage or heal). Keeps HP between 0 and max_hp.
    """
    player = ctx.userdata.game.player

    old_hp = player.hp
    player.hp += amount
    if player.hp > player.max_hp:
        player.hp = player.max_hp
    if player.hp < 0:
        player.hp = 0

    if amount < 0:
        change_text = f"took {-amount} damage"
    elif amount > 0:
        change_text = f"recovered {amount} HP"
    else:
        change_text = "had no HP change"

    status = "alive"
    if player.hp == 0:
        status = "down"

    return (
        f"Hunter {change_text} due to: {reason}. "
        f"HP changed from {old_hp} to {player.hp} (max {player.max_hp}). "
        f"Hunter status: {status}. "
        "Narrate this like a System notification and describe how it looks/feels in the scene."
    )


@function_tool
async def add_item(
    ctx: RunContext[Userdata],
    item_name: Annotated[str, Field(
        description="Name of the item to add to inventory, e.g. 'rusty dagger', 'healing potion', 'shadow crystal'"
    )],
) -> str:
    """
    Add a new item to the Hunter's inventory.
    """
    player = ctx.userdata.game.player
    item = item_name.strip()
    if item and item not in player.inventory:
        player.inventory.append(item)
        return f"Added '{item}' to the Hunter's inventory. Current inventory: {player.inventory}."
    return f"Item '{item}' is already in inventory or invalid. Current inventory: {player.inventory}."


@function_tool
async def remove_item(
    ctx: RunContext[Userdata],
    item_name: Annotated[str, Field(description="Name of the item to remove from inventory")],
) -> str:
    """
    Remove an item from the Hunter's inventory.
    """
    player = ctx.userdata.game.player
    item = item_name.strip()
    if item in player.inventory:
        player.inventory.remove(item)
        return f"Removed '{item}' from the Hunter's inventory. Current inventory: {player.inventory}."
    return f"Item '{item}' was not in inventory. Current inventory: {player.inventory}."


@function_tool
async def get_status(
    ctx: RunContext[Userdata],
) -> str:
    """
    Get a 'Status Window' summary of the Hunter's current HP and inventory.
    """
    player = ctx.userdata.game.player
    inv = player.inventory or ["(empty)"]
    return (
        f"Status Window — HP: {player.hp}/{player.max_hp}. "
        f"Inventory: {', '.join(inv)}. "
        "Use this to answer questions like 'What do I have?' or 'How injured am I?'. "
        "Describe it as a glowing System panel appearing in front of the Hunter."
    )


# ---------------------------------------------------------
# Solo Leveling–Style GM Prompt (SHORT DEMO VERSION)
# ---------------------------------------------------------
SOLO_GM_PROMPT = """
You are a Solo Leveling–inspired **Dungeon Game Master System**.

This is a **SHORT DEMO RUN** for a LinkedIn video, so:
- Keep the entire adventure to **4–6 turns only**.
- Finish the story in **under ~2 minutes** of conversation.
- The Hunter must:
  - Enter the Gate,
  - Encounter ONE quick threat,
  - Use at least ONE System Check (dice roll),
  - Have at least ONE HP change (damage or heal),
  - Optionally gain ONE loot item.
- End with a CLEAR mini-ending (defeat the enemy, escape the Dungeon, or barely survive).

WORLD:
- Modern world where dimensional Gates appear, leading to monster-filled Dungeons.
- The player is a new, low-rank Hunter entering a small, suspicious Gate.

TONE:
- Tense, cool, Solo Leveling vibes.
- Keep narration short and punchy (3–4 sentences).
- Describe the world in the second person ("you").
- Occasionally mention glowing blue System messages appearing.

YOUR ROLE:
- You are both the **narrator** and the **System** of this Dungeon run.
- The player is the Hunter. You never act as the Hunter yourself.
- You ALWAYS end your reply with: **"What do you do?"**
  EXCEPT on the final turn where you clearly end the story.

TOOLS:
- Use `roll_check` when the Hunter attempts something risky.
- Use `modify_hp` when the Hunter takes damage or heals.
- Use `add_item` / `remove_item` for loot and inventory.
- Use `get_status` if the Hunter asks for their Status/Inventory.

HUNTER:
- Starts with HP 20/20 and empty inventory.
- Early on, ask for the Hunter's name and remember it.
- You may grant a basic starter weapon via `add_item` like "rusty dagger".

STRUCTURE (KEEP IT SHORT):
1. Turn 1:
   - Introduce the strange Gate and the Dungeon entrance.
   - Ask for the Hunter's name and what they want to do.

2. Turn 2:
   - Lead them inside (corridor/room).
   - Introduce a weak enemy or immediate threat.

3. Turn 3:
   - When they act (attack, dodge, etc.), call `roll_check` with a suitable difficulty.
   - Based on result, use `modify_hp` if needed.
   - Narrate outcome Solo Leveling–style.

4–5:
   - Resolve the conflict quickly (enemy defeated or escape).
   - Optionally `add_item` for loot.
   - Optionally `get_status` if they ask.

Final Turn:
   - Finish the mini-arc (Gate closes / escape / victory).
   - Do NOT say "What do you do?" on the final line; clearly end the story.

IMPORTANT:
- Do NOT mention tool names or raw dice values unless styled as in-universe System messages
  (e.g. "System: CHECK – SUCCESS").
- Do NOT say you are an AI or model. Stay fully in-universe.
"""


# ---------------------------------------------------------
# Agent Definition
# ---------------------------------------------------------
class SoloLevelingGameMasterAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions=SOLO_GM_PROMPT,
            tools=[roll_check, modify_hp, add_item, remove_item, get_status],
        )


# ---------------------------------------------------------
# Prewarm – load VAD
# ---------------------------------------------------------
def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


# ---------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------
async def entrypoint(ctx: JobContext):
    ctx.log_context_fields = {"room": ctx.room.name}
    print("Starting Day 8 – Solo Leveling Style Dungeon Game Master (Short Demo)")

    player = PlayerState()
    game = GameState(player=player)
    userdata = Userdata(game=game)

    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-flash"),
                tts = murf.TTS(
        model="en-US-falcon",
        api_key=os.environ["MURF_API_KEY"],
    ),


        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        userdata=userdata,
    )

    userdata.agent_session = session

    await session.start(
        agent=SoloLevelingGameMasterAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
