from abc import ABC, abstractmethod
import pandas as pd
import re


class AbstractDataCleaner(ABC):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def clean_data(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError()

    @abstractmethod
    def remove_null_values(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError()

    @abstractmethod
    def remove_emojis_from_text(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError()

    @abstractmethod
    def replace_usernames_with_generic(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError()


class BaseDataCleaner(AbstractDataCleaner):
    def __init__(self) -> None:
        pass

    def clean_data(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = self.remove_null_values(dataframe)
        dataframe = self.remove_emojis_from_text(dataframe)
        dataframe = self.replace_usernames_with_generic(dataframe)
        return dataframe

    def remove_null_values(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = dataframe
        dataframe = dataframe.dropna(how='any', axis=0)
        return dataframe

    def remove_emojis_from_text(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe = dataframe
        dataframe = dataframe.astype(str).apply(
            lambda x: x.str.encode('ascii', 'ignore').str.decode('ascii'))
        return dataframe


class YoutubeDataCleaner(BaseDataCleaner):
    def replace_usernames_with_generic(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe['text'] = dataframe['text'].apply(
            lambda x: re.sub(r'@\w+', '@user', x))
        return dataframe


class RedditDataCleaner(BaseDataCleaner):
    def replace_usernames_with_generic(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe['text'] = dataframe['text'].apply(
            lambda x: re.sub(r'u/\w+', '@user', x))
        return dataframe
