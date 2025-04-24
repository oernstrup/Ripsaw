import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

def force_audio_jack():
    try:
        subprocess.run(["amixer", "cset", "numid=3", "1"], check=True, stdout=subprocess.DEVNULL)
        print("Audio output set to 3.5mm jack.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to set audio output to 3.5mm jack.")

def play_wav(file_path):
    if not os.path.isfile(file_path):
        messagebox.showerror("Error", f"File not found: {file_path}")
        return

    try:
        # Play using ffplay, no window (-nodisp), exit when done (-autoexit)
        subprocess.run(["ffplay", "-nodisp", "-autoexit", file_path])
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to play the audio.")

def browse_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("WAV files", "*.wav")],
        title="Select a WAV file"
    )
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

def play_selected_file():
    file_path = file_entry.get()
    if not file_path:
        messagebox.showwarning("Warning", "Please select a .wav file first.")
        return
    force_audio_jack()
    play_wav(file_path)

# GUI setup
root = tk.Tk()
root.title("Raspberry Pi WAV Player")
root.geometry("400x150")

file_entry = tk.Entry(root, width=40)
file_entry.pack(pady=10)

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=5)

play_button = tk.Button(root, text="Play on 3.5mm Jack", command=play_selected_file)
play_button.pack(pady=10)

root.mainloop()
