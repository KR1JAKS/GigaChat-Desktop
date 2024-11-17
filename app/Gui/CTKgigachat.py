import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image
from app.Gigachat_Connect.ai import chat_ai
from app.Styles.style import on_closing, fade_in, font_style, load_gif
from app.Config import config
import threading
import emoji
import winsound
import time

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Gigachat_CTk')
        self.iconbitmap('app\\Resources\\Img\\icon.ico')
        self.geometry('400x300+%d+%d' % (
            (self.winfo_screenwidth() - 400) // 2,
            (self.winfo_screenheight() - 300) // 2
        ))
        self.attributes('-alpha', 0)
        self.after(100, fade_in, self)
        self.protocol('WM_DELETE_WINDOW', lambda: on_closing(self))
        self.resizable(0, 0)

        path='app\\Resources\\load_screen\\loading.gif'

        self.loading_label = ctk.CTkLabel(self,
                                          text='')
        self.loading_label.pack(fill='both', expand=True)
        self.frames = load_gif(path)
        self.current_frame = 0

        self.loading_screen()

    def startup_thread(self):
        self.startup()
        self.play_startup_song()

    def play_startup_song(self):
        winsound.PlaySound('app\\Resources\\Sounds\\startup.wav', winsound.SND_FILENAME)

    def startup(self):
        self.loading_label.destroy()

        self.geometry('980x500+%d+%d' % (
            (self.winfo_screenwidth() - 980) // 2,
            (self.winfo_screenheight() - 500) // 2
        ))
        self.resizable(1, 1)

        self.text_canvas = ctk.CTkCanvas(self,
                                         bd=0,
                                         width=800,
                                         height=500,
                                         bg=self.cget('bg'),
                                         highlightthickness=0)
        self.text_canvas.place(relx=0.5, rely=0.5, anchor='center')
        text = self.text_canvas.create_text(self.text_canvas.winfo_reqwidth() / 2,
                                     self.text_canvas.winfo_reqheight() / 2,
                                     text='',
                                     anchor='center',
                                     fill='white',
                                     font=font_style(size=52))
        
        full_text = 'Добро пожаловать!'

        delta = 100
        delay = 0

        for i in range(len(full_text) + 1):
            symbol = full_text[:i]
            add_symbol = lambda symbol=symbol: self.text_canvas.itemconfigure(text, 
                                                                              text=symbol)
            self.text_canvas.after(delay, add_symbol)
            delay += delta
        
        self.after(3500, self.set_ui)

    def set_ui(self):
        self.text_canvas.destroy()

        self.settings_frame = ctk.CTkFrame(self, corner_radius=0)
        self.settings_frame.place(relx=0, rely=0, anchor='nw', relheight=1, relwidth=0.15)

        self.settings_frame.grid_columnconfigure(0, weight=1)
        self.settings_frame.grid_columnconfigure(1, weight=1)
        self.settings_frame.grid_columnconfigure(2, weight=1)

        self.setting_label = ctk.CTkLabel(self.settings_frame,
                                           text='Меню',
                                           text_color='#FFFFFF',
                                           font=font_style(size=25))
        self.setting_label.grid(row=0, column=1, padx=(5, 5), pady=(5, 10), sticky='n')

        self.line_label = ctk.CTkCanvas(self.settings_frame,
                                         height=0,
                                         highlightthickness=1,
                                         bg='#FFFFFF')
        self.line_label.create_line(0, 0, 1, 0)
        self.line_label.grid(row=0, column=1, pady=(5, 5), sticky='s')

        self.clear_btn = ctk.CTkButton(self.settings_frame,
                                        text='Очистка',
                                        image=ctk.CTkImage(Image.open('app\\Resources\\Img\\bin.png'), 
                                                            size=(30, 30)),
                                        text_color='#FFFFFF',
                                        font=font_style(),
                                        hover_color='#FF0000',
                                        command=self.clear)
        self.clear_btn.grid(row=2, column=1, padx=(5, 5), pady=(5, 5), sticky='nsew')

        self.info_btn = ctk.CTkButton(self.settings_frame,
                                        text='Справка',
                                        text_color='#FFFFFF',
                                        image=ctk.CTkImage(Image.open('app\\Resources\\Img\\book.png'), 
                                                            size=(30, 30)),
                                        font=font_style(),
                                        command=self.show_info)
        self.info_btn.grid(row=1, column=1, padx=(5, 5), pady=(25, 5), sticky='nsew')

        self.body = ctk.CTkFrame(self)
        self.body.place(relx=0.5, rely=0.5, anchor='center')

        self.frames = load_gif("app\\Resources\\Logo.gif")

        self.prompt_label = ctk.CTkLabel(self.body, 
                                         text='',
                                         image=self.frames[0])
        self.prompt_label.grid(row=0, column=0, padx=(5, 5), sticky='nsew')

        self.current_frame = 0
        self.play_gif()

        self.line = ctk.CTkCanvas(self.body,
                                  height=0,
                                  highlightthickness=1,
                                  bg='#FFFFFF')
        self.line.create_line(0, 0, 1, 0)
        self.line.grid(row=1, column=0, pady=(5, 5), sticky='nsew')

        self.question_entry = ctk.CTkTextbox(self.body, 
                                             width=490, 
                                             height=50,
                                             text_color='lime',
                                             font=font_style(),
                                             wrap='word')
        
        self.placeholder_text = "Введите ваш вопрос здесь..."
        self.question_entry.insert("1.0", self.placeholder_text)
        self.question_entry.bind("<FocusIn>", self.on_focus_in)
        self.question_entry.bind("<FocusOut>", self.on_focus_out)
        self.question_entry.bind("<Control-v>", self.paste_text)
        self.question_entry.bind("<Control-V>", self.paste_text)

        self.question_entry.grid(row=3, column=0, padx=(5, 5), pady=(5, 5), sticky='swn')
        
        self.answer_text = ctk.CTkTextbox(self.body, 
                                          width=600, 
                                          height=300,
                                          border_width=2,
                                          state=ctk.DISABLED,
                                          text_color='white',
                                          fg_color='black',
                                          border_color='white',
                                          font=font_style(size=16, style='normal'),
                                          wrap='word')
        self.answer_text.grid(row=2, column=0, padx=(5, 5), pady=(5, 5), sticky='nsew')

        self.send_button = ctk.CTkButton(self.body, 
                                         text='',
                                         width=100,
                                         image=ctk.CTkImage(Image.open('app\\Resources\\Img\\Send_request.png'), 
                                                            size=(30, 30)),
                                         command=self.send_question)
        self.send_button.grid(row=3, column=0, padx=(5, 5), pady=(5, 5), sticky='nes')

    def click_sound(self):
        winsound.PlaySound('app\\Resources\\Sounds\\click.wav', winsound.SND_FILENAME)

    def on_focus_in(self, event):
        current_text = self.question_entry.get("1.0", "end-1c")
        if current_text == self.placeholder_text:
            self.question_entry.delete("1.0", "end")

    def on_focus_out(self, event):
        current_text = self.question_entry.get("1.0", "end-1c")
        if current_text.strip() == '':
            self.question_entry.insert("1.0", self.placeholder_text)

    def paste_text(self, event):
            clipboard_content = self.clipboard_get()
            if clipboard_content:
                self.question_entry.insert(ctk.END, clipboard_content)
            return "break"

    def send_question(self):
        threading.Thread(target=self.process_question).start()

    def process_question(self):
        threading.Thread(target=self.click_sound).start()

        question = self.question_entry.get("1.0", ctk.END).strip()
        
        if question.lower() == 'exit':
            self.destroy()
        else:

            current_time = time.strftime('%H:%M:%S')
        
            answer = chat_ai(question)

            self.answer_text.tag_config('bold', 
                                        foreground='black', 
                                        background='orange', 
                                        justify=ctk.LEFT)
            
            self.answer_text.tag_config('color1', 
                                        foreground='lime', 
                                        background='orange', 
                                        justify=ctk.LEFT)
            
            self.answer_text.tag_config('color2', 
                                        foreground='cyan', 
                                        background='orange', 
                                        justify=ctk.LEFT)
            self.answer_text.configure(state='normal')

            emodji = emoji.emojize(':bust_in_silhouette:')
            emodji2 = emoji.emojize(':alien_monster:')

            self.answer_text.insert(ctk.END, f'[{current_time}] {emodji}', 'color1')
            self.answer_text.insert(ctk.END, f' Вопрос: \n', 'bold')
            self.answer_text.insert(ctk.END, f'{question} \n\n')
            self.answer_text.insert(ctk.END, f'[{current_time}] {emodji2}', 'color2')
            self.answer_text.insert(ctk.END, f' Ответ: \n', 'bold')
            self.answer_text.insert(ctk.END, f'{answer} \n\n')

            self.answer_text.configure(state='disabled')

        self.question_entry.delete('1.0', ctk.END)
        self.question_entry.focus()

    def clear(self):
        threading.Thread(target=self.click_sound).start()
        self.answer_text.configure(state='normal')
        self.answer_text.delete('1.0', ctk.END)
        self.answer_text.configure(state='disabled')

    def show_info(self):
        threading.Thread(target=self.click_sound).start()
        self.message = CTkMessagebox(self, title='Справка', 
                      message="""Дескоптный GigaChat - v0.0.1.\nНеобходим доступ в интернет!""",
                      option_1='ОК')
        response = self.message.get()
        if response == 'ОК':
            threading.Thread(target=self.click_sound).start()

    def play_gif(self):
        self.prompt_label.configure(image=self.frames[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.after(100, self.play_gif)

    def loading_screen(self):
        self.loading_label.configure(image=self.frames[self.current_frame])
        self.current_frame += 1

        if self.current_frame < len(self.frames):
            self.after(15, self.loading_screen)
        else:
            threading.Thread(target=self.startup_thread).start()