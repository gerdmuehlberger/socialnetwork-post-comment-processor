from abc import ABC, abstractmethod
import pandas as pd


class DataTransformer(ABC):
    @abstractmethod
    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.dataframe = dataframe

    @abstractmethod
    def remove_null_values(self) -> pd.DataFrame:
        dataframe = self.dataframe
        dataframe = dataframe.dropna(how='any', axis=0)
        return dataframe

    @abstractmethod
    def remove_emojis_from_text(self) -> pd.DataFrame:
        dataframe = self.dataframe
        dataframe = dataframe.astype(str).apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('ascii'))
        return dataframe

    @abstractmethod
    def noise_removal(dataframe:pd.DataFrame) -> pd.DataFrame:
        pass


class YoutubeDataCleaner(DataTransformer):
    def __init__(self, dataframe:pd.DataFrame) -> None:
        super().__init__(dataframe=dataframe)
        self.dataframe = dataframe

    def remove_null_values(self) -> pd.DataFrame:
        pass
    
    def remove_emojis_from_text(self) -> pd.DataFrame:
        pass
    
    def noise_removal(self) -> pd.DataFrame:
        pass


class RedditDataCleaner(DataTransformer):
    def __init__(self, dataframe:pd.DataFrame) -> None:
        super().__init__(dataframe=dataframe)
        self.dataframe = dataframe

    def remove_null_values(self) -> pd.DataFrame:
        return super().remove_null_values()
        
    def remove_emojis_from_text(self) -> pd.DataFrame:
        return super().remove_emojis_from_text()
    
    def noise_removal(self) -> pd.DataFrame:
        return super().noise_removal()