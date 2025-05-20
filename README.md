
# 🎥 YouTube Scraper CLI Tool

A lightweight Python script that fetches metadata and thumbnails from YouTube videos based on a search keyword. Useful for research, dataset creation, or content analysis.

---

## 📦 Features

- Scrapes top 50 YouTube videos for any keyword
- Saves metadata (title, channel, published date, etc.) to `metadata.csv`
- Downloads video thumbnails to a `thumbnails/` directory
- Command-line interface using `argparse`
- Clean output with progress bars (`tqdm`)

---

## 🚀 Getting Started

### 1. 📁 Clone the Repository

```bash
git clone https://github.com/noobg0d/youtube_Scrapper.git
cd youtube_Scrapper
````

### 2. 🐍 Set Up Your Environment

Create a virtual environment (recommended):

```bash
conda create -n yt_scraper python=3.10 -y
conda activate yt_scraper
```

Or use `venv`:

```bash
python -m venv yt_scraper
yt_scraper\Scripts\activate  # Windows
source yt_scraper/bin/activate  # Linux/macOS
```

### 3. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. 🔑 Add Your YouTube API Key

* Get an API key from [Google Cloud Console](https://console.cloud.google.com/).
* Enable **YouTube Data API v3**.
* Open `scrape_posts.py` and replace the `API_KEY` placeholder with your actual key:

```python
API_KEY = "YOUR_YOUTUBE_API_KEY"
```

---

## 🛠️ How to Use

Run the script via terminal:

```bash
python scrape_posts.py --platform youtube --target "<your search keyword>"
```

**Examples:**

```bash
python scrape_posts.py --platform youtube --target "chess"
python scrape_posts.py --platform youtube --target "machine learning"
```

**Output:**

* Metadata saved to `metadata.csv`
* Thumbnails downloaded to `/thumbnails/` folder

---

## ⚠️ Challenges Faced & Solutions

<details>
<summary>Click to expand</summary>

### 1. 🔐 API Key Handling & Quota Exhaustion

* Managed `HttpError` and added exception handling.
* Optimized request parameters to reduce quota usage.

### 2. 🧵 CLI Argument Handling

* Implemented `argparse` to support multiple platforms and targets.

### 3. 💾 File I/O Errors

* Encountered `PermissionError` when `metadata.csv` was already open in Excel.
* Solution: closed file manually or used timestamped filenames.

### 4. 🖼️ Thumbnail Download Failures

* Sanitized filenames to prevent OS errors.
* Truncated titles and used regex to remove forbidden characters.

### 5. 🌿 Git Issues

* Handled `src refspec main does not match any` and remote origin problems by resetting the Git branch and remote URL.

</details>

---

## 📁 Project Structure

```
youtube_Scrapper/
│
├── scrape_posts.py         # Main script
├── metadata.csv            # Output file (auto-generated)
├── requirements.txt        # Required packages
├── thumbnails/             # Downloaded thumbnails (auto-generated)
└── README.md               # This file
```

---

## 📌 Dependencies

* `google-api-python-client`
* `pandas`
* `tqdm`
* `requests`
* `argparse` (standard library)

Install all using:

```bash
pip install -r requirements.txt
```

