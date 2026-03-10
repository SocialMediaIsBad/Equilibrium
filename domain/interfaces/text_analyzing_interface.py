from abc import ABC, abstractmethod


class TextAnalyzingInterface(ABC):
    @abstractmethod
    def get_all_lines(self, text_matrix) -> list[str]:
        pass

    @abstractmethod
    def get_relevant_lines(self, all_lines: list[str]):
        pass