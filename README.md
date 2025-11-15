# YTMP3

A simple python script that allows you to download yt links as mp3 file

## Url format

Good:

```
https://www.youtube.com/watch?v=j_sG_Juncn8
```

Bad:

```
https://www.youtube.com/watch?v=j_sG_Juncn8&list=RDh2B5F8skpGE&index=9
```

## Setup Instructions

Follow these steps to get the project running on your machine.

### 1. Clone the repository
```bash
git clone https://github.com/Sinclair-4/ytmp3
cd ytmp3
```

### 2. Create a virtual environment
```bash
python -m venv venv
```

### 3. Activate the virtual environment
```bash
venv\Scripts\activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the project
```bash
python main.py
```

### Or just download the setup script
Download the setup script below and run it in the folder where you want the project created: 
[setup.bat](./setup.bat)

### Add to System PATH

Add this folder to your system `PATH` environment variable so you can call the script from anywhere using:
```bash
ytmp3
```

## Acknowledgements

This project uses:  
1. [yt-dlp](https://github.com/yt-dlp/yt-dlp) (Unlicense) – for downloading media. See [yt-dlp docs](https://github.com/yt-dlp/yt-dlp#readme) for more info.  
2. [FFmpeg](https://www.ffmpeg.org) (LGPL/GPL) – for audio and video processing. See [FFmpeg documentation](https://ffmpeg.org/documentation.html).  

Special thanks to the open-source communities behind these tools for their amazing work.
