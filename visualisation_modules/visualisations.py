import pandas as pd
from abc import ABC, abstractmethod
from dash import html
from dash import dcc
from utility_modules.constants import APP 


class VisualisationModule(ABC):
    @abstractmethod
    def __init__(self, dataframe: pd.DataFrame) -> None:
        super().__init__()

    @abstractmethod
    def create_component() -> html:
        pass


class BarChartVisualisationModule(VisualisationModule):
    def __init__(self) -> None:
        super().__init__()

    def create_component(dataframe: pd.DataFrame, x_axis: pd.Series, y_axis: pd.Series) -> html:
        APP.layout = html.Div(
        children = [
            dcc.Graph(
                figure={"data":[
                    {
                        "x": x_axis,
                        "y": y_axis,
                        "type": "bar"
                    }
                ]}
            )
        ]
        )


class WordcloudVisualisationModule(VisualisationModule):
    def __init__(self) -> None:
        super().__init__()

    def create_component() -> html:
        pass

