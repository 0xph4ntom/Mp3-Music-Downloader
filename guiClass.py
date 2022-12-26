import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import filedialog
from PIL import ImageTk,Image
from pytube import Playlist, YouTube

class YouTubeDownloader:
    def __init__(self, root):
        
        self.window = root
        self.window.title("Mp3 Music Downloader")
        self.window.configure(bg="#1776C3")
        self.window.geometry("450x700")

        # Frame 1
        self.image_frame = tk.LabelFrame(self.window, bg="#1776C3", relief="flat")

        self.audioWave = ImageTk.PhotoImage(Image.open("audiowave.png"))
        self.image_label = tk.Label(self.image_frame, image=self.audioWave, bg="#1776C3")
        
        self.image_label.pack(anchor="center")
        
        self.title_label = tk.Label(self.image_frame, text="Mp3 Music Downloader", bg="#1776C3", fg="white",  font=("Arial", 24))
        self.title_label.pack(anchor="center")

        # Frame 2
        self.frame = tk.LabelFrame(self.window, bg="#1776C3", relief="flat")

        self.title = tk.Label()
        self.e = tk.Entry(self.frame, width=50, borderwidth=5)
        
        self.selected_option = tk.StringVar()
        self.radio_button1 = tk.Radiobutton(self.frame, text="Song", variable=self.selected_option, value="Song")
        self.radio_button2 = tk.Radiobutton(self.frame, text="Playlist", variable=self.selected_option, value="Playlist")
        self.selected_option.set("Song")

        # Create a button to trigger the directory selection
        self.menu_button = tk.Button(self.frame, text="Select directory", command=self.select_directory)
        
        self.download_button = tk.Button(self.frame, text="Download", command=self.download)
        
        
        self.e.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        
        self.radio_button1.grid(row=2, column=0, pady=10)
        self.radio_button2.grid(row=2, column=1, pady=10)
        

        self.download_button.grid(row=3, column=1, pady=10)
        self.menu_button.grid(row=3, column=0, pady=10)

        # Frames 
        self.image_frame.pack()
        self.frame.pack()

        

    def url_error(self):
        messagebox.showerror("Error", "Enter url and try again")

    def select_directory(self):
        # Open a file dialog and get the selected directory
        self.directory = filedialog.askdirectory()
        
    def download(self):
        url = self.e.get()
        
        if url != "":
            if self.selected_option.get() == "Song":          
                self.download_song(url=url, path_to_store=self.directory)
            elif self.selected_option.get() == "Playlist":    
                self.download_playlist(url=url, path_to_store=self.directory)
        else:
            self.url_error()

    def download_song(self, url, path_to_store):
        self.download_button.configure(state="disabled")
        song = YouTube(url)
        try:
            filename = song.title + ".mp3"
            stream = song.streams.filter(only_audio=True)
            stream.get_by_itag(140).download(output_path=path_to_store, filename=filename)
        except:
            messagebox.showerror("Error", "Couldn't download this song")
        self.download_button.configure(state="normal")

    def download_playlist(self, url, path_to_store):
        self.download_button.configure(state="disabled")
        p = Playlist(url)
        
        for song in p.videos:
            try:
                filename = song.title + ".mp3"
                stream = song.streams.filter(only_audio=True)
                stream.get_by_itag(140).download(output_path=path_to_store, filename=filename)
            except:
                messagebox.showerror("Error", "Couldn't download " + song.title)
        self.download_button.configure(state="normal")
    


    

# Create the main window
root = tk.Tk()

# Create an instance of the YouTubeDownloader class
downloader = YouTubeDownloader(root)

# Run the main loop
root.mainloop()
