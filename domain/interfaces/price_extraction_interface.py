from abc import ABC, abstractmethod
from typing import Optional

class PriceExtractionInterface(ABC):
    @abstractmethod
    def coordinate_price_search(self, photo: bytearray) -> Optional[float]:
        pass