import customtkinter
import os
from PIL import Image
import webbrowser
import requests
from bs4 import BeautifulSoup
import scrape
import datetime
from threading import Thread
import psutil
import sys
import winreg
from anime_widget import anime_widget
import PIL.ImageOps    

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Arc")
        self.geometry("750x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        
        #check day of week and import anime list 
        self.day_of_week = datetime.date.today().weekday()
        self.anime_list = scrape.get_anime()
        self.frame_list = []
        self.tab_list = []

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(200, 200))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(100, 100))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.bg_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(200, 200))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        

    
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
        self.tab_list.append(self.home_button)

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Chat",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")
        self.tab_list.append(self.frame_2_button)

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Add person",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")
        self.tab_list.append(self.frame_3_button)

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=10, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.frame_list.append(self.home_frame)

        self.clock_label = customtkinter.CTkLabel(self.home_frame,font=("Courier New", 15,'bold'), text='')
        self.clock_label.grid(row=0, column=0,columnspan=2, padx=2, pady=10)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.bg_image)
        self.home_frame_large_image_label.grid(row=1, column=0,columnspan=2, padx=20, pady=10)
        self.home_button_1 = customtkinter.CTkButton(self.home_frame, text=" Open Browser ",command = lambda:self.open_web(web="https://www.google.com/"))
        self.home_button_1.grid(row=2, column=0, padx=10, pady=10)
        self.home_button_2 = customtkinter.CTkButton(self.home_frame, text="Place Holder Function ",command = lambda:self.open_web("tianguo"))
        self.home_button_2.grid(row=2, column=1, padx=10, pady=10) 

        self.home_sys_frame = customtkinter.CTkFrame(self.home_frame,fg_color=("gray80", "gray15"))
        self.home_sys_frame.grid(row=3, column=0,padx=(20, 0), pady=(20, 0), sticky="n")
        self.get_sys_frame()

        # self.home_buttons_frame = customtkinter.CTkScrollableFrame(self.home_frame, label_text="Anime List Today")
        # self.home_buttons_frame.grid(row=0, column=2, rowspan=2,padx=(20, 0), pady=(20, 0), sticky="nsew")
        # self.home_buttons_frame.grid_columnconfigure(0, weight=1)
        # thread1 = Thread(target = self.get_anime_list,args=())
        # thread1.start()
        recent_file,recent_files_path= self.check_recent_file()
        self.recent_file_widget(row=0, col=2,parent_frame=self.home_frame,file_list=recent_file,
                                path_list=recent_files_path,rowspan=3,columnspan =1 )
        
        self.home_weather_frame = customtkinter.CTkFrame(self.home_frame,fg_color=("gray80", "gray15"))
        self.home_weather_frame.grid(row=3, column=1,padx=(10, 10), pady=(20, 0), sticky="n")
        self.home_weather_label = customtkinter.CTkLabel(self.home_weather_frame,justify = 'right')
        self.home_weather_label.grid(padx=(20, 20), pady=(13, 13), sticky="w")

        self.anime_home = anime_widget()
        upcoming_anime = self.anime_home.home_widget_upcoming(parent_frame=self.home_frame,row=3,col=2)
        self.anime_frame = self.anime_home.anime_frame(parent_frame = self)
        
        anime_tab = self.anime_home.home_widget_tab(parent_frame = self.navigation_frame,anime_frame=self.anime_frame,row=4)
        anime_tab.configure(command=lambda:self.frame_4_button_event())
        self.tab_list.append(anime_tab)


        # create second frame 
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # self.home_frame_large_image_label = customtkinter.CTkLabel(self.second_frame, text="", image=self.large_test_image)
        # self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)
        # self.frame_2_button_4 = customtkinter.CTkButton(self.second_frame, text="CTkButton", image=self.image_icon_image, compound="right", anchor="center")
        # self.frame_2_button_4.grid(row=1, column=0, padx=20, pady=10)
        self.frame_list.append(self.second_frame)

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frame_list.append(self.third_frame)
        self.frame_list.append(self.anime_frame)

        # select default frame
        self.select_frame_by_num(0)
        self.check_time()
        self.weather()

    def weather(self):
        city = "weather"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        res = requests.get(
            f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        time = soup.select('#wob_dts')[0].getText().strip().split()[0]
        info = soup.select('#wob_dc')[0].getText().strip()
        weather = soup.select('#wob_tm')[0].getText().strip()
        weather_img ="http://"+soup.select('#wob_tci')[0].get('src').strip("//")
        humidity = soup.select('#wob_hm')[0].getText().strip()
        wind = soup.select('#wob_ws')[0].getText().strip()
        image = Image.open(requests.get(weather_img, stream=True).raw)
        image = customtkinter.CTkImage(image, size=(50, 50))
        self.home_weather_label.configure(text=time+"\n"+weather+"°C"+"\n"+humidity+"\n"+wind, image=image,compound="left")
        # print(time)
        # print(info)
        # print(weather+"°C")
        # print(weather_img)
        # print(humidity)
        # print(wind)
        self.home_weather_label.after(60000, self.weather)
        

    #Get System Information Widget setup.
    def get_sys_frame(self):
        self.CPU_label = customtkinter.CTkLabel(self.home_sys_frame, text="CPU : ")
        self.CPU_label.grid(row=0, column=0, padx=10)
        self.slider_cpu = customtkinter.CTkProgressBar(self.home_sys_frame, orientation="horizontal",width = 100)
        self.slider_cpu.grid(row=0, column=1,padx=(0,5))

        self.RAM_label = customtkinter.CTkLabel(self.home_sys_frame, text="RAM : ")
        self.RAM_label.grid(row=1, column=0, padx=10)
        self.slider_memory = customtkinter.CTkProgressBar(self.home_sys_frame, orientation="horizontal",width = 100)
        self.slider_memory.grid(row=1, column=1,padx=(0,5))

        self.DISK_label = customtkinter.CTkLabel(self.home_sys_frame, text="DISK : ")
        self.DISK_label.grid(row=2, column=0, padx=10)
        self.slider_disk = customtkinter.CTkProgressBar(self.home_sys_frame, orientation="horizontal",width = 100)
        self.slider_disk.grid(row=2, column=1,padx=(0,5))

    #Return the most recent 20 files (on WIN only)
    def check_recent_file(self):
        recent_files_dir = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Recent')
        # Get the list of recent files     
        recent_files_path = [os.path.join(recent_files_dir, f) for f in os.listdir(recent_files_dir)]
        recent_files_path = sorted(recent_files_path, key=os.path.getmtime, reverse=True)
        recent_files_path = recent_files_path[0:20]
        recent_files = [f.split('\\')[-1].strip(".lnk") for f in recent_files_path]
        return recent_files , recent_files_path
    
    #Method for generating recent file widget
    def recent_file_widget(self,row,col,parent_frame,file_list,path_list,rowspan,columnspan):
        main_frame = customtkinter.CTkScrollableFrame(parent_frame, label_text="Recent File",orientation="vertical",width=150,height=100)
        main_frame.grid(row=row, column=col,rowspan = rowspan,columnspan =1,padx=(20, 20), pady=(20, 20), sticky = 'ns')
        main_frame_list=dict()
        count = 0
        for element in file_list:
            main_frame_list[count]=customtkinter.CTkButton(main_frame, text=self.split_text(element,20), 
                                                            command=lambda a = path_list[count]: os.startfile(a))
            #main_frame_list[count].grid(row=count%10, column=0+int(count/10), padx=5, pady=5, sticky = 'w')
            main_frame_list[count].grid(row=count, column=0, padx=5, pady=5, sticky = 'w')
            count += 1
        return main_frame_list

    #Return the most recent 20 files (on WIN only)
    def check_sys(self):
        cpu = psutil.cpu_percent()
        disk = psutil.disk_usage('/').percent
        memory = psutil.virtual_memory().percent
        self.slider_cpu.set(cpu/100)
        self.slider_disk.set(disk/100)
        self.slider_memory.set(memory/100)
        self.tab_refresh()

    #Get System Information Widget update every 1 second with check_time.
    def check_time(self):
        self.clock_label.configure(text=datetime.datetime.now().replace(microsecond=0))
        current_time = datetime.datetime.now()
        self.thread2 = Thread(target = self.check_sys,args=())
        self.thread2.setDaemon(True)
        self.thread2.start()
        self.clock_label.after(1000, self.check_time)

    #Method for open web with either keyword or URL
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

    #rewrite default select_frame by name method
    def select_frame_by_num(self,num):
        self.tab_list[num].configure(fg_color=("gray75", "gray25"))
        count = 0
        for tabs in self.tab_list:
            if count != num:
                tabs.configure(fg_color="transparent")
            else:
                pass
            count+=1
        self.frame_list[num].grid(row=0, column=1, sticky="nsew")
        count = 0
        for frame in self.frame_list:
            if count != num:
                frame.grid_forget()
            else:
                pass
            count+=1

    def tab_refresh(self):
        self.anime_home.anime_refresh()

    def home_button_event(self):
        self.geometry("750x450")
        self.select_frame_by_num(0)

    def frame_2_button_event(self):
        self.select_frame_by_num(1)

    def frame_3_button_event(self):
        self.select_frame_by_num(2)
    
    def frame_4_button_event(self):
        self.geometry("1000x850")
        self.select_frame_by_num(3)

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
    sys.exit()
