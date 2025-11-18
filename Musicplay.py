import pygame
import tkinter as tk
from tkinter import filedialog
import os
import threading
import time

# Initialize pygame mixer
pygame.mixer.init()

# Global state
paused = False
current_index = 0
playlist = []
update_progress = True

# ---------- Functions ----------

def load_file():
    """Select a single MP3 file"""
    global playlist, current_index
    file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    if file_path:
        playlist = [file_path]
        current_index = 0
        update_song_label()
        play_music()

def load_folder():
    """Select a folder containing MP3 files"""
    global playlist, current_index
    folder_path = filedialog.askdirectory()
    if folder_path:
        playlist = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".mp3")]
        playlist.sort()
        if playlist:
            current_index = 0
            update_song_label()
            play_music()

def update_song_label():
    if playlist:
        song_label.config(text=f"Loaded: {os.path.basename(playlist[current_index])}")

def play_music():
    global paused, update_progress
    if playlist:
        song = playlist[current_index]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        paused = False
        status_label.config(text="Playing...")
        update_song_label()
        update_progress = True
        threading.Thread(target=update_progress_bar, daemon=True).start()

def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True
    status_label.config(text="Paused")

def stop_music():
    global update_progress
    pygame.mixer.music.stop()
    paused = False
    status_label.config(text="Stopped")
    update_progress = False
    progress_canvas.delete("all")

def next_song():
    global current_index
    if playlist:
        current_index = (current_index + 1) % len(playlist)
        play_music()

def prev_song():
    global current_index
    if playlist:
        current_index = (current_index - 1) % len(playlist)
        play_music()

def update_progress_bar():
    global update_progress
    while update_progress:
        try:
            length = get_song_length(playlist[current_index])
            pos = pygame.mixer.music.get_pos() / 1000
            progress_canvas.delete("all")
            bar_width = 350
            point_x = int((pos / length) * bar_width) if length > 0 else 0
            # Draw background bar
            progress_canvas.create_rectangle(0, 12, bar_width, 18, fill="#003300", outline="white")
            # Draw progress bar
            progress_canvas.create_rectangle(0, 12, point_x, 18, fill="#00FF00", outline="")
            # Draw moving point
            progress_canvas.create_oval(point_x-5, 8, point_x+5, 22, fill="white")
            time.sleep(0.2)
        except:
            break


# ---------- GUI Setup ----------

root = tk.Tk()
root.title("Retro MP3 Player 🎵")
root.geometry("450x350")
root.configure(bg="#111111")

# Labels
song_label = tk.Label(root, text="No file loaded", bg="#111111", fg="#00FF00", font=("Courier", 11))
song_label.pack(pady=10)

status_label = tk.Label(root, text="Idle", bg="#111111", fg="#00FF00", font=("Courier", 10))
status_label.pack(pady=5)

# Progress bar
progress_canvas = tk.Canvas(root, width=350, height=30, bg="#111111", highlightthickness=0)
progress_canvas.pack(pady=10)

# Buttons frame
button_frame = tk.Frame(root, bg="#111111")
button_frame.pack(side=tk.BOTTOM, pady=20)

# Helper to create round buttons
def create_round_button(frame, text, command):
    btn = tk.Button(frame, text=text, command=command, bg="#333333", fg="#00FF00", width=6, height=2, relief="flat", font=("Courier", 10))
    btn.pack(side=tk.LEFT, padx=5)
    return btn

# Top frame for file/folder selection
top_frame = tk.Frame(root, bg="#111111")
top_frame.pack(pady=5)

file_btn = tk.Button(top_frame, text="Open File", command=load_file, bg="#333333", fg="#00FF00", font=("Courier", 10))
file_btn.pack(side=tk.LEFT, padx=5)
folder_btn = tk.Button(top_frame, text="Open Folder", command=load_folder, bg="#333333", fg="#00FF00", font=("Courier", 10))
folder_btn.pack(side=tk.LEFT, padx=5)

# Buttons at bottom
prev_btn = create_round_button(button_frame, "<<", prev_song)
play_btn = create_round_button(button_frame, "Play", play_music)
pause_btn = create_round_button(button_frame, "Pause", pause_music)
stop_btn = create_round_button(button_frame, "Stop", stop_music)
next_btn = create_round_button(button_frame, ">>", next_song)

root.mainloop()
