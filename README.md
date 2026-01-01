# Active Recall Educational Agent (Day 4)

## Overview
This agent implements a pedagogical "Active Recall" loop. Instead of simply providing answers, the agent functions as a tutor that quizzes the user, evaluates their verbal response, and provides corrective feedback. This requires complex prompt chaining and logical evaluation within the LLM.

## Workflow
1.  **Teach:** The user explains a concept to the agent.
2.  **Evaluate:** Gemini compares the user's explanation against a ground-truth definition.
3.  **Feedback:** The agent provides specific gaps in knowledge via Murf TTS.
4.  **Quiz:** The agent generates a follow-up question based on the identified gaps.

## Technical Implementation
* **Evaluation Logic:** The backend utilizes a specific "Judge" prompt structure where Gemini outputs an internal score before generating the verbal response.
* **Latency Management:** Because evaluation requires higher token counts, streaming responses were optimized to begin speaking the introductory phrase while the evaluation logic finalized.

## Stack
* **STT:** Deepgram
* **LLM:** Google Gemini (Pro Model for reasoning)
* **TTS:** Murf Falcon
