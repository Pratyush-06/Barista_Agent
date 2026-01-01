# Voice Agent Architecture Prototype (Day 1)

## Overview
This branch establishes the foundational architecture for a real-time voice AI agent. Unlike traditional HTTP request-response models, this implementation utilizes a WebSocket-based full-duplex connection to handle audio streams. The primary objective is to minimize latency in the Speech-to-Text (STT) → Large Language Model (LLM) → Text-to-Speech (TTS) pipeline.

## System Architecture
The application operates on an event-driven loop:
1.  **Input:** User audio is captured via the React frontend and streamed to the backend via LiveKit.
2.  **Transduction (STT):** **Deepgram Nova-2** processes raw audio into text in real-time.
3.  **Reasoning (LLM):** **Google Gemini** processes the textual input and generates a conversational response.
4.  **Synthesis (TTS):** **Murf Falcon** converts the LLM response into high-fidelity audio.
5.  **Output:** Audio is streamed back to the client.

## Tech Stack
* **Orchestration:** LiveKit Agents
* **STT:** Deepgram (Real-time Streaming)
* **LLM:** Google Gemini 1.5 Flash
* **TTS:** Murf Falcon
* **Backend:** Python
* **Frontend:** React (TypeScript)

## Implementation Details
* Established the foundational `Worker` class for agent dispatch.
* Configured environment variables for API authentication across three different providers.
* Implemented basic error handling for audio stream interruptions.
