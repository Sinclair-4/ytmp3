from yt_dlp_script import YtMp3
from FFMPEG import FFMPEG
from pathlib import Path
import requests
import sys
import os

class App:
    def __init__(self):
        self.urls = []
        self._dir = Path(__file__).parent
        self.ffmpeg = None
        self.downloader = None
        self.output_dir = None
        self.ffmpeg_location = Path(self._dir / "ffmpeg")


    def printErr(self, message):
        print(f"\033[91m{message}\033[0m")
    def printSuccess(self, message):
        print(f"\033[92m{message}\033[0m")


    def init_ffmpeg(self) -> bool:
        try:
            self.ffmpeg = FFMPEG()
            self.ffmpeg.init()
            return True
        except Exception as e:
            # print(f"-> Error initializing FFMPEG: {e}")
            self.printErr(f"-> Error initializing FFMPEG: {e}")
            return False
        
    
    def set_output_dir(self):
        while True:
            output = input("Enter the output directory: ").strip()

            if not Path(output).exists():
                # print(f"-> Directory '{output}' does not exist")
                self.printErr(f"-> Directory '{output}' does not exist")
                continue

            confirm = input("Confirm? (y/n): ").lower()

            if confirm == 'y':
                # print(f"-> output_dir: {Path(output)}")
                self.printSuccess(f"-> Output set to: {Path(output)}")
                return output

    def init_downloader(self) -> bool:
        try:
            self.downloader = YtMp3(
                ffmpeg_location = str(self.ffmpeg_location),
                output = str(self.output_dir)
            )
            # print("-> Downloader initialized successfully!")
            self.printSuccess("-> Downloader initialized successfully!")
            return True
        except Exception as e:
            # print(f"-> Error initializing Downloader: {e}")
            self.printErr(f"-> Error initializing Downloader: {e}")
            return False
        

    def is_valid_yt_url(self, url):
        try:
            res = requests.get(url, timeout=5, stream=True, allow_redirects=True)
            res.close()
            # print("-> Input URL is valid.")
            self.printSuccess("-> Input URL is valid.")
            return True
        except Exception as e:
            # print("-> Error validating URL:", e)
            self.printErr("-> Error validating URL:", e)
            return False


    def add_url(self):
        
        while True: 
            print("[YTMP3] Enter 'q' or 'Q' to quit adding url...")
            url = ''
            while url.strip() == '':  
                url = input("Enter the URL: ").strip()
            
            if url == 'q' or url == 'Q':
                print("-> Returning to main menu...")
                return
            
            if not self.is_valid_yt_url(url):
                # print("-> Invalid URL or unable to connect")
                # print("-> Removing input...")
                self.printErr("-> Invalid URL or unable to connect")
                self.printErr("-> Removing input...")
                print()
                continue
            
            remove = url.find("&list=")

            if remove != -1:
                print("-> Sanitizing URL...")
                url = url[:remove]
                print("-> URL sanitized:", url)
            
            if url and url not in self.urls:
                self.urls.append(url)
                # print(f"-> Added URL ({len(self.urls)} total)")
                self.printSuccess(f"-> Added URL ({len(self.urls)} total)")
            else:
                # print("-> URL is empty or already in list")
                self.printErr("-> URL is empty or already in list")
            
            print()


    def remove_url(self):
        if not self.urls:
            print("-> No URLs to remove")
            return

        self.view_urls()
        print()
        
        try:
            choice = int(input("Enter the number of the URL to remove: "))
            if 1 <= choice <= len(self.urls):
                removed_url = self.urls.pop(choice - 1)
                print(f"-> Removed: {removed_url}")
            else:
                # print("-> Invalid number")
                self.printErr("-> Invalid number")
        except ValueError:
            # print("-> Please enter a valid number")
            self.printErr("-> Please enter a valid number")


    def view_urls(self):
        if not self.urls:
            print("No URLs in download list")
            return

        print("Download List:")
        print("----=====================================----")
        for i, url in enumerate(self.urls, 1):
            print(f"{i:2d}. {url}")
        print(f"Total: {len(self.urls)} URL(s)")


    def clear_list(self):
        if self.urls:
            confirm = input(f"Clear all {len(self.urls)} URLs? (y/n): ").lower()
            if confirm == 'y':
                self.urls.clear()
                print("-> All URLs cleared")
        else:
            print("List is already empty")


    def download_all(self):
        if not self.urls:
            print("No URLs to download")
            return

        if not self.downloader:
            # print("Downloader not initialized")
            self.printErr("Downloader not initialized")
            return

        print(f"Starting download of {len(self.urls)} file(s)...")
        print("----=====================================----")
        
        successful_downloads = 0
        for i, url in enumerate(self.urls, 1):
            print(f"\nDownloading {i}/{len(self.urls)}...")
            try:
                download = self.downloader.downloadMP3(url)

                if download:
                    successful_downloads += 1
                    
            except Exception as e:
                # print(f"Download {i} failed: {e}")
                self.printErr(f"Download {i} failed: {e}")
        
        print()
        # print(f"Download summary: {successful_downloads}/{len(self.urls)} successful")

        if successful_downloads == len(self.urls):
            self.printSuccess(f"Download summary: {successful_downloads}/{len(self.urls)} successful")
        elif successful_downloads < len(self.urls) and successful_downloads > 0:
            print(f"\033[93mDownload summary: {successful_downloads}/{len(self.urls)} successful\033[0m")
        else:
            self.printErr(f"Download summary: {successful_downloads}/{len(self.urls)} successful")

    def run(self):
        print("----=====================================----")
        print("|              YTMP3 - Sinclair             |")
        print("----=====================================----")
        print("[YTMP3] ---< Initializing FFMPEG >-----------")
        if not self.init_ffmpeg():
            # print("Failed to initialize FFMPEG")
            self.printErr("Failed to initialize FFMPEG")
            sys.exit(1)
        print()
        print("----=====================================----")
        print("[YTMP3] --< Setting Output Directory >-------")
        self.output_dir = self.set_output_dir()
        print()
        print("----=====================================----")
        print("[YTMP3] --< Initializing Downloader >--------")
        if not self.init_downloader():
            # print("Failed to initialize Downloader")
            self.printErr("Failed to initialize Downloader")
            sys.exit(1)
        print()
        
        while True:
            print("----=====================================----")
            print("|                 MAIN MENU                 |")
            print("----=====================================----")
            print("|         [1] Add URL to download           |")
            print("|         [2] Remove URL from list          |") 
            print("|         [3] View all URLs                 |")
            print("|         [4] Clear all URLs                |")
            print("|         [5] Download all URLs             |")
            print("|         [6] Exit                          |")
            print("----=====================================----")
            print()

            choice = None
            while choice not in ["1", "2", "3", "4", "5", "6"]:
                choice = input("Enter your choice (1-6): ").strip()
            print()

            if choice == "1":
                self.add_url()
            elif choice == "2":
                self.remove_url()
            elif choice == "3":
                self.view_urls()
            elif choice == "4":
                self.clear_list()
            elif choice == "5":
                self.download_all()
            elif choice == "6":
                print("\033[93m" + "----=====================================----")
                print("\\     -< Thank you for using YTMP3! >-      /")
                print("/             -< Sinclair >-                \\")
                print("----=====================================----" + "\033[0m")
                break
            else:
                # print("Invalid choice. Please enter 1-6.")
                self.printErr("Invalid choice. Please enter 1-6.")

            print()

if __name__ == "__main__":
    os.system('cls')
    app = App()
    app.run()