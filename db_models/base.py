from abc import ABC, abstractmethod

class Base(ABC):
    @abstractmethod
    def insert_to_db(self, cur):
        pass #pragma: no cover

    @abstractmethod
    def serialize(self):
        return {} #pragma: no cover

    @staticmethod
    @abstractmethod
    def create_table(cur):
        pass #pragma: no cover
