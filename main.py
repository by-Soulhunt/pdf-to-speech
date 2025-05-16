import os.path

import fitz
import edge_tts
import asyncio
import tkinter as tk
from tkinter import messagebox, filedialog


class PdfToSpeech:
    def __init__(self, window):
        self.window = window
        self.window.title("PDF to speech APP")
        self.window.config(padx=20, pady=20)
        self.window.geometry("600x600")
        self.file_name = ""
        self.book = ""

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
                                          command=self.open_file)
        self.save_button.config(state="disabled")
        self.save_button.pack(side="right")

    def truncate_filename(self, filepath, max_length=30):
        filename = os.path.basename(filepath)
        return filename if len(filename) <= max_length else filename[:max_length - 3] + "..."

    def open_file(self):
        """
        Open PDF file and save into self.book as text
        :return: nothing
        """
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

            # Change label
            self.file_name_label.config(text=f"File name: {self.file_name}")

        except Exception as e:
           messagebox.showerror(f"Error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PdfToSpeech(root)
    root.mainloop()