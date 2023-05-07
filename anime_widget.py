import customtkinter
import os
from PIL import Image
import scrape
import datetime
import webbrowser
import requests
from threading import Thread

class anime_widget():
    def __init__(self):
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.playlist_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "playlist_light.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "playlist_dark.png")), size=(20, 20))
        self.anime_list = scrape.get_anime()
        self.day_of_week = datetime.date.today().weekday()
        self.anime_next = self.upcoming_anime()

    def open_web(self,keyword='',web=''):
        if web=='':
            webbrowser.open_new("https://www.iyf.tv/search/"+keyword)
        else:
            webbrowser.open_new(web)

    def split_text(self,text,width):
        length = len(text)
        new_text ='\n'.join(text[i:i+width] for i in range(0, length, width))
        return new_text

    #Method for generate CTKImage from URL 
    def get_img(self, url, x = 100, y = 100):
        image = customtkinter.CTkImage(Image.open(requests.get(url, stream=True).raw), size=(x, y))
        return image
    
    def load_anime_frame(self,frame):
        self.date_widget =dict()
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.date_widget = self.list_to_widgets(days,frame,0)
        for day in range(0,7):
            list_anime = [sublist for sublist in self.anime_list if sublist[1] == day]
            thread3 = Thread(target = self.generate_anime_list,args=(list_anime,self.date_widget[day]))
            thread3.start()
    
    #generate a list of widgets and output as a dictionary
    def list_to_widgets(self,list,frame,row):
        col = 0
        list_widget = dict()
        for elements in list:
            #initialize the buttons and connect callback function to open relative webpage. 
            list_widget[col]=customtkinter.CTkScrollableFrame(frame, label_text=elements)
            list_widget[col].grid(row=row+int(col/3), column=col%3, padx=20, pady=10)
            col +=1
        return list_widget
    
    #generate a list of widgets in given tk frame by name from given list [name, day, time, img]
    def generate_anime_list(self,list,frame):
        count = 0
        self.list_buttons = dict()
        for elements in list:
            #initialize the buttons and connect callback function to open relative webpage. 
            self.list_buttons[count]=customtkinter.CTkButton(frame, text=self.split_text(elements[0],10)+ '\n' + elements[2], 
                                                           image=self.get_img(elements[3]), compound="top",
                                                           command=lambda a = elements[0]: self.open_web(a ))
            self.list_buttons[count].grid(row=count, column=0, padx=20, pady=10)
            count +=1
    
    def upcoming_anime(self):
        current_time = datetime.datetime.now()
        anime_today = [anime for anime in self.anime_list if anime[1] == self.day_of_week]
        anime_tmr = [anime for anime in self.anime_list if anime[1] == (self.day_of_week+1)%7]
        for anime in anime_today:
            if int(anime[2].split(':')[0]) > current_time.hour: 
                return anime
            elif int(anime[2].split(':')[0]) == current_time.hour:
                if int(anime[2].split(':')[1]) >= current_time.minute: 
                    return anime
        return anime_tmr[0]
    
    def home_widget_upcoming(self,parent_frame,row,col):
        upcoming_anime_btn = customtkinter.CTkButton(parent_frame, text="Upcoming :\n"+self.anime_next[0],image=self.get_img(self.anime_next[3]),
                                                     command = lambda:self.open_web(self.anime_next[0]))
        upcoming_anime_btn.grid(row=row, column=col, padx=10, pady=10,sticky = 'w') 
        return upcoming_anime_btn
    
    def anime_frame(self,parent_frame):
        self.master_frame = parent_frame
        anime_frame = customtkinter.CTkFrame(parent_frame, corner_radius=0, fg_color="transparent")
        self.load_anime_frame(anime_frame)
        return anime_frame
    
#USELESS
    def select_frame(self,parent_frame,parent_btn):
        #parent_btn.configure(fg_color=("gray75", "gray25"))
        #parent_frame.grid(row=0, column=1, sticky="nsew")
        self.master_frame.geometry("1000x850")
        #parent_btn.configure(fg_color="transparent")
        self.load_anime_frame(parent_frame)
#USELESS
        
    def home_widget_tab(self,parent_frame,anime_frame,row):
        
        anime_frame_button = customtkinter.CTkButton(parent_frame, corner_radius=0, height=40, border_spacing=10, text="Anime",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.playlist_image, anchor="w")
        #anime_frame_button.configure(command=lambda a=anime_frame,b =anime_frame_button:self.select_frame(a,b))
        anime_frame_button.grid(row=row, column=0, sticky="new")

        return anime_frame_button
