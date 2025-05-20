
📺 YouTube Scraper

A flexible, command-line-based YouTube metadata and thumbnail scraper using the YouTube Data API v3. Built for developers, researchers, and content analysts who want structured access to channel or video metadata without using a browser.


## 🚀 Features

- 🔍 Scrapes metadata like title, description, channel name, views, publish date, etc.
- 🖼️ Downloads thumbnails with clean, valid filenames
- 📦 Saves results in CSV format for further analysis
- ⚙️ CLI support with `argparse` to select platform (currently supports YouTube only)
- ⏱️ Progress bars and informative logs for better UX
- 🔐 API key-based access using YouTube Data API v3

---

## 🧰 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/noobg0d/youtube_Scrapper.git
   cd youtube_Scrapper
````

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Add your YouTube API key to the script or `.env` file:

   ```env
   YOUTUBE_API_KEY=your_api_key_here
   ```

---

## 📦 Usage

```bash
python scraper.py --platform youtube --target https://www.youtube.com/@channel_name
```

Arguments:

* `--platform`: Platform name (currently only `youtube` supported)
* `--target`: Channel URL or video URL

---

## 📁 Output

* `metadata.csv`: Contains scraped video metadata
* `thumbnails/`: Folder with downloaded thumbnail images
* Timestamped filenames prevent accidental overwrites

---

## ⚠️ Challenges Faced & Solutions

### 1. 🔐 API Key Handling & Quota Exhaustion

**Challenge**: The API key often became invalid or exceeded quota during testing.

**Solution**:

* Used valid **YouTube Data API v3** keys from Google Cloud Console
* Added structured error handling using `try-except` for `HttpError`
* Limited API usage by specifying only required fields (`part` and `fields`)

---

### 2. 🧵 Command-Line Integration with `argparse`

**Challenge**: Needed CLI-based flexibility for different platforms.

**Solution**:

* Used Python’s `argparse` to parse `--platform` and `--target` arguments
* Handled incorrect/missing arguments with helpful error messages
* Set foundation for future multi-platform scraping

---

### 3. 💾 Permission Denied While Writing Output

**Challenge**: Faced `PermissionError: [Errno 13]` due to open `metadata.csv` file.

**Solution**:

* Added `try-except` blocks around file I/O
* Included user warnings for open files
* Used timestamp-based naming (`metadata_YYYYMMDD.csv`) to avoid overwrites

---

### 4. 🖼️ Downloading and Naming Thumbnails Reliably

**Challenge**: Thumbnail downloads failed due to invalid or excessively long filenames from video titles.

**Solution**:

* Used `re.sub()` to sanitize file names (`\ / : * ? " < > |` removed)
* Truncated names to 100 characters
* Used `tqdm` for thumbnail download progress bars

---

### 5. 🌿 Git/GitHub Integration Issues

**Challenge**: Encountered common Git issues like `src refspec main does not match any` and push failures.

**Solution**:

```bash
git branch -M main
git remote remove origin
git remote add origin https://github.com/noobg0d/youtube_Scrapper.git
git push -u origin main
```

---

## 🧱 Project Structure

```
youtube_Scrapper/
├── thumbnails/           # Downloaded thumbnail images
├── metadata.csv          # Scraped video metadata
├── scraper.py            # Main script
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## 📜 License

This project is licensed under the MIT License. See `LICENSE` for more details.

---


