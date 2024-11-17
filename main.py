import customtkinter as ctk
from app.Gui.CTKgigachat import Application
from app.Config import config

if __name__ == '__main__':
    try:
        ctk.set_default_color_theme('green')
        ctk.set_appearance_mode('Dark')

        app = Application()
        app.mainloop()
    except KeyboardInterrupt:
        pass