import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from PIL.Image import Resampling
import queue
import sys

if sys.platform.startswith('win'):
    import ctypes
    from ctypes import wintypes
    from ctypes import windll

class AssistantGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # Removes the window decorations
        self.root.attributes('-topmost', True)
        unique_color = "#abcdef"  # This should be a color not used in other widgets
        self.root.configure(bg=unique_color)
        self.root.attributes('-transparentcolor', unique_color)

        # System tray setup
        if sys.platform.startswith('win'):
            self.add_to_system_tray()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width // 2)
        window_height = int(screen_height // 1.2)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')

        window_space = 10

        self.user_text_var = tk.StringVar()
        self.ai_text_var = tk.StringVar()

        text_color = "#%02x%02x%02x" % (224, 226, 231)  # Light grey color
        background_color = "#%02x%02x%02x" % (7, 28, 49)  # Dark blue color

        self.user_label = tk.Label(
            self.root,
            textvariable=self.user_text_var,
            font=('Helvetica', 18),
            justify=tk.LEFT,
            anchor='w',
            wraplength=window_width - 40,
            fg=text_color,
            bg=background_color,
            borderwidth=0,
            relief=tk.RIDGE # tk.RAISED, tk.SUNKEN, tk.GROOVE, and .tk.FLAT
        )
        self.ai_label = tk.Label(
            self.root,
            textvariable=self.ai_text_var,
            font=('Helvetica', 18),
            justify=tk.LEFT,
            anchor='w',
            wraplength=window_width - 40,
            fg=text_color,
            bg=background_color,
            borderwidth=0,
            relief=tk.RIDGE # tk.RAISED, tk.SUNKEN, tk.GROOVE, and .tk.FLAT
        )

        self.user_label.place(
            x=0,
            #y=(window_height // 2) - window_space - self.user_label.winfo_reqheight(),
            y=(window_height // 2) - window_space - 100,
            #y=(window_height // 2),
            width=window_width-20,
            height=100,
        )
        self.user_label.place_forget()

        self.ai_label.place(
            x=0,
            # y=window_height // 2 + window_space + self.ai_label.winfo_reqheight(),
            y=(window_height // 2) + window_space,
            width=window_width-20,
            height=100,
        )
        self.ai_label.place_forget()

        # Load and position microphone image
        mic_image = Image.open("microphone_icon.png").convert("RGBA")
        baseheight = int(window_height / 4)
        hpercent = (baseheight / float(mic_image.size[1]))
        wsize = int((float(mic_image.size[0]) * float(hpercent)))
        mic_image = mic_image.resize((wsize, baseheight), Resampling.LANCZOS)
        self.mic_photo = ImageTk.PhotoImage(mic_image)

        self.animation_x = window_width // 2 - wsize // 2
        self.animation_y = (window_height // 2) - baseheight

        self.animation_label = tk.Label(
            self.root,
            bg=unique_color,
            image=self.mic_photo,
            borderwidth=0,
        )

        self.animation_label.place(
            x=self.animation_x,
            y=self.animation_y,
        )
        self.animation_label.place_forget()

        self.queue = queue.Queue()
        self.process_queue()

    def user_message(self, text):
        self.user_text_var.set(text)
        self.user_label.place(
            x=0,
            y=(self.root.winfo_height() // 2) - 90,
            width=self.root.winfo_width(),
            height=self.user_label.winfo_reqheight()+20,
        )

    def clear_user_message(self):
        self.user_text_var.set("")
        if self.user_text_var.get() == "":
            self.user_label.place_forget()

    def ai_message(self, text):
        self.ai_text_var.set(text)
        self.ai_label.place(
            x=0,
            y=(self.root.winfo_height() // 2) + 10,
            width=self.root.winfo_width(),
            height=self.ai_label.winfo_reqheight()+20,
        )

    def clear_ai_message(self):
        self.ai_text_var.set("")
        if self.ai_text_var.get() == "":
            self.ai_label.place_forget()

    def show_listening_animation(self):
        self.animation_label.place(
            x=self.animation_x,
            y=self.animation_y)

    def hide_listening_animation(self):
        self.animation_label.place_forget()

    def hide_all(self):
        self.user_label.place_forget()
        self.ai_label.place_forget()
        self.animation_label.place_forget()

    def user_stream(self, text):
        """Append and update the text streaming in the GUI."""
        self.queue.put(f"USER_STREAM:{text}")

    def ai_stream(self, text):
        """Append and update the text streaming in the GUI."""
        self.queue.put(f"AI_STREAM:{text}")

    def start_user_stream(self):
        """Initialize the streaming text by clearing any previous content."""
        self.user_message_text = ""
        self.user_message(self.user_message_text)

    def start_ai_stream(self):
        """Initialize the streaming text by clearing any previous content."""
        self.ai_message_text = ""
        self.ai_message(self.ai_message_text)

    def append_user_stream(self, text):
        """Append text to the ongoing stream display."""
        self.user_message_text += text
        self.user_message(self.user_message_text)

    def append_ai_stream(self, text):
        """Append text to the ongoing stream display."""
        self.ai_message_text += text
        self.ai_message(self.ai_message_text)

    def add_to_system_tray(self):
        # Placeholder for Windows-specific code to add icon to the system tray
        pass

    def run_gui(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def on_closing(self):
        self.queue.put("CLOSE")

    def close(self):
        self.root.destroy()


    def process_queue(self):
        try:
            task = self.queue.get_nowait()
            if task == "CLOSE":
                self.close()
            elif task.startswith("USER_MSG:"):
                message = task.split(":", 1)[1]
                self.user_message(message)
            elif task.startswith("AI_MSG:"):
                message = task.split(":", 1)[1]
                self.ai_message(message)
            elif task.startswith("USER_STREAM:"):
                message = task.split(":", 1)[1]
                self.append_user_stream(message)
            elif task.startswith("AI_STREAM:"):
                message = task.split(":", 1)[1]
                self.append_ai_stream(message)
            elif task == "START_USER_STREAM":
                self.start_user_stream()
            elif task == "START_AI_STREAM":
                self.start_ai_stream()
            elif task == "CLEAR_USER":
                self.clear_user_message()
            elif task == "CLEAR_AI":
                self.clear_ai_message()
            elif task == "HIDE_ALL":
                self.hide_all()
            elif task == "LISTEN":
                self.show_listening_animation()
            elif task == "STOP_LISTEN":
                self.hide_listening_animation()
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_queue)

    # To run the GUI
if __name__ == "__main__":
    gui = AssistantGUI()
    gui.run_gui()
