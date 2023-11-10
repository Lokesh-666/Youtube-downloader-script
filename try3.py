from pytube import Playlist, YouTube
from tqdm import tqdm
import time
import keyboard
import sys

# Function to check if "Q" has been pressed
def check_exit_signal():
    if keyboard.is_pressed('q'):
        print("Exit signal detected. Exiting...")
        sys.exit()

# Prompt the user to enter the YouTube playlist link
playlist_url = input("Enter the YouTube playlist URL: ")

# Create a Playlist object
playlist = Playlist(playlist_url)

# Define the maximum number of retries and delay between retries
max_retries = 3
retry_delay = 5  # 5 seconds

# Chunk size for frequent updates (adjust as needed)
chunk_size = 1024

# Initialize a counter to keep track of successfully downloaded videos
success_count = 0

# Iterate through the videos in the playlist and download them with retries
total_videos = len(playlist.video_urls)
for video_number, video_url in enumerate(playlist.video_urls, start=1):
    video_title = None  # Initialize video title
    retries = max_retries
    while retries > 0:
        try:
            check_exit_signal()  # Check for the exit signal
            yt = YouTube(video_url)
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            video_title = yt.title  # Get the title of the downloaded video
            # Append the desired file extension to the filename
            video_filename = f'{video_title}.mp4'
            print(f"Downloading video {video_number}/{total_videos}: {video_title}")
            total_bytes = stream.filesize
            with tqdm(total=total_bytes, unit='B', unit_scale=True, unit_divisor=1024) as bar:
                stream.download(output_path='your_download_path', filename=video_filename)
                bar.update(total_bytes)  # Update the progress bar to 100%
            print(f"Downloaded video {video_number}/{total_videos}: {video_title}")
            success_count += 1  # Increment the success count
            break  # Successful download, exit the retry loop
        except Exception as e:
            check_exit_signal()  # Check for the exit signal
            print(f"Download failed for {video_title}: {str(e)}")
            if retries > 1:
                print(f"Retrying (Attempt {max_retries - retries + 1}/{max_retries})...")  # Indicate the retry attempt
            retries -= 1
            time.sleep(retry_delay)
    
    if retries == 0:
        print(f"Max retries reached for {video_title}. Skipping this video.")

# Display the congratulatory message with the total number of videos successfully downloaded
print(f"Congratulations! {success_count} out of {total_videos} videos were successfully downloaded.")
