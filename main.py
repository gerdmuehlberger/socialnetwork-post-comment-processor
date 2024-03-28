import json
from pathlib import Path
from data_modules import connection
from data_modules import extraction
from data_modules import transformation
from utility_modules import utils

# add if condition to check if user has setup credentials here
secrets = json.load(open('./config/secrets.json'))

def main():

    cliArguments = utils.parseCliArguments()

    if cliArguments.client == 'reddit':
        thread_url = utils.URLParser(cliArguments.url).parseRedditUrl()
        redditClient = connection.RedditApiConnector(
                                    use_script=secrets['reddit_use_script'],
                                    client_secret=secrets['reddit_client_secret'],
                                    user_agent=secrets['reddit_user_agent'],
                                    username=secrets['reddit_username'],
                                    password=secrets['reddit_password']).connect()
        
        rawCommentsDataFrame = extraction.RedditExtractor(client=redditClient).fetchRawCommentsDataFrame(url=thread_url)

        if cliArguments.raw_data == 'true':
            return rawCommentsDataFrame
        else:
            return transformation.RedditDataCleaner(rawCommentsDataFrame)


    elif cliArguments.client == 'youtube':
        youtube_video_id = utils.URLParser(cliArguments.url).parseYoutubeUrl()
        youtubeClient = connection.YoutubeApiConnector(api_key=secrets['youtube_api_key']).connect()

        rawCommentsDataFrame = extraction.YoutubeExtractor(client=youtubeClient).fetchRawCommentsDataFrame(url=youtube_video_id)

        if cliArguments.raw_data == 'true':
            return rawCommentsDataFrame
        else:
            return transformation.YoutubeDataCleaner(rawCommentsDataFrame)
    

    else:
        print('The client you entered is not supported.')

if __name__ == "__main__":
    main()
