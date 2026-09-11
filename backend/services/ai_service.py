from ollama import chat


def enhance_text(text: str, action: str) -> str:

    prompts = {
        "improve": """
Improve the following text while keeping its original meaning.
Make it clearer, more natural, and grammatically correct.
Return only the improved text.
Do not add explanations.
""",

        "grammar": """
Correct the grammar, spelling, punctuation, and sentence structure
of the following text.
Return only the corrected text.
Do not add explanations.
""",

        "professional": """
Rewrite the following text in a professional and polished tone.
Keep the original meaning.
Return only the rewritten text.
Do not add explanations.
""",

        "conversational": """
Rewrite the following text so it sounds natural, friendly,
and conversational.
Keep the original meaning.
Return only the rewritten text.
Do not add explanations.
""",

        "summarize": """
Summarize the following text while preserving the most important
information.
Return only the summary.
Do not add explanations.
"""
    }

    if action not in prompts:
        raise ValueError("Invalid AI enhancement action.")

    try:
        response = chat(
            model="llama3.2",
            messages=[
                {
                    "role": "system",
                    "content": prompts[action]
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        return response.message.content.strip()

    except Exception as error:
        print("Ollama error:", error)
        raise RuntimeError(
            "Ollama is not running or the llama3.2 model is unavailable."
        )