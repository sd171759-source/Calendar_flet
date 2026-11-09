from abc import ABC, abstractmethod

class BaseEntity(ABC):
    @abstractmethod
    def __str__(self) :
        pass
    @abstractmethod
    def __eq__(self, other) :
        pass
    @abstractmethod
    def __lt__(self):
        pass
