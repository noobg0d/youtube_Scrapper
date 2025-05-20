import argparse
import os
import requests
import pandas as pd
from tqdm import tqdm
from googleapiclient.discovery import build
import time

parser = argparse.ArgumentParser(description="Scrape social media posts")
parser.add_argument('--platform', type=str, required=True, help='Platform to scrape (e.g., youtube)')
parser.add_argument('--target', type=str, required=True, help='Search term or hashtag')
args = parser.parse_args()

API_KEY = "secret"  
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
THUMBNAILS_DIR = "thumbnails"

os.makedirs(THUMBNAILS_DIR, exist_ok=True)

def get_youtube_service():

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

def search_youtube(service, query, max_results=50):
  
    print(f"Searching for '{query}' on YouTube...")

    video_data = []
    next_page_token = None

    with tqdm(total=max_results, desc="Fetching videos") as pbar:
        while len(video_data) < max_results:
            try:
                request = service.search().list(
                    q=query,
                    part="snippet",
                    type="video",
                    maxResults=min(70, max_results - len(video_data)), 
                    pageToken=next_page_token
                )
                response = request.execute()
            except Exception as e:
                print(f"Error during YouTube API call: {e}. Retrying in 5 seconds...")
                time.sleep(5)
                continue  # Retry the API call

            for item in response.get("items", []):
                video_id = item["id"]["videoId"]
                snippet = item["snippet"]
                video_data.append({
                    "post_id": video_id,
                    "platform": "YouTube",
                    "post_text": snippet.get("description", ""),
                    "hashtags": [tag for tag in snippet.get("description", "").split() if tag.startswith("#")],
                    "timestamp": snippet.get("publishedAt", ""),
                    "image_url": snippet["thumbnails"]["high"]["url"],
                    "author": snippet.get("channelTitle", ""),
                    "title": snippet.get("title", ""),
                    "likes": None,      # Placeholder to be updated later
                    "comments": None    # Placeholder to be updated later
                })
                pbar.update(1)

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

    return video_data

def fetch_video_statistics(service, video_ids):
   
    stats = {}
    for i in range(0, len(video_ids), 50):
        batch_ids = video_ids[i:i+50]
        retries = 3
        while retries > 0:
            try:
                request = service.videos().list(
                    part="statistics",
                    id=",".join(batch_ids)
                )
                response = request.execute()
                for item in response.get("items", []):
                    vid = item["id"]
                    statistics = item.get("statistics", {})
                    stats[vid] = {
                        "likes": int(statistics.get("likeCount", 0)),
                        "comments": int(statistics.get("commentCount", 0))
                    }
                break  # Successful, break out of retry loop
            except Exception as e:
                retries -= 1
                print(f"Error fetching statistics: {e}. Retries left: {retries}. Waiting 5 seconds before retry...")
                time.sleep(5)
        else:
            print(f"Failed to fetch statistics for videos: {batch_ids}")

    return stats

def download_thumbnail(url, filename, max_retries=3):
   
    retries = max_retries
    while retries > 0:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            with open(filename, 'wb') as f:
                f.write(response.content)
            return True
        except Exception as e:
            retries -= 1
            print(f"Failed to download {url}: {e}. Retries left: {retries}")
            time.sleep(3)  # Wait before retrying
    return False

def save_to_csv(data, filename="metadata.csv"):
    
    # Convert list of hashtags to comma-separated string for CSV
    for item in data:
        item['hashtags'] = ','.join(item.get('hashtags', []))

    # Define the order of columns for CSV output
    columns = ['post_id', 'platform', 'post_text', 'hashtags', 'timestamp', 'image_url', 'likes', 'comments', 'author']

    # Ensure keys exist for all items
    for item in data:
        item.setdefault('likes', None)
        item.setdefault('comments', None)

    df = pd.DataFrame(data)
    df = df[columns]  # Reorder columns
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"Metadata saved to {filename}")

def main():
    if args.platform.lower() != "youtube":
        print("Currently, only YouTube platform is supported.")
        return

    service = get_youtube_service()
    results = search_youtube(service, args.target, max_results=50)

    print(f"Fetched {len(results)} videos.")

    # Fetch likes and comments statistics for all videos
    video_ids = [video['post_id'] for video in results]
    stats = fetch_video_statistics(service, video_ids)

    # Update results with likes and comments
    for video in results:
        vid = video['post_id']
        video['likes'] = stats.get(vid, {}).get('likes', 0)
        video['comments'] = stats.get(vid, {}).get('comments', 0)

    # Download thumbnails and update local file paths
    for video in tqdm(results, desc="Downloading thumbnails"):
        thumbnail_path = os.path.join(THUMBNAILS_DIR, f"{video['post_id']}.jpg")
        success = download_thumbnail(video['image_url'], thumbnail_path)
        if success:
            video['image_url'] = thumbnail_path
        else:
            video['image_url'] = ""  # Clear URL if download failed

    # Save metadata CSV
    save_to_csv(results)

if __name__ == "__main__":
    main()
