import os
import argparse
from tqdm import tqdm
import subprocess
from datetime import datetime, timedelta

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

def parse_date_string(date_str):
    """Parse date string in YYYYMMDD format and return datetime object."""
    try:
        return datetime.strptime(date_str, '%Y%m%d')
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Expected format: YYYYMMDD")

def generate_date_range(start_date, end_date):
    """Generate a list of dates between start_date and end_date (inclusive)."""
    start_dt = parse_date_string(start_date)
    end_dt = parse_date_string(end_date)
    
    if start_dt > end_dt:
        raise ValueError("Start date must be before or equal to end date")
    
    dates = []
    current_date = start_dt
    while current_date <= end_dt:
        dates.append(current_date.strftime('%Y%m%d'))
        current_date += timedelta(days=1)
    
    return dates

def parse_multiple_dates(date_input):
    """Parse multiple date formats and return a list of dates."""
    dates = []
    
    # Split by commas to handle multiple date specifications
    date_specs = [spec.strip() for spec in date_input.split(',')]
    
    for spec in date_specs:
        if '-' in spec:
            # Date range format: YYYYMMDD-YYYYMMDD
            try:
                start_date, end_date = spec.split('-')
                range_dates = generate_date_range(start_date.strip(), end_date.strip())
                dates.extend(range_dates)
            except ValueError as e:
                print(f"Error parsing date range '{spec}': {e}")
                continue
        else:
            # Single date format: YYYYMMDD
            try:
                parse_date_string(spec)  # Validate the date
                dates.append(spec)
            except ValueError as e:
                print(f"Error parsing date '{spec}': {e}")
                continue
    
    # Remove duplicates and sort
    return sorted(list(set(dates)))

def merge_videos_by_date(date, base_path, output_path):
    """Merge videos for a specific date."""
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

def merge_videos_by_multiple_dates(dates_input, base_path, output_path):
    """Merge videos from multiple dates into single files."""
    dates = parse_multiple_dates(dates_input)
    
    if not dates:
        print("No valid dates found to process.")
        return
    
    print(f"Processing {len(dates)} dates: {', '.join(dates)}")
    
    # Define paths for front and back folders
    front_folder = os.path.join(base_path, 'Normal', 'Front')
    back_folder = os.path.join(base_path, 'Normal', 'Back')
    
    # Collect all videos from all specified dates
    all_front_videos = []
    all_back_videos = []
    
    for date in dates:
        # Get videos for this specific date
        front_videos = [os.path.join(front_folder, f) for f in os.listdir(front_folder) 
                       if f.startswith(f'NO{date}') and f.endswith('F.MP4')]
        back_videos = [os.path.join(back_folder, f) for f in os.listdir(back_folder) 
                      if f.startswith(f'NO{date}') and f.endswith('B.MP4')]
        
        all_front_videos.extend(front_videos)
        all_back_videos.extend(back_videos)
    
    # Sort all videos to ensure chronological order
    all_front_videos.sort()
    all_back_videos.sort()
    
    # Create output filenames based on date range
    if len(dates) == 1:
        date_suffix = dates[0]
    else:
        date_suffix = f"{dates[0]}-{dates[-1]}"
    
    # Merge all front videos into one file
    if all_front_videos:
        front_output_file = os.path.join(output_path, f'Merged_Front_{date_suffix}.mp4')
        print(f"Merging {len(all_front_videos)} front videos from {len(dates)} dates...")
        merge_videos_ffmpeg(all_front_videos, front_output_file)
        print(f"All front videos merged into {front_output_file}")
    else:
        print(f"No front videos found for the specified dates")
    
    # Merge all back videos into one file
    if all_back_videos:
        back_output_file = os.path.join(output_path, f'Merged_Back_{date_suffix}.mp4')
        print(f"Merging {len(all_back_videos)} back videos from {len(dates)} dates...")
        merge_videos_ffmpeg(all_back_videos, back_output_file)
        print(f"All back videos merged into {back_output_file}")
    else:
        print(f"No back videos found for the specified dates")

def merge_all_dates(base_path, output_path):
    """Merge videos for all available dates."""
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
    parser = argparse.ArgumentParser(
        description="Merge dashcam videos by date.",
        epilog="""
Date format examples:
  Single date: 20240829
  Multiple dates: 20240829,20240830,20240831
  Date range: 20240829-20240831
  Mixed: 20240825,20240829-20240831,20240905
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("base_path", nargs='?', default=os.getcwd(), 
                       help="Base path to the video directories (default: current directory)")
    parser.add_argument("--date", 
                       help="Date(s) for merging videos. Supports single dates (YYYYMMDD), "
                            "multiple dates (comma-separated), and date ranges (YYYYMMDD-YYYYMMDD)")
    parser.add_argument("--output_path", 
                       help="Path where the merged video files will be saved")

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    if args.output_path and not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    if args.date:
        merge_videos_by_multiple_dates(args.date, args.base_path, args.output_path)
    else:
        merge_all_dates(args.base_path, args.output_path)