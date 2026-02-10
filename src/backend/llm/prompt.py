import re
from datetime import datetime, timezone


def get_prompt(context: str, question: str) -> str:
    prompt = f"""
                You are a research assistant that gives correct, factual answers
                using ONLY the provided context.
                Current datetime (UTC): {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}

                RULES:
                - Use ONLY the provided context.
                - Do NOT use internal knowledge.
                - Even if one word answer, explain the answer in detail.
                - Do NOT guess or infer.
                - Context is composed of multiple source snippets, and each snippet starts with a citation ID written in square brackets (e.g., [1], [2]). All text following a citation ID belongs to that source until the next citation ID appears.
                - If the answer is not explicitly in the context, say "Insufficient information to answer this question,please refer the sources."
                - Each context snippet has a citation ID in square brackets.
                - Do NOT invent citation IDs.
                - If multiple sources say the same thing, prefer the latest one.
                - If multiple facts come from the same source, reuse the same citation ID.
                - Do not explain citations.
                - Ensure every factual claim is supported by at least one citation, append the citation ID(s) in square brackets.
                - Reuse the same citation ID for multiple sentences when they rely on the same source.
                - Only introduce a new citation ID when the source changes.
                - Avoid repeating citation IDs unnecessarily. 

                Context:
                {context}

                Question:
                {question}

                Answer:
                """

    return prompt


def get_question_generator_prompt(question: str) -> str:
    prompt = f""""
        You are an AI assistant generating search queries for a retrieval system.

        Refine this prompt into 2 unique prompt to search

        Rules:
        - Do NOT answer the question.
        - Do NOT add explanations.
        - Avoid redundancy and semantic overlap.
        - Use {datetime.now().year} as the current year. Do not generate questions about current or ongoing events without explicitly mentioning the year.
        - Do NOT include quotes, numbering words, or extra text.
        - Do NOT include same question as User Question

        User Question:
        {question}

        Output format (exact):
        1. <question>
        2. <question>

        """
    return prompt
