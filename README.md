# Persistent State Wellness Check-In Agent (Day 3)

## Overview
This branch introduces data persistence to the voice agent. The Wellness Agent conducts a daily health check-in, parses the user's sentiment, and stores the data structurally. This moves the application from ephemeral interactions to stateful sessions where previous data influences current dialogue.

## Core Functionality
* **Sentiment Analysis:** Uses Gemini to implicitly analyze the user's mood based on voice transcriptions.
* **Data Serialization:** Captures conversation outcomes and serializes them into local JSON storage.
* **Session Recall:** Upon initialization, the agent reads previous entries to greet the user contextually (e.g., asking about a previously mentioned issue).

## Implementation Details
* **Storage Layer:** Implemented a lightweight JSON-based file system to mock database interactions.
* **System Prompting:** Instructed Gemini to adopt an empathetic persona and prioritize follow-up questions based on historical data.
* **Deepgram Configuration:** Optimized for "conversational" models to better capture emotional inflection logic via text.

## Stack
* **STT:** Deepgram
* **LLM:** Google Gemini
* **TTS:** Murf Falcon
* **Storage:** Local JSON
