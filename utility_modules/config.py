from abc import ABC, abstractmethod
import json


class CredentialsConfigurator(ABC):
    def __init__(self) -> None:
        self.config_json = {}

    @abstractmethod
    def set_credentials(self) -> None:
        pass


class RedditCredentialConfigurator(CredentialsConfigurator):
    def __init__(self) -> None:
        super().__init__()

    def set_credentials(self) -> None:
        credentials = {}
        print(
            "You can set up your credentials here: https://old.reddit.com/prefs/apps/\nFor help, please refer to: https://praw.readthedocs.io/en/latest/getting_started/quick_start.html#\n"
        )
        print("Enter reddit use script:")
        use_script = input()
        credentials["reddit_use_script"] = use_script

        print("Enter reddit client secret:")
        client_secret = input()
        credentials["reddit_client_secret"] = client_secret

        print("Enter reddit user agent:")
        user_agent = input()
        credentials["reddit_user_agent"] = user_agent

        print("Enter reddit username:")
        username = input()
        credentials["reddit_username"] = username

        print("Enter reddit password:")
        password = input()
        credentials["reddit_password"] = password

        with open("./config/reddit_config.json", "w") as config_file:
            json.dump(credentials, config_file)


class YoutubeCredentialConfigurator(CredentialsConfigurator):
    def __init__(self) -> None:
        super().__init__()

    def set_credentials(self) -> None:
        credentials = {}
        print(
            "You can set up your YouTube API Key here: https://console.cloud.google.com/apis/dashboard\nFor help, please refer to: https://developers.google.com/youtube/v3/docs\n"
        )
        print("Enter youtube API key:")
        api_key = input()
        credentials["youtube_api_key"] = api_key

        with open("./config/youtube_config.json", "w") as config_file:
            json.dump(credentials, config_file)