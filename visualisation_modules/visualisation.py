import pandas as pd
from abc import ABC, abstractmethod
from dash import html
from dash import dcc


class VisualisationModule(ABC):
    @abstractmethod
    def __init__(self, dataframe: pd.Dataframe):
        super().__init__()

    @abstractmethod
    def create_component() -> html:
        pass


class HistogramVisualisationModule(VisualisationModule):
    def __init__(self) -> None:
        super().__init__()

    def create_component() -> html:
        pass


class WordcloudVisualisationModule(VisualisationModule):
    def __init__(self) -> None:
        super().__init__()

    def create_component() -> html:
        pass

