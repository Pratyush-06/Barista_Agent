# Automated Sales Development (SDR) Agent (Day 5)

## Overview
A functional implementation of an outbound/inbound Sales Development Representative agent. This branch focuses on "Slot Filling"—the ability to extract specific entities (Name, Company, Budget, Timeline) from unstructured voice input and structure them into a lead object.

## Key Features
* **Entity Extraction:** Parses unstructured conversation to identify key qualification criteria (BANT framework).
* **Conversation Steering:** If a piece of data is missing, the agent logic specifically prompts for that information.
* **Lead Object Generation:** Converts the final conversation state into a structured JSON payload ready for CRM integration.

## Technical Implementation
* **Tool Calling:** Utilized Gemini’s function calling capabilities to identify when a slot (e.g., `user_email`) has been satisfied.
* **Deepgram Keyword Boosting:** Applied keyword boosting for alphanumeric characters to improve accuracy on email addresses and phone numbers.

## Stack
* **STT:** Deepgram
* **LLM:** Google Gemini
* **TTS:** Murf Falcon
