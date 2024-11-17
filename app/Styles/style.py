from app.Config import config
from PIL import Image, ImageTk
import customtkinter as ctk
import time

def font_style(font_style='Segoe UI Emoji', size=16, style='bold'):
    return (font_style, size, style)

def fade_in(window):
    alpha = window.attributes('-alpha')
    if alpha < 1:
        alpha += 0.15
        window.attributes('-alpha', alpha)
        window.after(50, fade_in, window)

def fade_out(window):
    alpha = window.attributes('-alpha')
    if alpha > 0:
        alpha -= 0.25
        window.attributes('-alpha', alpha)
        window.after(50, fade_out, window)
    else:
        window.destroy() 

def on_closing(self):
    fade_out(self)

def load_gif(path):
    img = Image.open(path)
    frames = []
    for i in range(img.n_frames):
        img.seek(i)
        frame = ctk.CTkImage(light_image=img.copy(), size=(img.width, img.height))
        frames.append(frame)
    return frames