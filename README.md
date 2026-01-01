# Secure Identity Verification Agent (Day 6)

## Overview
This branch simulates a banking fraud alert workflow. The priority here is deterministic conversation flows and security. Unlike open-ended chat agents, this agent is restricted to a specific state machine to verify user identity before disclosing sensitive "account" details.

## Architecture
* **State Machine:** Implemented a strict logic flow (Greeting → Verification → Incident Report → Resolution). The agent cannot proceed to step 3 without explicit boolean confirmation in step 2.
* **PII Handling:** Input masking implementation for simulated sensitive data (PINs/DOB).

## Technical Implementation
* **Guardrails:** Configured Gemini system instructions to refuse prompts that attempt to override the verification protocol (Prompt Injection defense).
* **Verification Logic:** Simple Python logic gates that validate spoken numbers against a mock user database before allowing the LLM to generate the next response.

## Stack
* **STT:** Deepgram
* **LLM:** Google Gemini
* **TTS:** Murf Falcon
