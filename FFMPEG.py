import zipfile as zip
import requests
import shutil
import os 

class FFMPEG:
    def __init__(self):
        self.url = 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip'
        self._dir = os.path.dirname(__file__)

        self.folder = f"{self._dir}/ffmpeg"
        self.zip = 'ffmpeg.zip'
        self.ffmpeg = 'ffmpeg.exe'
        self.ffprobe = 'ffprobe.exe'

    def init_folder(self):
        # Check if folder exists
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

    def download_zip(self):
        # Check if zip is already downloaded
        if os.path.exists(f"{self._dir}/{self.zip}"):
            print("-> FFMPEG zip is already downloaded.")
            return
        
        try:
            print("-> Downloading FFmpeg...")
            print("-> This will take a moment...")
            response = requests.get(self.url)

            if response.status_code == 200:
                # Create the zipfile in the current directory
                with open(f"{self._dir}/{self.zip}", 'wb') as file:
                    file.write(response.content)

                print("-> File downloaded successfully!")
            else:
                print("-> Download failed.")

        except Exception as e:
            print("-> Error downloading file:", e)

    def extract_zip(self):
        with zip.ZipFile(f"{self._dir}/{self.zip}", "r") as z_ref:
            try: 
                print("-> Extracting FFmpeg executables...")
                # Extract ffmpeg.exe and ffprobe.exe
                ffmpeg = z_ref.read("ffmpeg-8.0-essentials_build/bin/ffmpeg.exe")
                ffprobe = z_ref.read("ffmpeg-8.0-essentials_build/bin/ffprobe.exe")

                # Create ffmpeg.exe in the ffmpeg folder
                with open(f"{self.folder}/ffmpeg.exe", 'wb') as f:
                    f.write(ffmpeg)

                # Create ffprobe.exe in the ffmpeg folder
                with open(f"{self.folder}/ffprobe.exe", 'wb') as f:
                    f.write(ffprobe)

                print("-> FFmpeg executables extracted successfully!")
            except Exception as e:
                print("-> Error extracting FFmpeg executables:", e)

    def init(self):
        print("[FFMPEG] Initializing...")
        if os.path.exists("ffmpeg/ffmpeg.exe" and "ffmpeg/ffprobe.exe"):
            print("-> Executables found.")
            return
        
        if os.path.exists(f"{self.folder}/ffmpeg"):
            shutil.rmtree(f"{self.folder}/ffmpeg")

        print("-> This will only run once.")

        self.init_folder()
        self.download_zip()
        self.extract_zip()

        # Optional: remove zip file to save space
        os.remove(f"{self._dir}/{self.zip}")

if __name__ == "__main__":
    ffmpeg = FFMPEG()
    ffmpeg.init()