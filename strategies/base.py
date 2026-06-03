from abc import ABC, abstractmethod

class Strategy(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def generate_signals(self, data):
        pass



