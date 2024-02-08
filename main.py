import customtkinter 
from PIL import Image
import tkinter as tk
import pandas as pd
import pyaudio
import psutil
import easygui
import webrtcvad
import json
import os
from vosk import Model, KaldiRecognizer
import threading
import queue
import ctypes
import webbrowser
import platform
import time
from PyQt5.QtWidgets import QTextEdit, QLabel, QDialog, QApplication, QVBoxLayout, QGroupBox, QHBoxLayout, \
    QPushButton, QComboBox
from PyQt5.QtGui import QIcon
from sys import argv, exit
import warnings
from keyboard import is_pressed
from playsound import playsound
from random import randint

warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.Label = customtkinter.CTkLabel(self, text="ToplevelWindow")
        self.Label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="enw")

class App(customtkinter.CTk):

    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    hWnd = kernel32.GetConsoleWindow()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("valera")
        self.geometry("1000x600")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.data = pd.DataFrame()
        with open('data.csv', encoding='utf-8') as file:
            self.data = pd.read_csv(file)

        self.activation_word = list((self.data.loc[self.data['type'] == 'activation']['command']))[0]

        self.button_image_play = customtkinter.CTkImage(Image.open("icons\play.png"), size=(20, 20))
        self.button_image_pause = customtkinter.CTkImage(Image.open("icons\pause.png"), size=(20, 20))
        self.button_image_save = customtkinter.CTkImage(Image.open("icons\save.png"), size=(20, 20))

        self.checkbox_frame = customtkinter.CTkFrame(master=self, height=50)
        self.checkbox_frame.grid(row=0, column=0, padx=10, pady=(40, 0), sticky="new")
        
        self.checkbox_frame2 = customtkinter.CTkFrame(master=self, height=50)
        self.checkbox_frame2.grid(row=0, column=0, padx=10, pady=(150, 0), sticky="new")
        
        self.checkbox_frame3 = customtkinter.CTkFrame(master=self, height=100)
        self.checkbox_frame3.grid(row=0, column=0, padx=10, pady=(370, 0), sticky="new")

        self.checkbox_frame4 = customtkinter.CTkFrame(master=self, height=100)
        self.checkbox_frame4.grid(row=0, column=0, padx=10, pady=(260, 0), sticky="new")

        self.checkbox_frame5 = customtkinter.CTkFrame(master=self, height=100)
        self.checkbox_frame5.grid(row=0, column=0, padx=10, pady=(480, 0), sticky="new")

        self.title = customtkinter.CTkLabel(self, text="Activation Word", fg_color="black", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="enw")

        self.title2 = customtkinter.CTkLabel(self, text="Add Command", fg_color="black", corner_radius=6)
        self.title2.grid(row=0, column=0, padx=10, pady=(120, 0), sticky="enw")

        self.title3 = customtkinter.CTkLabel(self, text="Or enter your ref/way here", fg_color="black", corner_radius=6)
        self.title3.grid(row=0, column=0, padx=10, pady=(340, 0), sticky="enw")

        self.title4 = customtkinter.CTkLabel(self, text="Choose manually", fg_color="black", corner_radius=6)
        self.title4.grid(row=0, column=0, padx=10, pady=(230, 0), sticky="enw")
        
        self.textbox = customtkinter.CTkTextbox(master=self.checkbox_frame, width=650,height=25)
        self.textbox.grid(row=0, column=0,padx=10, sticky="e")
        self.textbox.insert("0.0", text=self.activation_word)
        self.textbox.configure(state= "disabled")

        self.textbox2 = customtkinter.CTkTextbox(master=self.checkbox_frame2, width=470,height=25)
        self.textbox2.grid(row=0, column=1,padx=10, sticky="e")
        self.textbox2.insert("0.0", text="                                                                Add Command ->")
        self.textbox2.configure(state= "disabled")

        self.textbox3 = customtkinter.CTkTextbox(master=self.checkbox_frame4, width=150,height=25)
        self.textbox3.grid(row=0, column=0,padx=10, sticky="e")
        self.textbox3.insert("0.0", text="Type here")

        self.text3 = customtkinter.CTkTextbox(self.checkbox_frame3, width=960, height=25)
        self.text3.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        self.button = customtkinter.CTkButton(self.checkbox_frame, fg_color="yellow", text="",image=self.button_image_play,command=self.activation_settings)
        self.button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.button2 = customtkinter.CTkButton(self.checkbox_frame, fg_color="yellow", text="",image=self.button_image_save, command=self.save_activation_word)
        self.button2.grid(row=0, column=2, padx=0, pady=0, sticky="e")

        self.button3 = customtkinter.CTkButton(self.checkbox_frame2,fg_color="yellow",  text="",image=self.button_image_play, command=self.command_settings)
        self.button3.grid(row=0, column=3, padx=10, pady=10, sticky="e")

        self.button4 = customtkinter.CTkButton(self.checkbox_frame2,fg_color="yellow",  text="",image=self.button_image_save, command=self.save_command)
        self.button4.grid(row=0, column=4, padx=0, pady=0, sticky="e")

        self.button5 = customtkinter.CTkButton(self.checkbox_frame4,fg_color="yellow", text="Find", command=self.update_programs_lst)  #  ",image=self.button_image_save,")
        self.button5.grid(row=0, column=1, padx=0, pady=0, sticky="e")

        self.button6 = customtkinter.CTkButton(self.checkbox_frame4,fg_color="yellow", text="...",text_color='#228', width=20, command=self.open_explorer_and_select_exe)
        self.button6.grid(row=0, column=5, padx=0, pady=0, sticky="e")

        self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(self.checkbox_frame2,text_color='#228', fg_color="yellow",button_color="yellow", button_hover_color="blue", dropdown_hover_color="blue", values=["open site", "open app"],width=160)
        self.appearance_mode_option_menu.grid(row=0, column=0, columnspan=1,padx=10, pady=(10, 10))
        self.appearance_mode_option_menu.set("Select")

        self.programs = self.get_sorted_names()

        self.appearance_mode_option_menu2 = customtkinter.CTkOptionMenu(self.checkbox_frame4,text_color='#228',fg_color="yellow",button_color="yellow",button_hover_color="blue", dropdown_hover_color="blue", values=self.programs,width=300)
        self.appearance_mode_option_menu2.grid(row=0, column=2, columnspan=1,padx=10, pady=(10, 10))
        self.appearance_mode_option_menu2.set("Select")

        self.hello_phrases = ['audio\\doing.mp3', 'audio\\doing2.mp3', 'audio\\doing3.mp3']
        self.gb_phrases = ['audio\\gb.mp3', 'audio\\gb2.mp3']

        actions = ['открыть сайт', 'открыть приложение']

        #self.play_icon = QIcon('icons\\play.png')
        #self.stop_icon = QIcon('icons\\pause.png')
        #save_icon = QIcon('icons\\save.png')
        self.settings_activation_record = False
        self.settings_command_record = False

        #main_layout = QVBoxLayout()

        self.temp_activation_word = self.activation_word

        #activation_group_box = QGroupBox('Activation Word')  # изменение активации
        #activation_layout = QHBoxLayout()

        self.button_1 = customtkinter.CTkButton(self.checkbox_frame5, text="open toplevel", command=self.open_toplevel)
        self.button_1.grid(row=0, column=0, padx=0, pady=0, sticky="e")

        self.toplevel_window = None

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    @staticmethod
    def hide_console():
        App.user32.ShowWindow(App.hWnd, 0)

    @staticmethod
    def show_console():
        App.user32.ShowWindow(App.hWnd, 5)

    @staticmethod
    def audio_capture(stream, frame_size, vad, audio_queue):
        while True:
            frames = [stream.read(frame_size, exception_on_overflow=False) for _ in
                      range(5)]  # Уменьшаем количество фреймов
            audio_queue.put(b''.join(frames))

    @staticmethod
    def open_url(url):
        if platform.system() == "Windows":
            os.system(f"start {url}")
        elif platform.system() == "Darwin":
            os.system(f"open {url}")
        elif platform.system() == "Linux":
            os.system(f"xdg-open {url}")
        else:
            print("Неизвестная операционная система")

    def process_open_site_command(self, command):

        for i, row in self.data.iterrows():
            site_name = row.command
            site_url = row.url
            site_type = row.type
            if site_name in command and site_type == 'site':
                print(f"Попытка открыть сайт {site_name}")
                try:
                    self.open_url(site_url)
                    print(f"Сайт {site_name} открыт")

                    self.random_greets_answer()
                except Exception as e:
                    print(f"Ошибка при открытии сайта {site_name}: {e}")
                return True

        print("Название сайта не распознано")
        return False

    def process_open_app_command(self, command):

        for i, row in self.data.iterrows():
            app_name = row.command
            app_path = row.url
            app_type = row.type
            if app_name in command and app_type == 'app':
                print(f"Попытка открыть приложение {app_name}")
                try:
                    os.startfile(app_path)
                    print(f"Приложение {app_name} открыто")

                    self.random_greets_answer()
                except Exception as e:
                    print(f"Ошибка при открытии приложения {app_name}: {e}")
                return True

        print("Название приложения не распознано")
        return False

    def command_recognition(self, recognizer, audio_queue):
        console_hidden = False
        waiting_for_keyword = True
        partial_result = ''

        while True:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result_json = recognizer.Result()
                result = json.loads(result_json)
                command = result['text']

                if self.settings_activation_record:
                    self.temp_activation_word = command
                    self.textbox.configure(state= "normal")
                    self.textbox.delete('0.0', '100.0')
                    self.textbox.insert("0.0", text=command)
                    self.textbox.configure(state= "disabled")

                if self.settings_command_record:
                    self.textbox2.configure(state= "normal")
                    self.textbox2.delete('0.0','100.0')
                    self.textbox2.insert('0.0', text=command)
                    self.textbox2.configure(state= "disabled")

                if waiting_for_keyword and self.activation_word in command:
                    print("Ключевое слово распознано, ожидаю команду...")
                    playsound('audio\\listen.mp3')
                    waiting_for_keyword = False
                    if console_hidden:
                        self.show_console()
                        console_hidden = False
                    partial_result = ''
                    continue

                if waiting_for_keyword:
                    continue

                print(f"Распознанная команда: {command}")

                if "открой сайт" in command and self.process_open_site_command(command):
                    partial_result = ''

                elif "открой приложение" in command and self.process_open_app_command(command):
                    partial_result = ''

                elif "хайд" in command:
                    print("Выполняю команду 'Скройся'")
                    self.hide_console()
                    waiting_for_keyword = True
                    console_hidden = True
                    partial_result = ''

                elif "стоп" in command:
                    print(f"Ожидаю команду '{self.activation_word}' для активации")
                    waiting_for_keyword = True
                    self.random_gb_answer()
                    partial_result = ''

                elif "консоль" in command:
                    print("Открываю консоль...")
                    os.system("start cmd")

                elif "добавь сайт" in command:
                    request = command.replace('добавь сайт', '')
                    print(request)

                partial_result = ''

            else:
                partial_result += recognizer.PartialResult()

    def listen_for_commands(self, model_path, interface):
        vad = webrtcvad.Vad(1)

        model = Model(model_path)
        recognizer = KaldiRecognizer(model, 16000)

        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=320)
        stream.start_stream()

        frame_duration_ms = 20
        frame_size = int(16000 * frame_duration_ms / 1000)

        audio_queue = queue.Queue()

        threading.Thread(target=self.audio_capture, args=(stream, frame_size, vad, audio_queue), daemon=True).start()
        threading.Thread(target=self.command_recognition, args=(recognizer, audio_queue), daemon=True).start()

        print("Слушаю...")

        while True:
            exit(interface.mainloop())
            if is_pressed('ctrl') and is_pressed('shift') and is_pressed('h'):
                pass
                

    def activation_settings(self):
        self.settings_activation_record = not self.settings_activation_record

        if self.settings_activation_record:
            self.button.configure(image=self.button_image_pause)
        else:
            self.button.configure(image=self.button_image_play)

        print("1")

    def save_activation_word(self):
        print("2")
        self.activation_word = self.temp_activation_word
        self.data.loc[0]['command'] = self.activation_word
        self.save_data()

    def command_settings(self):
        print("3")
        self.settings_command_record = not self.settings_command_record

        if self.settings_command_record:
            self.button3.configure(image=self.button_image_pause)
        else:
            self.button3.configure(image=self.button_image_play)


    def save_command(self):
        print("4")
        typo = ''
        if self.appearance_mode_option_menu.get() == 'open site':
            typo = 'site'
        elif self.appearance_mode_option_menu.get() == 'open app':
            typo = 'app'
        self.data.loc[len(self.data.index)] = [typo, self.textbox2.get(1.0, "end-1c"),
                                               self.text3.get(1.0, "end-1c")]
        self.save_data()

    @staticmethod
    def update_installed_programs():
        installed_programs = {}

        # Проходим по всем процессам
        for proc in psutil.process_iter(['name', 'exe']):
            try:
                # Получаем имя процесса и путь к исполняемому файлу
                process_name = proc.info['name']
                process_exe = proc.info['exe']

                # Добавляем в словарь только те программы, у которых есть имя и путь к исполняемому файлу
                if process_name and process_exe:
                    installed_programs[process_name] = process_exe
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass

        return installed_programs
    
    def get_sorted_names(self) -> list:
        lst = list(self.update_installed_programs().keys())
        for num, app in enumerate(lst):
            temp_len = len(app)
            lst[num] = app[:temp_len - 4].lower()
        lst.sort()
        return lst
    
    def update_programs_lst(self):
        temp = self.textbox3.get(1.0, "end-1c").lower()
        self.programs = []
        for app in list(self.update_installed_programs().keys()):
            if temp in app.lower():
                temp_len = len(app)
                self.programs.append(app[:temp_len - 4].lower())
        if len(self.programs) == 0:
            self.programs.append('poshel nahuy')
        self.programs.sort()
        self.appearance_mode_option_menu2.configure(values=self.programs)
        

    def random_greets_answer(self):
        phrase = randint(0, 2)
        playsound(self.hello_phrases[phrase])

    def random_gb_answer(self):
        phrase = randint(0, 1)
        playsound(self.gb_phrases[phrase])

    def save_data(self):
        self.data.to_csv('data.csv', encoding='utf-8', index=False)
    
    def button_callback(self):
        print("button pressed")
    
    def open_explorer_and_select_exe(self):
        # Открываем диалоговое окно выбора файла
        file_path = easygui.fileopenbox(msg="Выберите .exe файл", filetypes=["*.exe"])

        if file_path:
            try:
                self.text3.delete('0.0','100.0')
                self.text3.insert('0.0', file_path)
            except FileNotFoundError:
                easygui.msgbox("Произошла ошибка при попытке открыть проводник.")
    
if __name__ == "__main__":
    mod_path = f"{os.path.dirname(os.path.realpath(__file__))}\\vosk-model-small-ru-0.22"
    app = QApplication(argv)
    window = App()
    window.listen_for_commands(mod_path, window)