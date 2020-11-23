from abc import ABC, abstractmethod

class Base(ABC):
    @abstractmethod
    def insert_to_db(self, cur):
        pass

    @abstractmethod
    def serialize(self):
        return {}

    @staticmethod
    @abstractmethod
    def create_table(cur):
        pass
