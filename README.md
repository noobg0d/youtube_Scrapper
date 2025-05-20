
# 🎥 YouTube Scraper CLI Tool

A lightweight Python script that fetches metadata and thumbnails from YouTube videos based on a search keyword. Useful for research, dataset creation, or content analysis.

---

## 📦 Features

- 🔎 Scrapes top 50 YouTube videos for any keyword
- 📝 Saves metadata (title, channel, published date, etc.) to `metadata.csv`
- 🖼️ Downloads video thumbnails to a `thumbnails/` directory
- 💻 Command-line interface using `argparse`
- 📊 Clean output with progress bars (`tqdm`)

---

## 🚀 Getting Started

### 1. 📁 Clone the Repository

```bash
git clone https://github.com/noobg0d/youtube_Scrapper.git
cd youtube_Scrapper
````

### 2. 🐍 Set Up Your Environment

Using conda:

```bash
conda create -n yt_scraper python=3.10 -y
conda activate yt_scraper
```

Or using venv:

```bash
python -m venv yt_scraper
yt_scraper\Scripts\activate  # Windows
source yt_scraper/bin/activate  # macOS/Linux
```

### 3. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. 🔑 Add Your YouTube API Key

* Go to [Google Cloud Console](https://console.cloud.google.com/)
* Enable **YouTube Data API v3**
* Create an API key
* Open `scrape_posts.py` and replace:

```python
API_KEY = "YOUR_YOUTUBE_API_KEY"
```

---

## 🛠️ How to Use

Run the script from terminal like this:

```bash
python scrape_posts.py --platform youtube --target "<your search keyword>"
```

**Examples:**

```bash
python scrape_posts.py --platform youtube --target "chess"
python scrape_posts.py --platform youtube --target "machine learning"
```

**Outputs:**

* CSV file: `metadata.csv`
* Images: downloaded to `/thumbnails/`

---

## ⚠️ Challenges Faced & How They Were Solved

### 1. 🔐 API Key Quota & Invalid Requests

**Challenge:**
Initially, the script failed due to invalid API keys or exhausting the quota with multiple test runs.

**Solution:**

* Generated a valid key from Google Cloud Console.
* Wrapped the API call inside a `try-except` block to handle `HttpError` gracefully.
* Reduced quota usage by only requesting specific fields (`part=snippet`, etc.).

---

### 2. 🖼️ Thumbnail Download Failures

**Challenge:**
Some thumbnails failed to download due to invalid characters (e.g., `\/:*?"<>|`) in video titles used as filenames.

**Solution:**

* Used `re.sub(r'[\\/*?:"<>|]', "", filename)` to sanitize titles.
* Truncated filenames to avoid OS limits.

---

## 📁 Project Structure

```
youtube_Scrapper/
├── scrape_posts.py         # Main scraper script
├── metadata.csv            # Output file (auto-generated)
├── thumbnails/             # Downloaded thumbnails (auto-generated)
├── requirements.txt        # Package dependencies
└── README.md               # Project documentation
```

---

## 📌 Requirements

Your `requirements.txt` should include:

```
google-api-python-client
pandas
tqdm
requests
```

Install with:

```bash
pip install -r requirements.txt
```

---
