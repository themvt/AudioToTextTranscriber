import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from datetime import datetime
import os
from utils_file import get_files_in_directory
from transcription import transcribe_audio_files

class TranscriberApp:
    def __init__(self, root):
        # Assign root to self.root
        self.root = root
        
        # Initialize cached directories
        self.last_target_dir = self.load_last_directory("target_dir")
        self.last_output_dir = self.load_last_directory("output_dir")
        
        self.transcription_in_progress = False

        self.root.title("Audio to Text Transcriber")
        self.root.geometry("800x500")
        self.root.minsize(800, 500)
        self.root.configure(bg='#008080')  # Set teal background color

        # Set the window to always be on top
        self.root.attributes("-topmost", True)  # Make window always on top by default

        # Configure grid layout to allow resizing
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(6, weight=1)

        # Initialize "Always on Top" checkbox as checked
        self.always_on_top_var = tk.BooleanVar(value=True)
        self.always_on_top_checkbox = tk.Checkbutton(root, text="Always on Top", variable=self.always_on_top_var,
                                                     command=self.toggle_always_on_top, bg='#008080', fg='white')
        self.always_on_top_checkbox.grid(row=8, column=0, padx=10, pady=10, sticky="w")

        # Title and description
        self.title_label = tk.Label(root, text="Audio to Text Transcriber", font=("Helvetica", 18, "bold"), bg='#008080', fg='white')
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(10, 5))

        self.description_label = tk.Label(root, text="This application allows you to transcribe audio files into text using OpenAI's Whisper API.",
                                          font=("Helvetica", 10), bg='#008080', fg='white')
        self.description_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))

        # Target folder selection
        self.target_label = tk.Label(root, text="Target Folder:", bg='#008080', fg='white')
        self.target_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.target_entry = tk.Entry(root)
        self.target_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.browse_target_button = tk.Button(root, text="Browse Target", command=self.browse_target)
        self.browse_target_button.grid(row=2, column=2, padx=10, pady=5, sticky="ew")

        # Output folder selection
        self.output_label = tk.Label(root, text="Output Folder:", bg='#008080', fg='white')
        self.output_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.output_entry = tk.Entry(root)
        self.output_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        self.browse_output_button = tk.Button(root, text="Browse Output", command=self.browse_output)
        self.browse_output_button.grid(row=3, column=2, padx=10, pady=5, sticky="ew")

        # Debug display area
        self.log_text_area = tk.Text(root, height=15, state=tk.DISABLED)
        self.log_text_area.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        scroll_bar = tk.Scrollbar(root)
        scroll_bar.grid(row=6, column=3, sticky="ns")
        
        self.log_text_area.config(yscrollcommand=scroll_bar.set)
        scroll_bar.config(command=self.log_text_area.yview)

        # Control buttons with centered alignment and equal width
        button_padding = 30  # Increased padding on sides to ensure consistent button width
        self.cancel_button = tk.Button(root, text="CANCEL", command=self.cancel_transcription, bg="orange", fg="white", width=15)
        self.cancel_button.grid(row=7, column=0, padx=(button_padding, 5), pady=10, sticky="ew")

        self.run_button = tk.Button(root, text="RUN", command=self.run_transcription, bg="blue", fg="white", width=15)
        self.run_button.grid(row=7, column=1, padx=5, pady=10, sticky="ew")

        self.exit_button = tk.Button(root, text="EXIT", command=root.quit, bg="red", fg="white", width=15)
        self.exit_button.grid(row=7, column=2, padx=(5, button_padding), pady=10, sticky="ew")

        # Author and version info on the right
        current_time = datetime.now().strftime("%Y%m%d-%H:%M")
        self.version_label = tk.Label(root, text=f"Version: {current_time}", font=("Helvetica", 9, "italic"), bg='#008080', fg='white')
        self.version_label.grid(row=8, column=2, padx=10, pady=10, sticky="e")

        self.author_label = tk.Label(root, text="Author: Marco V. Torresi", font=("Helvetica", 9, "italic"), bg='#008080', fg='white')
        self.author_label.grid(row=8, column=1, pady=10, sticky="e")

    def browse_target(self):
        initial_dir = self.last_target_dir if self.last_target_dir else '/'
        directory = filedialog.askdirectory(initialdir=initial_dir)
        if directory:
            self.last_target_dir = directory  # Update cache
            self.save_last_directory("target_dir", directory)
            self.target_entry.delete(0, tk.END)
            self.target_entry.insert(0, directory)
    
    def browse_output(self):
        initial_dir = self.last_output_dir if self.last_output_dir else '/'
        directory = filedialog.askdirectory(initialdir=initial_dir)
        if directory:
            self.last_output_dir = directory  # Update cache
            self.save_last_directory("output_dir", directory)
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, directory)
    
    def run_transcription(self):
        if not self.transcription_in_progress:
            self.transcription_in_progress = True
            target_dir = self.target_entry.get()
            output_dir = self.output_entry.get()
            audio_files = get_files_in_directory(target_dir, extensions=[".mp3", ".wav", ".flac"])
            self.log("Starting transcription...")
            transcribe_audio_files(audio_files, output_dir, log_callback=self.log)
            self.transcription_in_progress = False
    
    def cancel_transcription(self):
        if self.transcription_in_progress:
            self.log("Transcription canceled.")
            self.transcription_in_progress = False

    def toggle_always_on_top(self):
        current_state = self.root.attributes("-topmost")
        self.root.attributes("-topmost", not current_state)
        self.always_on_top_var.set(not current_state)

    def log(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        formatted_message = f"{timestamp} - {message}"
        
        self.log_text_area.config(state=tk.NORMAL)  # Temporarily make text area editable to insert logs
        self.log_text_area.insert(tk.END, formatted_message + "\n")
        self.log_text_area.see(tk.END)  # Scroll to the bottom
        self.log_text_area.config(state=tk.DISABLED)  # Set back to read-only

    def load_last_directory(self, dir_type):
        """Load last used directory from a file."""
        if os.path.exists(f"{dir_type}.txt"):
            with open(f"{dir_type}.txt", "r") as file:
                return file.read().strip()
        return None

    def save_last_directory(self, dir_type, directory):
        """Save last used directory to a file."""
        with open(f"{dir_type}.txt", "w") as file:
            file.write(directory)

if __name__ == "__main__":
    root = tk.Tk()
    app = TranscriberApp(root)
    root.mainloop()
