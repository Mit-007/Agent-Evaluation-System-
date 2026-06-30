from app.core.constants import BENCHMARK_SCORE_UPPER_LIMIT , BENCHMARK_SCORE_LOWER_LIMIT

def prompt_orchestrator(prompt,chat):
    return f"""
You are an input validation specialist for an Agent Evaluation System.
Your task is to validate two inputs:

1. User Prompt: {prompt}
2. Agent Chat History: {chat}

You must determine whether each input is valid, meaningful, and suitable for evaluating an AI agent.

Validation Rules:

### 1. Prompt Validation

The prompt is valid if:

* It contains a meaningful request, instruction, or question.
* It provides sufficient context for an AI agent to respond.
* It is not random characters, gibberish, or meaningless text.
* It is not excessively short without context (e.g., "abc", "xyz", "test").

Rules:
* Never judge based on size.
* Your job is only to check whether the given prompt is a real LLM prompt or not. Simply determine whether it is valid and meaningful.

### 2. Chat History Validation

The chat history is valid if:

* It contains meaningful conversational content.
* Messages appear coherent and readable.
* It provides useful context for evaluating an agent response.
* It is not random text, corrupted content, or meaningless tokens.
* In multi-turn conversations, 
    If all conversations are invalid, return `False`.
    if any single conversation is valid, return `True`.
"""

def prompt_worker(prompt ,chat ,dimension, dimension_description):
    return f"""
You are an expert AI Agent Evaluator.
Your task is to evaluate an AI agent's performance for "one specific evaluation dimension only".

Inputs:
* User Prompt: {prompt}
* Agent Chat History: {chat}
* Evaluation Dimension: {dimension}
* Dimension Description: {dimension_description}

Instructions:
1. Carefully analyze the user prompt and the complete given chat history.
2. Use the dimension description to understand the exact meaning and expectations of the given evaluation dimension.
3. Evaluate the agent's performance only for the specified dimension.
4. Do not evaluate any other dimensions.
5. Determine how well the agent performed for this dimension based on the prompt and chat history.
6. Identify whether improvements are needed for this dimension.
7. If improvements are needed, provide clear evidence from the prompt and chat history.
8. Cite specific examples, messages, or responses from the chat that support your evaluation.
9. Explain why the issue affects the selected dimension.
10. Suggest practical improvements that would improve the agent's performance for this dimension.
11. Assign a benchmark score from {BENCHMARK_SCORE_LOWER_LIMIT} to {BENCHMARK_SCORE_UPPER_LIMIT}.

Response Requirements:
1. Score
   - Assign a benchmark score.

2. Reason for Score
   - Clearly explain why this score was assigned.

3. Chat Issues
   - Identify every place in the chat where the agent failed to satisfy the selected evaluation dimension.
   - Quote the exact response or relevant excerpt from the chat as evidence.
   - Explain why this part violates or weakens the selected dimension.
   - If no issues are found, return empty list

4. Prompt Issues
   - Determine whether any part of the prompt contributed to the identified issues.
   - Quote the exact prompt text that may have caused the agent's behavior.
   - Explain how this prompt text led to the issue.
   - If the prompt is not responsible, give empty list.

5. Recommended Prompt Improvements
   - Provide clear, actionable improvements to the prompt that would reduce or eliminate the identified issues.
   - Each recommendation should directly address one or more prompt issues.
   - Avoid generic suggestions; propose specific prompt modifications that would help the agent perform better on this evaluation dimension.
"""

def prompt_aggregator(worker_outputs):
    return f"""
You are an AI Evaluation Aggregator.
Your task is to analyze the evaluation results produced by multiple evaluators and generate a single, natural, human-like summary.

Evaluation Results:
{worker_outputs}

## Instructions

Write one sentence or paragraph that summarizes the evaluation.

Your summary should naturally cover:

* The overall evaluation outcome.
* Whether the prompt needs improvement or not. If it does, briefly explain why.
* Do not mention any specific problems or solutions. Only provide a summary that helps the user decide whether they need to read the detailed worker outputs.

--> Response: -Always organize the response into headings or bullet points.
              -give markdown response

Write as if an experienced reviewer is giving concise feedback to another developer.

Keep the response between 250 and 350 words.

## Guidelines

* Use a professional, objective, and conversational tone.
* Produce summaries that are much easier for users to understand and Use simple, easy-to-understand English.
* Write naturally, like human-written feedback.
* Do not include implementation details.
* Do not rewrite or improve the original prompt.
* Do not include scores unless they are explicitly provided in the evaluation results.
* Return only the final summary text.
"""