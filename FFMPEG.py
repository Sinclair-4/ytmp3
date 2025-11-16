from tqdm import tqdm
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


    def printErr(self, message):
        print(f"\033[91m[FFMPEG] -> {message}\033[0m")
    def printSuccess(self, message):
        print(f"\033[92m[FFMPEG] -> {message}\033[0m")


    def init_folder(self):
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)


    def download_zip(self):
        if os.path.exists(f"{self._dir}/{self.zip}"):
            self.printSuccess("FFMPEG zip is already downloaded.")
            return
        
        url = self.url
        filename = self.zip

        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length'))

            progress_bar = tqdm(
                total=total_size,
                unit='B',
                unit_scale=True,
                desc="[FFMPEG] -> Downloading",
                ncols=40,
                bar_format='{l_bar}{bar} | {n_fmt}/{total_fmt}'
            )

            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        progress_bar.update(len(chunk))

            progress_bar.close()

            if total_size != 0 and progress_bar.n != total_size:
                self.printErr("Download failed.")
                os.remove(f"{self._dir}/{filename}")
            else:
                self.printSuccess("File downloaded successfully!")

        except Exception as e:
            self.printErr(f"Error downloading file: {e}")
            os.remove(f"{self._dir}/{filename}")
 

    def extract_zip(self):
        try:
            with zip.ZipFile(f"{self._dir}/{self.zip}", "r") as z_ref:
                print("[FFMPEG] -> Extracting FFmpeg executables...")
                ffmpeg = z_ref.read("ffmpeg-8.0-essentials_build/bin/ffmpeg.exe")
                ffprobe = z_ref.read("ffmpeg-8.0-essentials_build/bin/ffprobe.exe")

                with open(f"{self.folder}/ffmpeg.exe", 'wb') as f:
                    f.write(ffmpeg)

                with open(f"{self.folder}/ffprobe.exe", 'wb') as f:
                    f.write(ffprobe)

                self.printSuccess("FFmpeg executables extracted successfully!")
        except zip.BadZipFile as e:
            self.printErr(f"Error extracting FFmpeg executables: {e}")
            self.printErr(f"Error type: {type(e).__name__}")

            self.printErr(f"Attempting to download again...")
            os.remove(f"{self._dir}/{self.zip}")
            self.download_zip()

        except Exception as e:
            self.printErr(f"Error extracting FFmpeg executables: {e}")
            self.printErr(f"Error type: {type(e).__name__}")


    def init(self):
        print("[FFMPEG] -> Initializing...")
        if os.path.exists("ffmpeg/ffmpeg.exe") and os.path.exists("ffmpeg/ffprobe.exe"):
            self.printSuccess("Executables found.")
            return
        
        if os.path.exists(self.folder):
            print("[FFMPEG] -> Removing old folder...")
            shutil.rmtree(self.folder)

        print("[FFMPEG] -> This will only run once.")

        self.init_folder()
        self.download_zip()
        self.extract_zip()

        print("[FFMPEG] -> Removing zip file...")
        os.remove(f"{self._dir}/{self.zip}")


if __name__ == "__main__":
    ffmpeg = FFMPEG()
    ffmpeg.init()
