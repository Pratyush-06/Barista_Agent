# E-Commerce Agent (ACP Architecture) (Day 9)

## Overview
Inspired by the Agentic Commerce Protocol (ACP), this branch separates the "Conversational Layer" from the "Merchant Layer." The agent acts as a buyer proxy, interfacing with a simulated merchant API to discover products and finalize transactions.

## Architecture
* **Buyer Agent:** The Voice Interface (LiveKit + Gemini) that understands user needs.
* **Merchant Interface:** A structured Python API representing a store's inventory and checkout endpoints.
* **Protocol:** JSON-based communication between the Agent and the Merchant.

## Technical Implementation
* **Structured Output:** Forced Gemini to output responses in strict JSON format when interacting with the Merchant API, ensuring code reliability.
* **Transaction Flow:** Implemented a multi-step confirmation flow (Search → Select → Confirm → Payment Simulation).

## Stack
* **STT:** Deepgram
* **LLM:** Google Gemini
* **TTS:** Murf Falcon
