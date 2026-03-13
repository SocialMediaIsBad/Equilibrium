from abc import ABC, abstractmethod

class BalanceCalculationInterface(ABC):
    @abstractmethod
    def calculate_balances(self) -> list:
        pass

    @abstractmethod
    def calculate_deposits(self) -> list:
        pass