import customtkinter 
from PIL import Image
import tkinter as tk

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("valera")
        self.geometry("1000x320")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)


        self.checkbox_frame = customtkinter.CTkFrame(master=self, height=50)
        self.checkbox_frame.grid(row=0, column=0, padx=10, pady=(40, 0), sticky="new")
        
        self.checkbox_frame2 = customtkinter.CTkFrame(master=self, height=50)
        self.checkbox_frame2.grid(row=0, column=0, padx=10, pady=(150, 0), sticky="new")
        
        self.checkbox_frame3 = customtkinter.CTkFrame(master=self, height=100)
        self.checkbox_frame3.grid(row=0, column=0, padx=10, pady=(260, 0), sticky="new")


        self.title = customtkinter.CTkLabel(self, text="Activation Word", fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="enw")

        self.title2 = customtkinter.CTkLabel(self, text="Add Command", fg_color="gray30", corner_radius=6)
        self.title2.grid(row=0, column=0, padx=10, pady=(120, 0), sticky="enw")

        self.title3 = customtkinter.CTkLabel(self, text="Enter your ref/way here", fg_color="gray30", corner_radius=6)
        self.title3.grid(row=0, column=0, padx=10, pady=(230, 0), sticky="enw")
        
        
        self.textbox = customtkinter.CTkTextbox(master=self.checkbox_frame, width=650,height=25)
        self.textbox.grid(row=0, column=0,padx=10, sticky="e")
        self.textbox.insert("0.0", text="Vadik")
        self.textbox.configure(state= "disabled")

        self.textbox2 = customtkinter.CTkTextbox(master=self.checkbox_frame2, width=470,height=25)
        self.textbox2.grid(row=0, column=1,padx=10, sticky="e")
        self.textbox2.insert("0.0", text="                                                                Add Command ->")
        self.textbox2.configure(state= "disabled")

        self.text3 = customtkinter.CTkTextbox(self.checkbox_frame3, width=960, height=25)
        self.text3.grid(row=0, column=0, padx=10, pady=10, sticky="n")


        self.button = customtkinter.CTkButton(self.checkbox_frame, text="play",command=self.button_callback)
        self.button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.button2 = customtkinter.CTkButton(self.checkbox_frame, text="save", command=self.button_callback)
        self.button2.grid(row=0, column=2, padx=0, pady=0, sticky="e")

        self.button = customtkinter.CTkButton(self.checkbox_frame2, text="play",command=self.button_callback)
        self.button.grid(row=0, column=3, padx=10, pady=10, sticky="e")

        self.button2 = customtkinter.CTkButton(self.checkbox_frame2, text="save", command=self.button_callback)
        self.button2.grid(row=0, column=4, padx=0, pady=0, sticky="e")

        
        self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(self.checkbox_frame2, values=["открыть сайт", "хуй знает че еще", "хуй знает че еще х2"],width=160)
        self.appearance_mode_option_menu.grid(row=0, column=0, columnspan=1,padx=10, pady=(10, 10))
        self.appearance_mode_option_menu.set("Select")


    def button_callback(self):
        print("button pressed")

if __name__ == "__main__":
    app = App()
    app.mainloop()
