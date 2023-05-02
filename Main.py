import customtkinter
import os
from PIL import Image
from cefpython3 import cefpython as cef
import requests
import scrape
import datetime
import vlc
from random import *
#from web_widget import *
import webbrowser
from threading import Thread

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Arc")
        self.geometry("800x350")

        self.browser_frame = None

        #character list for kantai 
        self.char_list = ['Верный','Warspite','Kawakaze','Yura','Ark_Royal']
        self.char_pos = 0
        self.kantai_is_start = False

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #check day of week and import anime list 
        self.day_of_week = datetime.date.today().weekday()+1
        self.anime_list = scrape.main()

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.char_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Characters")
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

        self.home_button_1 = customtkinter.CTkButton(self.home_frame, text="Start Kantai",
                                                     command = self.start_kantai)
        self.home_button_1.grid(row=2, column=0, padx=10, pady=10)

        self.home_button_2 = customtkinter.CTkButton(self.home_frame, text="Next Character",
                                                     command = self.change_char)
        self.home_button_2.grid(row=2, column=1, padx=10, pady=10) 

        self.home_buttons_frame = customtkinter.CTkScrollableFrame(self.home_frame, label_text="Anime List")
        self.home_buttons_frame.grid(row=0, column=2, rowspan=3,padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.home_buttons_frame.grid_columnconfigure(0, weight=1)
        thread1 = Thread(target = self.get_anime_list,args=())
        thread1.start()

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        
        
        
        
        

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # cef.Initialize()
        # self.browser_frame = BrowserFrame(self.third_frame)
        # self.browser_frame.grid(row=0, column=0)

        # select default frame
        self.select_frame_by_name("home")
        self.check_time()

    def change_char(self):
        if self.char_pos >= len(self.char_list)-1:
            self.char_pos-=len(self.char_list)-1
        else:
            self.char_pos+=1

        #get correct size of image to be a square   
        old_image = Image.open(os.path.join(self.char_path, self.get_cur_char()+".png" ))
        im_size = old_image.size
        if im_size[0]>im_size[1]:
            new_w = im_size[0]
            background = (new_w,new_w)
            location = (0,int((new_w-im_size[1])/2))
        else:
            new_h = im_size[1]
            background = (new_h,new_h)
            location = (int((new_h-im_size[0])/2),0)
        new_image = Image.new('RGBA', background, (0, 0, 0, 0))
        new_image.paste(old_image,location )

        #output image to update on home screen
        image_char = customtkinter.CTkImage(new_image, size=(200, 200))
        self.home_frame_large_image_label.configure(image=image_char)

        if self.kantai_is_start:
             self.play_sound("_Intro")
        else:
            pass
        
    def switch_back_char(self):
         #get correct size of image to be a square   
        old_image = Image.open(os.path.join(self.char_path, self.get_cur_char()+".png" ))
        im_size = old_image.size
        if im_size[0]>im_size[1]:
            new_w = im_size[0]
            background = (new_w,new_w)
            location = (0,int((new_w-im_size[1])/2))
        else:
            new_h = im_size[1]
            background = (new_h,new_h)
            location = (int((new_h-im_size[0])/2),0)
        new_image = Image.new('RGBA', background, (0, 0, 0, 0))
        new_image.paste(old_image,location )

        #output image to update on home screen
        image_char = customtkinter.CTkImage(new_image, size=(200, 200))
        self.home_frame_large_image_label.configure(image=image_char)

    #Start or shut down kantain clock
    def start_kantai(self):
        self.kantai_is_start = not self.kantai_is_start
        if self.kantai_is_start:
            sound_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Sounds")
            sound = vlc.MediaPlayer(os.path.join(sound_path, "TitleCallA" + str(randint(1, 20)) + ".mp3"))
            sound.play()
            self.switch_back_char()
        else:
            self.home_frame_large_image_label.configure(image=self.large_test_image)
        self.home_button_1.configure(text="Start Kantai" if self.kantai_is_start==False else "Close Kantai")

    #Get name of current character as string
    def get_cur_char(self):
        return  self.char_list[self.char_pos]
    
    #Play Sound
    def play_sound(self,keyword):
        sound_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Sounds")
        if self.kantai_is_start:
            sound = vlc.MediaPlayer(os.path.join(sound_path, self.get_cur_char() + str(keyword) + ".mp3"))
            sound.play()
        else:
            pass
    
    #Update Time based on current PC time on home screen        
    def check_time(self):
        self.clock_label.configure(text=datetime.datetime.now().replace(microsecond=0))
        current_time = datetime.datetime.now()
        self.clock_label.after(1000, self.check_time)
        if current_time.minute == 0 and current_time.second == 0:
            self.play_sound(str(current_time.hour))
            idle_times = [randint(5, 25),randint(35, 55)]
        else:
            pass
   

    #Open website on click for anime list
    def open_web(self,keyword):
        webbrowser.open_new("https://www.iyf.tv/search/"+keyword)

    #Get_img from URL
    def get_img(self,url,x=100,y =100):
        image = customtkinter.CTkImage(Image.open(requests.get(url, stream=True).raw), size=(x, y))
        return image
    
    def split_text(self,text):
        length = len(text)
        new_text ='\n'.join(text[i:i+10] for i in range(0, length, 10))
        return new_text
    
    #load anime frame into desired frame
    def load_anime_frame(self,frame):
        self.date_widget =dict()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.date_widget = self.list_to_widgets(days,frame,0)
        for day in range(1,8):
            list_anime = [sublist for sublist in self.anime_list if sublist[1] == day]
            thread3 = Thread(target = self.generate_anime_list,args=(list_anime,self.date_widget[day-1]))
            thread3.start()
    
    def list_to_widgets(self,list,frame,row):
        col = 0
        list_widget = dict()
        for elements in list:
            #initialize the buttons and connect callback function to open relative webpage. 
            list_widget[col]=customtkinter.CTkScrollableFrame(frame, label_text=elements)
            list_widget[col].grid(row=row+int(col/3), column=col%3, padx=20, pady=10)
            col +=1
        return list_widget
    

    def generate_anime_list(self,list,frame):
        count = 0
        self.list_buttons = dict()
        for elements in list:
            #initialize the buttons and connect callback function to open relative webpage. 
            self.list_buttons[count]=customtkinter.CTkButton(frame, text=self.split_text(elements[0]), 
                                                           image=self.get_img(elements[3]), compound="top",
                                                           command=lambda a = elements[0]: self.open_web(a ))
            self.list_buttons[count].grid(row=count, column=0, padx=20, pady=10)
            count +=1

    #genearate button list for anime of the day !!!! NEED TO chaneg to more general use
    def get_anime_list(self):
        count = 0
        self.anime_today = dict()
        for anime in self.anime_list:
            if self.day_of_week == anime[1]:
                #initialize the buttons and connect callback function to open relative webpage. 
                self.anime_today[count]=customtkinter.CTkButton(self.home_buttons_frame, text=self.split_text(anime[0]), 
                                                           image=self.get_img(anime[3]), compound="top",
                                                           command=lambda a = anime[0]: self.open_web(a ))
                self.anime_today[count].grid(row=count, column=0, padx=20, pady=10)
                count +=1
   
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
        self.geometry("800x350")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")
        self.geometry("1000x850")
        thread2 = Thread(target = self.load_anime_frame,args=(self.second_frame,))
        thread2.start()

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()