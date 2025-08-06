from abc import ABC, abstractmethod

class LLMBase(ABC):
    @abstractmethod
    def generate_answer(self, question: str, context: str) -> str:
        pass