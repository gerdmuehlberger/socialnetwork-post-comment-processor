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

If the config file is missing on the first run, the script will prompt you for the credentials and create it for you.

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

Create an API key at https://console.cloud.google.com/apis/dashboard with the YouTube Data API v3 enabled:
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
| `--url` | URL of the Reddit post or YouTube video. Reddit URLs must use `www.reddit.com`. |
| `--output` | Optional. Path of the file to write the dataset to. The file extension selects the format (supported: `.csv`). |

The first 10 rows of the cleaned dataset are always printed to the terminal.

**Examples**
```bash
python main.py --url "https://www.reddit.com/r/<subreddit>/comments/<id>/<slug>/" --output reddit_comments.csv
python main.py --url "https://www.youtube.com/watch?v=<video id>" --output youtube_comments.csv
```

The resulting dataset has two columns: `upvotes` and `text` for Reddit, `like_count` and `text` for YouTube.

## Testing
There is no automated test suite yet. Run these checks manually from the repo root with the virtual environment activated (`source .venv/bin/activate`).

**Export to a file** (requires valid credentials)
```bash
python main.py --url "https://www.reddit.com/r/<subreddit>/comments/<id>/<slug>/" --output test.csv
head test.csv
```
The preview is printed, followed by `Wrote N comments to test.csv`. The CSV header should be `upvotes,text`. Use a small thread, since all "load more" comments are fetched.

**Unsupported format**
```bash
python main.py --url "https://www.reddit.com/r/<subreddit>/comments/<id>/<slug>/" --output test.xlsx
```
The script exits immediately with `Unsupported output format 'xlsx'. Supported formats: csv`, before any comments are fetched.

**Without `--output`**

Only the preview is printed and no file is written.

**Exporter only** (offline, no credentials needed)
```bash
python - <<'EOF'
import sys
sys.argv = ["x", "--url", "https://www.reddit.com/r/a/comments/b/c/"]  # factories parses CLI args on import
import pandas as pd
from utility_modules import factories
factories.get_exporter("offline.csv").export(pd.DataFrame({"upvotes": [1, 2], "text": ["hi", "a, \"quoted\" comment"]}), "offline.csv")
print(open("offline.csv").read())
EOF
```
The output should be a valid CSV with the comma and quotes in the second comment escaped.

Remove the test files afterwards with `rm test.csv offline.csv`.

## Adding an output format
Exporters follow the same factory pattern as the API clients:
1. Add a subclass of `DataExporter` in `data_modules/export.py` that implements `export(dataframe, path)`.
2. Register it under its file extension in `get_exporter` in `utility_modules/factories.py`, e.g. `"json": export.JsonExporter()`.
