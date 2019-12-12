from abc import ABC, abstractmethod

class DataHandler(ABC):
    def __init__(self, next_handler):
        self.set_handler(next_handler)
    
    def get_handler(self):
        return self.next_handler

    @abstractmethod
    def process_entry(self, entry):
        pass

    def set_handler(self, next_handler):
        self.next_handler = next_handler