# import sys
# import cv2
# import os
# import tkinter as tk
# from tkinter import scrolledtext
# from PIL import Image, ImageTk
# from vlm_api import VLM
# import threading

# # Load configuration
# CONFIG_PATH = "qwen_vl_2b_api_config.yaml"
# vlm = VLM(CONFIG_PATH)

# # Placeholder functions for Vision Language model
# def get_image_description(image, query):
#     cv2.imwrite('curr_iamge.jpg', image)
#     response = vlm.get_image_description("curr_iamge.jpg", query)
#     # Vision Language model call for image description
#     return response

# def get_text_summary(text):
#     response = vlm.get_text_summary(text)
#     # Vision Language model call for text summary
#     return response

# class ChatBotWindow(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Vision Language Chatbot")
#         self.geometry("1350x500")

#         # Open the camera
#         self.cap = cv2.VideoCapture(0)

#         # Create UI elements
#         self.create_widgets()

#         # Timer to update the image every 30 ms (approximately 33 frames per second)
#         self.after(30, self.update_image)

#     def create_widgets(self):
#         # Create a frame for video and chat sections
#         frame = tk.Frame(self)
#         frame.pack(fill=tk.BOTH, expand=True)

#         # Create a canvas to display video feed
#         self.video_label = tk.Label(frame)
#         self.video_label.grid(row=0, column=0, rowspan=2)

#         # Create chat display
#         self.chat_display = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=15, width=80)
#         self.chat_display.grid(row=0, column=1, pady=10, padx=10)
#         self.chat_display.config(state=tk.DISABLED)

#         # User input
#         self.query_input = tk.Entry(frame, width=80)
#         self.query_input.grid(row=1, column=1, pady=10, padx=10)
#         self.query_input.bind("<Return>", self.process_query)

#     def update_image(self):
#         ret, frame = self.cap.read()
#         if ret:
#             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             image = Image.fromarray(rgb_frame)
#             photo = ImageTk.PhotoImage(image=image)
#             self.video_label.config(image=photo)
#             self.video_label.image = photo

#         # Continue updating the image every 30ms
#         self.after(30, self.update_image)

#     def display_response(self, response):
#         self.chat_display.config(state=tk.NORMAL)
#         self.chat_display.insert(tk.END, f"\nBot: {response}\n")
#         self.chat_display.config(state=tk.DISABLED)
#         self.chat_display.yview(tk.END)


#     def process_query(self, event=None):
#         query = self.query_input.get()
#         self.chat_display.config(state=tk.NORMAL)
#         self.chat_display.insert(tk.END, f"\nUser: {query}\n")
#         self.chat_display.config(state=tk.DISABLED)

#         def query_task():
#             if "see" in query.lower():
#                 ret, frame = self.cap.read()
#                 if ret:
#                     description = get_image_description(frame, query)
#                     self.display_response(description)
#             else:
#                 summary = get_text_summary(query)
#                 self.display_response(summary)

#         threading.Thread(target=query_task, daemon=True).start()

#         self.query_input.delete(0, tk.END)
#         self.chat_display.yview(tk.END)


# if __name__ == '__main__':
#     window = ChatBotWindow()
#     window.mainloop()


################### chat app video with text to speech 

import sys
import cv2
import os
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
from vlm_api import VLM
import threading
from gtts import gTTS
import tempfile
import pygame

# Load configuration
CONFIG_PATH = "qwen_vl_2b_api_config.yaml"
vlm = VLM(CONFIG_PATH)

# Placeholder functions for Vision Language model
def get_image_description(image, query):
    cv2.imwrite('curr_image.jpg', image)
    response = vlm.get_image_description("curr_image.jpg", query)
    return response

def get_text_summary(text):
    response = vlm.get_text_summary(text)
    return response

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    temp_file = tempfile.NamedTemporaryFile(delete=True, suffix=".mp3")
    tts.save(temp_file.name)
    pygame.mixer.init()
    pygame.mixer.music.load(temp_file.name)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    temp_file.close()

class ChatBotWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vision Language Chatbot")
        self.geometry("1350x500")

        # Open the camera
        self.cap = cv2.VideoCapture(2)

        # Create UI elements
        self.create_widgets()

        # Timer to update the image every 30 ms
        self.after(30, self.update_image)

    def create_widgets(self):
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        self.video_label = tk.Label(frame)
        self.video_label.grid(row=0, column=0, rowspan=2)

        self.chat_display = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=15, width=80)
        self.chat_display.grid(row=0, column=1, pady=10, padx=10)
        self.chat_display.config(state=tk.DISABLED)

        self.query_input = tk.Entry(frame, width=80)
        self.query_input.grid(row=1, column=1, pady=10, padx=10)
        self.query_input.bind("<Return>", self.process_query)

    def update_image(self):
        ret, frame = self.cap.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb_frame)
            photo = ImageTk.PhotoImage(image=image)
            self.video_label.config(image=photo)
            self.video_label.image = photo

        self.after(30, self.update_image)

    def display_response(self, response):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\nBot: {response}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.yview(tk.END)
        
        threading.Thread(target=text_to_speech, args=(response,), daemon=True).start()

    def process_query(self, event=None):
        query = self.query_input.get()
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\nUser: {query}\n")
        self.chat_display.config(state=tk.DISABLED)

        def query_task():
            if "see" in query.lower():
                ret, frame = self.cap.read()
                if ret:
                    description = get_image_description(frame, query)
                    self.display_response(description)
            else:
                summary = get_text_summary(query)
                self.display_response(summary)

        threading.Thread(target=query_task, daemon=True).start()

        self.query_input.delete(0, tk.END)
        self.chat_display.yview(tk.END)

if __name__ == '__main__':
    window = ChatBotWindow()
    window.mainloop()

