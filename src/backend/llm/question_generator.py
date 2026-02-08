from backend.llm.prompt import get_question_generator_prompt


class QuestionGeneratorMixin:
    def generate_questions(
        self,
        question: str,
    ) -> str:
        prompt = get_question_generator_prompt(question)
        stream = self.generate_stream(prompt)

        parts = []
        for chunk in stream:
            parts.append(chunk["message"]["content"])

        return "".join(parts)
