import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from pytube import YouTube
from moviepy.editor import VideoFileClip


class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Downloader")
        self.root.geometry("600x400")

        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.pack()

        self.app_title = tk.Label(
            root, text="Video Downloader", fg="blue", font=("Arial", 20)
        )
        self.canvas.create_window(300, 50, window=self.app_title)

        self.url_label = tk.Label(text="Enter Video URL")
        self.canvas.create_window(300, 80, window=self.url_label)

        self.video_url = tk.Entry(root)
        self.canvas.create_window(300, 110, window=self.video_url)

        self.select_folder_btn = tk.Button(
            root, text="Select Destination Folder", command=self.open_file_explorer
        )
        self.canvas.create_window(300, 140, window=self.select_folder_btn)

        self.destination_folder = tk.Label(root, text="")
        self.canvas.create_window(300, 170, window=self.destination_folder)

        self.start_download_button = tk.Button(
            root, text="Start Downloading", command=self.start_downloading
        )
        self.canvas.create_window(
            300, 200, window=self.start_download_button, state="DISABLED"
        )

        # Progress bar
        self.progress_bar = ttk.Progressbar(
            root,
            orient="horizontal",
            mode="determinate",
            length=300,
        )
        self.canvas.create_window(300, 240, window=self.progress_bar)

        # Status message label
        self.status_label = tk.Label(root, text="", fg="red")
        self.canvas.create_window(300, 270, window=self.status_label)

    def open_file_explorer(self):
        destination = filedialog.askdirectory()
        self.destination_folder.config(text=destination)

    def download_progress_callback(self, stream, chunk, bytes_remaining):
        file_size = stream.filesize
        bytes_downloaded = file_size - bytes_remaining
        download_percentage = (bytes_downloaded / file_size) * 100
        self.progress_bar["value"] = download_percentage

    def start_downloading(self):
        url = self.video_url.get()
        download_path = self.destination_folder.cget("text")

        try:
            yt = YouTube(url, on_progress_callback=self.download_progress_callback)
            stream = yt.streams.get_highest_resolution()
            mp4_file = stream.download(output_path=download_path)

            # Convert the downloaded video to MP3
            # video_clip = VideoFileClip(mp4_file)
            # audio_clip = video_clip.audio
            # audio_file = mp4_file.replace(".mp4", ".mp3")
            # audio_clip.write_audiofile(audio_file)
            # audio_clip.close()
            # video_clip.close()

            self.status_label.config(text="Download complete.", fg="green")
        except Exception as e:
            self.status_label.config(text=f"An error occurred: {str(e)}", fg="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
