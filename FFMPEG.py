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
        print(f"\033[91m{message}\033[0m")

    def printSuccess(self, message):
        print(f"\033[92m{message}\033[0m")

    def init_folder(self):
        # Check if folder exists
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

    # def download_zip(self):
    #     # Check if zip is already downloaded
    #     if os.path.exists(f"{self._dir}/{self.zip}"):
    #         # print("-> FFMPEG zip is already downloaded.")
    #         self.printSuccess("-> FFMPEG zip is already downloaded.")
    #         return
        
    #     try:
    #         print("-> Downloading FFmpeg...")
    #         print("-> This will take a moment...")
    #         response = requests.get(self.url, timeout=10)

    #         if response.status_code == 200:
    #             # Create the zipfile in the current directory
    #             with open(f"{self._dir}/{self.zip}", 'wb') as file:
    #                 file.write(response.content)

    #             # print("-> File downloaded successfully!")
    #             self.printSuccess("-> File downloaded successfully!")
    #         else:
    #             # print("-> Download failed.")
    #             self.printErr("-> Download failed.")

    #     except Exception as e:
    #         # print("-> Error downloading file:", e)
    #         self.printErr(f"-> Error downloading file: {e}")


    def download_zip(self):
        if os.path.exists(f"{self._dir}/{self.zip}"):
            # print("-> FFMPEG zip is already downloaded.")
            self.printSuccess("-> FFMPEG zip is already downloaded.")
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
                desc=f"Downloading",
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
                self.printErr("-> Download failed.")
                os.remove(f"{self._dir}/{filename}")
            else:
                self.printSuccess("-> File downloaded successfully!")

        except Exception as e:
            self.printErr(f"-> Error downloading file: {e}")
            os.remove(f"{self._dir}/{filename}")

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

                # print("-> FFmpeg executables extracted successfully!")
                self.printSuccess("-> FFmpeg executables extracted successfully!")
            except Exception as e:
                # print("-> Error extracting FFmpeg executables:", e)
                self.printErr(f"-> Error extracting FFmpeg executables: {e}")

    def init(self):
        print("[FFMPEG] Initializing...")
        if os.path.exists("ffmpeg/ffmpeg.exe" and "ffmpeg/ffprobe.exe"):
            # print("-> Executables found.")
            self.printSuccess("-> Executables found.")
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