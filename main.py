import sys
from pathlib import Path
from yt_dlp_script import YtMp3
from FFMPEG import FFMPEG

class AudioDownloader:
    def __init__(self):
        self.urls = []
        self.yt_downloader = None
        self.ffmpeg = FFMPEG()

    def initialize_ffmpeg(self) -> bool:
        try:
            self.ffmpeg.init()
            return True
        except Exception as e:
            print(f"Failed to initialize FFMPEG: {e}")
            return False

    def get_output_directory(self) -> str:
        while True:
            output = input("Enter the output directory: ").strip()

            if not Path(output).exists():
                print(f"Directory '{output}' does not exist")
                continue

            confirm = input("Confirm? (y/n): ").lower()

            if confirm == 'y':
                return output

        # return 'C:/Users/user/Music/'

    def initialize_downloader(self) -> bool:
        if not self.initialize_ffmpeg():
            return False

        output_dir = self.get_output_directory()
        ffmpeg_path = Path.cwd() / "ffmpeg"

        try:
            self.yt_downloader = YtMp3(
                output=output_dir,
                ffmpeg_location=ffmpeg_path
            )
            print("Downloader initialized successfully!")
            return True
        except Exception as e:
            print(f"Failed to initialize downloader: {e}")
            return False

    def add_url(self):
        url = input("Enter the URL: ").strip()
        if url and url not in self.urls:
            self.urls.append(url)
            print(f"Added URL ({len(self.urls)} total)")
        else:
            print("URL is empty or already in list")

    def remove_url(self):
        if not self.urls:
            print("No URLs to remove")
            return

        self.view_urls()
        print()
        
        try:
            choice = int(input("Enter the number of the URL to remove: "))
            if 1 <= choice <= len(self.urls):
                removed_url = self.urls.pop(choice - 1)
                print(f"Removed: {removed_url}")
            else:
                print("Invalid number")
        except ValueError:
            print("Please enter a valid number")

    def view_urls(self):
        if not self.urls:
            print("No URLs in download list")
            return

        print("\nDownload List:")
        print("-" * 50)
        for i, url in enumerate(self.urls, 1):
            print(f"{i:2d}. {url}")
        print(f"Total: {len(self.urls)} URL(s)")

    def download_all(self):
        if not self.urls:
            print("No URLs to download")
            return

        if not self.yt_downloader:
            print("Downloader not initialized")
            return

        print(f"\nStarting download of {len(self.urls)} file(s)...")
        print("-" * 50)
        
        successful_downloads = 0
        for i, url in enumerate(self.urls, 1):
            print(f"\nDownloading {i}/{len(self.urls)}...")
            try:
                download = self.yt_downloader.downloadMP3(url)

                if download:
                    successful_downloads += 1
                    
            except Exception as e:
                print(f"Download {i} failed: {e}")
        
        print(f"\nDownload summary: {successful_downloads}/{len(self.urls)} successful")

    def clear_list(self):
        if self.urls:
            confirm = input(f"Clear all {len(self.urls)} URLs? (y/n): ").lower()
            if confirm == 'y':
                self.urls.clear()
                print("All URLs cleared")
        else:
            print("List is already empty")

    def run(self):
        print("YouTube Audio Downloader")
        print("=" * 40)
        
        if not self.initialize_downloader():
            print("Failed to initialize application")
            sys.exit(1)

        while True:
            print("\n" + "=" * 40)
            print("MAIN MENU")
            print("=" * 40)
            print("[1] Add URL to download")
            print("[2] Remove URL from list") 
            print("[3] View all URLs")
            print("[4] Clear all URLs")
            print("[5] Download all URLs")
            print("[6] Exit")
            print()

            choice = input("Enter your choice (1-6): ").strip()

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
                print("\nThank you for using YTMP3!")
                print(" - Sinclair")
                break
            else:
                print("Invalid choice. Please enter 1-6.")


def main():
    try:
        downloader = AudioDownloader()
        downloader.run()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
