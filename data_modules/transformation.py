from abc import ABC, abstractmethod
import pandas as pd


class DataTransformer(ABC):
    @abstractmethod
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.dataframe = dataframe

    @abstractmethod
    def removeNullValues(self) -> pd.DataFrame:
        dataframe = self.dataframe
        dataframe = dataframe.dropna(how='any', axis=0)
        return dataframe

    @abstractmethod
    def removeEmojisFromText(self) -> pd.DataFrame:
        dataframe = self.dataframe
        dataframe = dataframe.astype(str).apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('ascii'))
        return dataframe

    @abstractmethod
    def noiseRemoval(dataframe:pd.DataFrame) -> pd.DataFrame:
        pass


class YoutubeDataCleaner(DataTransformer):
    def __init__(self, dataframe:pd.DataFrame) -> None:
        super().__init__(dataframe=dataframe)
        self.dataframe = dataframe

    def removeNullValues(self) -> pd.DataFrame:
        pass
    
    def removeEmojisFromText(self) -> pd.DataFrame:
        pass
    
    def noiseRemoval(self) -> pd.DataFrame:
        pass


class RedditDataCleaner(DataTransformer):
    def __init__(self, dataframe:pd.DataFrame) -> None:
        super().__init__(dataframe=dataframe)
        self.dataframe = dataframe

    def removeNullValues(self) -> pd.DataFrame:
        return super().removeNullValues()
        
    def removeEmojisFromText(self) -> pd.DataFrame:
        return super().removeEmojisFromText()
    
    def noiseRemoval(self) -> pd.DataFrame:
        return super().noiseRemoval()