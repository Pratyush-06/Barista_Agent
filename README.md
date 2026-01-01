# Interactive RPG Game Master Engine (Day 8)

## Overview
This branch demonstrates the capability of Voice Agents to manage complex game states. The agent acts as a Dungeon Master (DM), narrating a story, tracking user Health Points (HP), and performing dice rolls (RNG) based on user actions.

## Core Components
* **World State:** A JSON object tracking current location, inventory, and player stats.
* **RNG Integration:** The agent calls a Python function to generate random numbers (1-20) for skill checks, influencing the narrative outcome.
* **Narrative Adaptation:** Gemini generates story segments dynamically based on the success/failure of the RNG.

## Technical Implementation
* **Function Calling for Game Logic:** The LLM does not calculate probability; it invokes a `roll_dice()` function and uses the returned integer to determine the narrative path.
* **Murf TTS Styles:** Utilized specific "Narration" voice styles within Murf to differentiate between storytelling and system announcements.

## Stack
* **STT:** Deepgram
* **LLM:** Google Gemini
* **TTS:** Murf Falcon
