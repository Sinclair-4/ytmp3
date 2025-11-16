from pathlib import Path
import yt_dlp

_dir = Path(__file__).parent

class YtMp3:
    def __init__(self, output = '', ffmpeg_location = ''):
        self.output_dir = Path(output)
        self.ffmpeg_location = Path(ffmpeg_location)  

    def printErr(self, message):
        print(f"\033[91m{message}\033[0m")

    def printSuccess(self, message):
        print(f"\033[92m{message}\033[0m")

    def validate_ffmpeg_location(self) -> bool:
        print("[YT_DLP] Validating FFmpeg location...")

        if (self.ffmpeg_location == ""):
            # print("-> Error: FFmpeg location not specified.")
            self.printErr("-> Error: FFmpeg location not specified.")
            return False
        
        if not Path(self.ffmpeg_location).exists():
            # print(f"-> Error: FFmpeg location '{self.ffmpeg_location}' does not exist.")
            self.printErr(f"-> Error: FFmpeg location '{self.ffmpeg_location}' does not exist.")
            return False
        
        ffmpeg = Path(self.ffmpeg_location) / "ffmpeg.exe"
        ffprobe = Path(self.ffmpeg_location) / "ffprobe.exe"

        if not ffmpeg.exists():
            # print(f"-> Error: FFmpeg executable '{ffmpeg}' does not exist.")
            self.printErr(f"-> Error: FFmpeg executable '{ffmpeg}' does not exist.")
            return False

        if not ffprobe.exists():
            # print(f"-> Error: FFmpeg executable '{ffprobe}' does not exist.")
            self.printErr(f"-> Error: FFmpeg executable '{ffprobe}' does not exist.")
            return False

        # print("-> FFmpeg location is valid.")
        self.printSuccess("-> FFmpeg location is valid.")
        return True
    

    def check_duplicate(self, url):
        print("[YT_DLP] Checking for duplicates...")
        # Check for duplicate
        try:
            ytdlp = yt_dlp.YoutubeDL({
                'quiet': True, 
                'no_warnings': True
            })

            with ytdlp as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'unknown_title')

            file_output = Path(self.output_dir) / f"{title}.mp3"

            if file_output.exists():
                # print(f"-> File '{file_output}' already exists.")
                self.printErr(f"-> File '{file_output}' already exists.")
                return {
                    "exists": True,
                    "title": title,
                    "file_output": file_output
                }
            else:
                # print(f"-> File '{file_output}' does not exist.")
                self.printSuccess(f"-> File '{file_output}' does not exist.")
                return {
                    "exists": False,
                    "title": title,
                    "file_output": file_output
                }

        except Exception as e:
            # print(f"Error downloading '{url}': {e}")
            self.printErr(f"Error downloading '{url}': {e}")


    def downloadMP3(self, url):
        if not self.validate_ffmpeg_location():
            return False

        check_duplicate = self.check_duplicate(url)

        if check_duplicate["exists"]:
            # print("-> Skipping download")
            self.printErr("-> Skipping download")
            return False
        elif not check_duplicate["exists"]:
            # print("-> Continuing download...")
            self.printSuccess("-> Continuing download...")
            title = check_duplicate["title"]
            file_output = check_duplicate["file_output"]
        
        try:
            opts = {
                'format': 'bestaudio/best',
                'outtmpl': f"{self.output_dir}/{title}",
                'ffmpeg_location': self.ffmpeg_location,
                'no_warnings': True,
                'quiet': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }]
            }

            with yt_dlp.YoutubeDL(opts) as ydl:
                print("[YT_DLP] Started downloading MP3...")
                ydl.download([url])

            print("--------------------------------------------")
            # print(f"[YT_DLP] Download '{title}' completed.")
            self.printSuccess(f"[YT_DLP] Download '{title}' completed.")
            # print(f"-> File saved to: {file_output}")
            self.printSuccess(f"-> File saved to: {file_output}")

            return True

        except Exception as e:
            # print(f"Error downloading '{url}': {e}")
            self.printErr(f"Error downloading '{url}': {e}")
        
if __name__ == "__main__":
    ytmp3 = YtMp3( 
        output = "C:/Users/user/Music",
        ffmpeg_location= Path(_dir / "ffmpeg")
    )

    ytmp3.downloadMP3("https://www.youtube.com/watch?v=jQjdEDWDeQ8")