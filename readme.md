<!-- PROJECT LOGO -->
<br />
<h1 align="center">Video Merger</h1>
<p align="center">
  A Python script for merging dashcam videos by date using FFmpeg.
  <br />
  <a href="https://github.com/your_username/your_repo_name"><strong>Explore the docs »</strong></a>
  <br />
  <br />
  <a href="#usage">View Demo</a>
  ·
  <a href="#contributing">Report Bug</a>
  ·
  <a href="#contact">Request Feature</a>
</p>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project provides a Python script to merge dashcam video files recorded on different dates into single video files for each date. The script uses FFmpeg to handle video merging efficiently.

### Why This Project?

* Automate the merging of dashcam videos, saving time and effort.
* Ensure videos are combined in the correct order based on date.
* Simplify the process of organizing and managing large quantities of video files.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python.org]][Python-url]
* [![FFmpeg][FFmpeg.org]][FFmpeg-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Follow these instructions to set up and use the script on your local machine.

### Prerequisites

Ensure you have Python and FFmpeg installed. You can download FFmpeg from [FFmpeg.org](https://ffmpeg.org/download.html).

* Python 3.x
* FFmpeg

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/your_username/your_repo_name.git

2. Navigate into the directory
   ```sh
   cd your_repo_name

3. No additional Python packages are required beyond the standard library.
<p align="right">(<a href="#readme-top">back to top</a>)</p> 

<!-- USAGE EXAMPLES -->
### Usage

<p align="right">(<a href="#readme-top">back to top</a>)</p>

1. Use the following command to merge videos by date:
    ```sh 
    python merge_videos.py --date YYYYMMDD --output_path /path/to/output

2. Replace YYYYMMDD with the desired date and /path/to/output with the path where you want the merged videos to be saved. For example, to merge videos for August 29, 2024, and save them to /videos/merged, use:
    ```sh
    python merge_videos.py --date 20240829 --output_path /videos/merged

3. To merge videos for all available dates, omit the --date argument:
    ```sh
    python merge_videos.py --output_path /videos/merged

<p align="right">(<a href="#readme-top">back to top</a>)</p> 

## Roadmap

- [x] Basic video merging functionality
- [x] Support for merging videos by date
- [ ] Add support for different video formats
- [ ] Improve error handling
- [ ] Add more usage examples

