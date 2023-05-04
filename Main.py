import customtkinter
import os
from PIL import Image
import webbrowser
import requests
import scrape
import datetime
from threading import Thread

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Arc")
        self.geometry("800x350")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #check day of week and import anime list 
        self.day_of_week = datetime.date.today().weekday()
        self.anime_list = scrape.get_anime()

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(200, 200))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(100, 100))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.holder_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "holder.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "holder.png")), size=(100, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        self.anime_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "anime.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "anime.png")), size=(100, 100))
    
        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Arc Demo", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Chat",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Add person",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.clock_label = customtkinter.CTkLabel(self.home_frame,font=("Courier New", 15,'bold'), text='')
        self.clock_label.grid(row=0, column=0,columnspan=2, padx=2, pady=10)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=1, column=0,columnspan=2, padx=20, pady=10)
        self.home_button_1 = customtkinter.CTkButton(self.home_frame, text=" Place Holder Function ")
        self.home_button_1.grid(row=2, column=0, padx=10, pady=10)
        self.home_button_2 = customtkinter.CTkButton(self.home_frame, text="Place Holder Function ",command = lambda:self.open_web("tianguo"))
        self.home_button_2.grid(row=2, column=1, padx=10, pady=10) 

        self.home_buttons_frame = customtkinter.CTkScrollableFrame(self.home_frame, label_text="Anime List Today")
        self.home_buttons_frame.grid(row=0, column=2, rowspan=2,padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.home_buttons_frame.grid_columnconfigure(0, weight=1)
        thread1 = Thread(target = self.get_anime_list,args=())
        thread1.start()


        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame_large_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)
        self.frame_2_button_4 = customtkinter.CTkButton(self.second_frame, text="CTkButton", image=self.image_icon_image, compound="right", anchor="center")
        self.frame_2_button_4.grid(row=1, column=0, padx=20, pady=10)


        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")


        # select default frame
        self.select_frame_by_name("home")
        self.check_time()

    def check_time(self):
        self.clock_label.configure(text=datetime.datetime.now().replace(microsecond=0))
        current_time = datetime.datetime.now()
        self.clock_label.after(1000, self.check_time)

    def open_web(self,keyword):
        webbrowser.open_new("https://www.iyf.tv/search/"+keyword)

    def get_img(self, url, x = 100, y = 100):
        image = customtkinter.CTkImage(Image.open(requests.get(url, stream=True).raw), size=(x, y))
        return image
    
    #genearate button list for anime of the day
    def get_anime_list(self):
        count = 0
        self.anime_today = dict()
        for anime in self.anime_list:
            if self.day_of_week == anime[1]:
                #initialize the buttons and connect callback function to open relative webpage. 
                self.anime_today[count]=customtkinter.CTkButton(self.home_buttons_frame, text=anime[0] + '\n' + anime[2], 
                                                            image=self.get_img(anime[3]), compound="top",
                                                            command=lambda a = anime[0]: self.open_web(a))
                self.anime_today[count].grid(row=count, column=0, padx=20, pady=20)
                count += 1
    

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()