from abc import ABC, abstractmethod


class RunInterface(ABC):
    @abstractmethod
    def __init__(self, performance_test: bool):
        pass

    @abstractmethod
    def run(self):
        pass
