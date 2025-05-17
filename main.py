import os.path
from idlelib.zoomheight import set_window_geometry

import fitz
import edge_tts
import asyncio
import threading
import tkinter as tk
from tkinter import messagebox, filedialog, ttk


class PdfToSpeech:
    def __init__(self, window):
        self.window = window
        self.window.title("PDF to speech APP")
        self.window.config(padx=20, pady=20)
        self.window.geometry("600x600")
        self.file_name = ""
        self.book = ""
        self.voices = {"English": "en-US-GuyNeural",
                       "Ukraine": "uk-UA-OstapNeural"}

        # UI
        # Open dialog and file frame
        # Openfile Button
        self.open_file_button = tk.Button(self.window, text="Open PDF File", font=("Calibri", 18, "bold"),
                                          command=self.open_file)
        self.open_file_button.pack()

        # Book Name Label
        self.file_name_label = tk.Label(self.window, text="File name: Not open yet", font=("Calibri", 14))
        self.file_name_label.pack(pady=10)

        # Text preview Label
        self.text_preview_label = tk.Label(self.window, text="Short preview", font=("Calibri", 14))
        self.text_preview_label.pack()

        # Text preview
        self.text_preview = tk.Text(self.window, height=15, wrap="word", font=("Calibri", 14))
        self.text_preview.config(state="disabled")
        self.text_preview.pack(fill="x", pady=10)


        # Bottom buttons frame
        self.bottom_frame = tk.Frame(self.window)
        self.bottom_frame.pack(fill="x")

        # Play button
        self.play_button = tk.Button(self.bottom_frame, text="Play file", font=("Calibri", 18, "bold"),
                                          command=self.open_file)
        self.play_button.config(state="disabled")
        self.play_button.pack(side="left")

        # Save button
        self.save_button = tk.Button(self.bottom_frame, text="Save file", font=("Calibri", 18, "bold"),
                                          command=self.run_async_save_to_mp3)
        self.save_button.config(state="disabled")
        self.save_button.pack(side="right")

        # Choose voice combobox
        self.combo_box = ttk.Combobox(self.bottom_frame, values=self.receive_voices_names())
        self.combo_box.set("Select voice")
        self.combo_box.config(state="disabled")
        self.combo_box.pack(side="right", padx=5)


    def truncate_filename(self, filepath, max_length=30):
        """
        Truncate file name to 30 chars to avoid long name
        :param filepath: path of file
        :param max_length: static param, length of name
        :return: str, processed filename
        """
        filename = os.path.basename(filepath)
        return filename if len(filename) <= max_length else filename[:max_length - 3] + "..."

    def receive_voices_names(self):
        """
        Make list of keys from self.voices for voice Combobox
        :return: list of keys
        """
        return [key for key, value in self.voices.items()]

    def open_file(self):
        """
        Open PDF file and save into self.book as text
        :return: nothing
        """
        self.book = ""
        try:
            # Take file path
            filepath = filedialog.askopenfilename(
                title="Chose PDF file",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            # Take file name
            self.file_name = self.truncate_filename(filepath)

            # If file not PDF
            if not filepath.lower().endswith(".pdf"):
                raise ValueError("Invalid file format. Please select a PDF file.")

            # Open PDF file and save into self.book as text
            doc = fitz.open(filepath)
            for page in doc:
                self.book += page.get_text()

            # Show preview
            self.text_preview.config(state="normal")
            self.text_preview.delete("1.0", "end")
            self.text_preview.insert("1.0", self.book)
            self.text_preview.config(state="disabled")

            # Change label and buttons
            self.file_name_label.config(text=f"File name: {self.file_name}")
            self.save_button.config(state="normal")
            self.play_button.config(state="normal")
            self.combo_box.config(state="normal")

        except Exception as e:
           messagebox.showerror(f"Error: {e}")


    async def save_to_mp3(self):
        """
        Save audio .mp3 into /audio folder
        :return: nothing
        """
        # Make correct folder path
        folder_path = os.path.join(os.getcwd(), "audio")
        # Check if folder exist
        os.makedirs(folder_path, exist_ok=True)
        # Create full path
        filepath = os.path.join(folder_path, f"{self.file_name}.mp3")
        if os.path.exists(filepath):
            filepath = os.path.join(folder_path, f"{self.file_name}_new.mp3")

        try:
            self.combo_box.config(state="disabled")
            self.save_button.config(state="disabled", text="Saving...")
            self.open_file_button.config(state="disabled")
            # Check empty book
            if not self.book.strip():
                raise ValueError("Book is empty. Please load file first.")
            # Save file
            voice = self.voices[f"{self.combo_box.get()}"] # Voice choose
            tts = edge_tts.Communicate(text=self.book, voice=voice)
            await tts.save(filepath)

            messagebox.showinfo("Good news", f"Your book {self.file_name} was saved into audio folder")

        except Exception as e:
            messagebox.showerror("Error", f"Something goes wrong: \n {e}")

        finally:
            self.save_button.config(state="normal", text="Save file")
            self.open_file_button.config(state="normal")

    def run_async_save_to_mp3(self):
        """
        Wrapper for the asynchronous save_to_mp3 function. Required for binding to a button save_button.
        :return: nothing
        """
        threading.Thread(target=lambda: asyncio.run(self.save_to_mp3())).start()



if __name__ == "__main__":
    root = tk.Tk()
    app = PdfToSpeech(root)
    root.mainloop()