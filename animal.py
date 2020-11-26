from abc import ABC, abstractmethod


class Animal(ABC):

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def position(self):
        pass
