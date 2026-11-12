## About
This is a simple tool to export the comment sections of social network threads and posts as datasets. Simply clone the repo and run the script as stated below to retrieve the dataset in a desired format. <br><br>
**Currently supported clients:**
- Reddit
- YouTube

**Currently supported dataset formats:**
- CSV

## Setup

### 1. Install Python (macOS, via Homebrew)
```bash
brew install python@3.13
echo 'export PATH="$(brew --prefix python@3.13)/libexec/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
python --version
```

### 2. Create a virtual environment and install dependencies
Run these from the repository root:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Set up API credentials
Credentials are stored in `config/<client>_config.json`, relative to the directory you run the script from (the repo root). The `config/` directory is git-ignored.

If the config file is missing on the first run, the script will prompt you for the credentials and create it for you. To re-enter credentials, edit the file or delete it and run the script again.

**Reddit** (`config/reddit_config.json`)

Create a *script* app at https://old.reddit.com/prefs/apps/, then provide:
```json
{
  "reddit_use_script": "YOUR_CLIENT_ID",
  "reddit_client_secret": "YOUR_CLIENT_SECRET",
  "reddit_user_agent": "comment-exporter by u/yourname",
  "reddit_username": "yourname",
  "reddit_password": "yourpassword"
}
```
`reddit_use_script` is the app's client ID (the string shown under "personal use script").

**YouTube** (`config/youtube_config.json`)

Create an API key at https://console.cloud.google.com/apis/credentials in a project with the YouTube Data API v3 enabled:
```json
{
  "youtube_api_key": "YOUR_API_KEY"
}
```

## Usage
```bash
python main.py --url "<post url>" [--output <output file>]
```

| Flag | Description |
| --- | --- |
| `--url` | URL of the Reddit post or YouTube video. Reddit URLs must use `www.reddit.com`, YouTube URLs must use `www.youtube.com` (`/watch?v=...` or `/shorts/...`). Short links such as `redd.it` or `youtu.be` and other hosts such as `m.youtube.com` are not supported. |
| `--output` | Optional. Path of the file to write the dataset to. The file extension selects the format (supported: `.csv`). |

The first 10 rows of the cleaned dataset are always printed to the terminal.

For Reddit, every comment of the post is fetched, including all "load more comments" and "continue this thread" branches. Each branch costs one API request and Reddit allows roughly 100 requests per minute, so large threads can take several minutes. The number of requests made is shown while loading. Temporary Reddit errors (server errors, timeouts, rate limiting) are retried up to 5 times with increasing delays, and the fetch resumes where it stopped.

For YouTube, only the first page of top-level comments (20 by default) is fetched, without replies.

**Examples**
```bash
python main.py --url "https://www.reddit.com/r/<subreddit>/comments/<id>/<slug>/" --output reddit_comments.csv
python main.py --url "https://www.youtube.com/watch?v=<video id>" --output youtube_comments.csv
```

The resulting dataset has two columns: `upvotes` and `text` for Reddit, `like_count` and `text` for YouTube.
