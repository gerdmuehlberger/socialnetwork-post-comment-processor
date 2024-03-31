from abc import ABC, abstractmethod
import sys


class CredentialsConfigurator(ABC):
    @abstractmethod
    def create_credentials():
        pass

