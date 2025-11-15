# from pathlib import Path
# import yt_dlp

# class YtMp3:
#     def __init__(self, output='', ffmpeg_location=''):
#         # Options for downloading
#         self.output = output
#         self.ffmpeg_location = ffmpeg_location
#         self.ydl_opts = {
#             'format': 'bestaudio/best',  
#             'outtmpl': self.getOutput(),  
#             'postprocessors': [{           
#                 'key': 'FFmpegExtractAudio',
#                 'preferredcodec': 'mp3',
#                 'preferredquality': '192',
#             }],
#             'ffmpeg_location': ffmpeg_location,
#             'no_warnings': True,
#             'quiet': True
#         }

#     def getOutput(self):
#         output = self.output
#         if (output.endswith("/")):
#             print("output ends with /")
#             print(output)
#             return output
#         else:
#             print("output does not end with /")
#             output = output + '/'
#             print(output)
#             return output
        
#     def getOpts(self):
#         opts = {
#             'format': 'bestaudio/best',  
#             'outtmpl': self.getOutput(),  
#             'postprocessors': [{           
#                 'key': 'FFmpegExtractAudio',
#                 'preferredcodec': 'mp3',
#                 'preferredquality': '192',
#             }],
#             'ffmpeg_location': self.ffmpeg_location,
#             'no_warnings': True,
#             'quiet': True
#         }
#         return opts
        
#     def validate_ffmpeg_location(self):
#         if (self.ffmpeg_location == ""):
#             print("Error: FFmpeg location not specified.")
#             return False
        
#         if not Path(self.ffmpeg_location).exists():
#             print(f"Error: FFmpeg location '{self.ffmpeg_location}' does not exist.")
#             return False
        
#         ffmpeg = Path(self.ffmpeg_location) / "ffmpeg.exe"
#         ffprobe = Path(self.ffmpeg_location) / "ffprobe.exe"

#         if not ffmpeg.exists():
#             print(f"Error: FFmpeg executable '{ffmpeg}' does not exist.")
#             return False

#         if not ffprobe.exists():
#             print(f"Error: FFmpeg executable '{ffprobe}' does not exist.")
#             return False

#         return True

#     # Download function with file existence check
#     def downloadMP3(self, url):
#         if not self.validate_ffmpeg_location():
#             return
        
#         try:
#             # Get info dict without downloading
#             with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
#                 info = ydl.extract_info(url, download=False)
#                 title = info.get('title', 'unknown_title')
#                 output_file = (f"{self.getOutput()}{title}.mp3")
#                 print("Self.output:", self.output)
#                 print("title:", title)
#                 print("output_file:", output_file)

#             # Check if file already exists
#             if Path(output_file).exists():
#                 print(f"Skipping '{title}' — file already exists.")
#                 return { "state": 'exists', "title": title }
            
#             # Download if file does not exist
#             with yt_dlp.YoutubeDL(self.getOpts()) as ydl:
#                 ydl.download([url])
#                 print(f"Downloaded '{title}' successfully.")
#                 return { "state": 'downloaded', "title": title }
            
#         except Exception as e:
#             print(f"Error downloading '{url}': {e}")

from pathlib import Path
import yt_dlp

_dir = Path(__file__).parent

class YtMp3:
    def __init__(self, output = '', ffmpeg_location = ''):
        self.output_dir = Path(output)
        self.ffmpeg_location = Path(ffmpeg_location)  

    def validate_ffmpeg_location(self) -> bool:
        print("[YT_DLP] Validating FFmpeg location...")

        if (self.ffmpeg_location == ""):
            print("--> Error: FFmpeg location not specified.")
            return False
        
        if not Path(self.ffmpeg_location).exists():
            print(f"--> Error: FFmpeg location '{self.ffmpeg_location}' does not exist.")
            return False
        
        ffmpeg = Path(self.ffmpeg_location) / "ffmpeg.exe"
        ffprobe = Path(self.ffmpeg_location) / "ffprobe.exe"

        if not ffmpeg.exists():
            print(f"--> Error: FFmpeg executable '{ffmpeg}' does not exist.")
            return False

        if not ffprobe.exists():
            print(f"--> Error: FFmpeg executable '{ffprobe}' does not exist.")
            return False

        print("--> FFmpeg location is valid.")
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
                print(f"--> File '{file_output}' already exists.")
                return {
                    "exists": True,
                    "title": title,
                    "file_output": file_output
                }
            else:
                print(f"--> File '{file_output}' does not exist.")
                return {
                    "exists": False,
                    "title": title,
                    "file_output": file_output
                }

        except Exception as e:
            print(f"Error downloading '{url}': {e}")


    def downloadMP3(self, url):
        if not self.validate_ffmpeg_location():
            return False

        check_duplicate = self.check_duplicate(url)

        if check_duplicate["exists"]:
            print("--> Skipping download")
            return False
        elif not check_duplicate["exists"]:
            print("--> Continuing download...")
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

            print(f"[YT_DLP] Download '{title}' completed.")
            print(f"--> File saved to: {file_output}")

            return True

        except Exception as e:
            print(f"Error downloading '{url}': {e}")
        
if __name__ == "__main__":
    ytmp3 = YtMp3( 
        output = "C:/Users/user/Music",
        ffmpeg_location= Path(_dir / "ffmpeg")
    )

    ytmp3.downloadMP3("https://www.youtube.com/watch?v=jQjdEDWDeQ8")
