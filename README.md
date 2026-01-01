# Low-Latency Improv Game Engine (Day 10)

## Overview
The final branch focuses on the limits of real-time interaction. This is an "Improv Battle" game where timing is critical. The agent must respond rapidly with wit and personality. This branch pushes the optimization of the Deepgram → Gemini → Murf pipeline to its limit.

## Performance Optimizations
* **Prompt Caching:** Utilized context caching for the static "Game Rules" prompt to reduce input token processing time.
* **Aggressive End-pointing:** Tuned Deepgram to detect end-of-speech faster (reduced silence threshold) to keep the game momentum high.
* **Streaming TTS:** Initiated Murf audio stream on the first valid sentence chunk received from Gemini.

## Technical Implementation
* **Persona Tuning:** High-temperature settings on Gemini (0.9) to maximize creativity and unpredictability in responses.
* **Session Timer:** Implemented a background asyncio task to manage round timing independent of the conversation loop.

## Stack
* **STT:** Deepgram (Nova-2 Fastest Model)
* **LLM:** Google Gemini 1.5 Flash
* **TTS:** Murf Falcon
