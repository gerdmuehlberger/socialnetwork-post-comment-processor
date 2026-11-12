from abc import ABC, abstractmethod
import pandas as pd


class DataExporter(ABC):
    @abstractmethod
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def export(self, dataframe: pd.DataFrame, path: str) -> None:
        pass


class CsvExporter(DataExporter):
    def __init__(self) -> None:
        super().__init__()

    def export(self, dataframe: pd.DataFrame, path: str) -> None:
        dataframe.to_csv(path, index=False)
