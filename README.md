# Voice-Activated Grocery Ordering System (Day 7)

## Overview
A voice commerce prototype allowing users to build a shopping cart. This requires the agent to understand intents related to quantity, product modifications, and removals. The challenge addressed here is converting natural language ambiguity ("Get me two packs of milk") into precise cart operations.

## Key Features
* **Intent Resolution:** Maps spoken requests to specific CRUD operations on the cart object.
* **Dynamic Cart Management:** State is maintained in Python and updated in real-time based on Gemini's tool outputs.
* **Order Summary:** The agent can read back the current state of the cart upon request.

## Technical Implementation
* **Product Catalog:** Injected a static JSON product catalog into the LLM context window to ensure the agent only "sells" items that exist.
* **Quantity Parsing:** Logic to handle numerical words ("dozen", "pair", "five") and convert them to integers for the cart logic.

## Stack
* **STT:** Deepgram
* **LLM:** Google Gemini
* **TTS:** Murf Falcon
