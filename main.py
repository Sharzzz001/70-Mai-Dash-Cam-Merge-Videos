import os
import argparse
from tqdm import tqdm
import subprocess

def merge_videos_ffmpeg(video_files, output_file):
    """Merge all video files using ffmpeg with the demux concat method."""
    # Create a temporary file to list all video files
    with open('filelist.txt', 'w') as filelist:
        for video in video_files:
            filelist.write(f"file '{video}'\n")
    
    # Use ffmpeg to concatenate the video files
    command = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "filelist.txt", "-c", "copy", output_file]
    subprocess.run(command, check=True)

    # Remove the temporary file
    os.remove('filelist.txt')

def merge_videos_by_date(date, base_path, output_path):
    # Define paths for front and back folders
    front_folder = os.path.join(base_path, 'Normal', 'Front')
    back_folder = os.path.join(base_path, 'Normal', 'Back')

    # Get only videos for the specified date
    front_videos = [os.path.join(front_folder, f) for f in os.listdir(front_folder) if f.startswith(f'NO{date}') and f.endswith('F.MP4')]
    back_videos = [os.path.join(back_folder, f) for f in os.listdir(back_folder) if f.startswith(f'NO{date}') and f.endswith('B.MP4')]

    # Sort videos to ensure they are merged in order
    front_videos.sort()
    back_videos.sort()

    # Merge videos for the front camera
    if front_videos:
        front_output_file = os.path.join(output_path, f'Merged_Front_{date}.mp4')
        print(f"Merging front videos for date {date}...")
        merge_videos_ffmpeg(front_videos, front_output_file)
        print(f"Front videos merged into {front_output_file}")
    else:
        print(f"No front videos found for date {date}")

    # Merge videos for the back camera
    if back_videos:
        back_output_file = os.path.join(output_path, f'Merged_Back_{date}.mp4')
        print(f"Merging back videos for date {date}...")
        merge_videos_ffmpeg(back_videos, back_output_file)
        print(f"Back videos merged into {back_output_file}")
    else:
        print(f"No back videos found for date {date}")

def merge_all_dates(base_path, output_path):
    # Define paths for front and back folders
    front_folder = os.path.join(base_path, 'Normal', 'Front')
    back_folder = os.path.join(base_path, 'Normal', 'Back')

    # Get all unique dates from the filenames
    front_dates = set(f[2:10] for f in os.listdir(front_folder) if f.endswith('F.MP4'))
    back_dates = set(f[2:10] for f in os.listdir(back_folder) if f.endswith('B.MP4'))
    
    # Get the union of all dates present in either folder
    all_dates = sorted(front_dates.union(back_dates))

    # Merge videos for each date
    for date in tqdm(all_dates, desc="Processing dates"):
        merge_videos_by_date(date, base_path, output_path)

if __name__ == "__main__":
    # Argument parsing for path, date, and output path
    parser = argparse.ArgumentParser(description="Merge dashcam videos by date.")
    parser.add_argument("base_path", nargs='?', default=os.getcwd(), help="Base path to the video directories (default: current directory)")
    parser.add_argument("--date", help="Date for which you want to merge videos in format YYYYMMDD (e.g., 20240829)")
    parser.add_argument("--output_path", help="Path where the merged video files will be saved")

    args = parser.parse_args()

    if args.date:
        merge_videos_by_date(args.date, args.base_path, args.output_path)
    else:
        merge_all_dates(args.base_path, args.output_path)
