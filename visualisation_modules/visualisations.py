import pandas as pd
from abc import ABC, abstractmethod
from dash import html
from dash import dcc
from utility_modules.constants import APP 


class VisualisationModule(ABC):
    @abstractmethod
    def __init__(self):
    #def __init__(self, dataframe: pd.DataFrame):
        super().__init__()

    @abstractmethod
    def create_component() -> html:
        pass


class HistogramVisualisationModule(VisualisationModule):
    def __init__(self) -> None:
        super().__init__()

    def create_component() -> html:
        APP.layout = html.Div(
        children = [
            html.H1(children="test"),
            html.P(children="test paragraph")
        ]
    )


class WordcloudVisualisationModule(VisualisationModule):
    def __init__(self) -> None:
        super().__init__()

    def create_component() -> html:
        pass

