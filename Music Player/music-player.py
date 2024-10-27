#Sahar_Ganjkhani   #Music_Player

from tkinter import *
from tkinter import ttk,filedialog
from pygame import mixer
import os
import time
from mutagen.mp3 import MP3
import threading
from ttkthemes import themed_tk as tk

root = tk.ThemedTk()
root.title("Music Player")
root.geometry("920x670")
root.configure(bg="#FF69B4")
root.resizable(False,False)

mixer.init()


leftframe = Frame(root)
leftframe.place(x=30,y=600)

topframe = Frame(leftframe)
topframe.pack()

lengthlabel = ttk.Label(topframe,text='Total Length : --:--',relief=GROOVE)
lengthlabel.pack()

currenttimelabel = ttk.Label(topframe,text='Current Time : --:--', relief=GROOVE)
currenttimelabel.pack()


def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1

def open_folder():
    path=filedialog.askdirectory()
    if path:
        os.chdir(path)
        songs=os.listdir(path)
        print(songs)
        for song in songs:
            if song.endswith(".mp3"):
                playlist.insert(END,song)

def play_song():
    music_name=playlist.get(ACTIVE)
    mixer.music.load(playlist.get(ACTIVE))
    mixer.music.play()
    music.config(text=music_name[0:-4],font=("Tohoma",8,"bold"),bg="blue")
    show_details(music_name)
    
paused = FALSE

def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    
    
style = ttk.Style()
style.configure(".", background="aqua")
scale = ttk.Scale(root,from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.place(x=150,y=605)
scale.set(70)  
mixer.music.set_volume(0.7)



#icon
image_icon=PhotoImage(file="logo.png")
root.iconphoto(False,image_icon)

Top=PhotoImage(file="top.png")
Label(root,image=Top,bg="#FF69B4").pack()

#logo
Logo=PhotoImage(file="logo.png")
Label(root,image=Logo,bg="#FF69B4").place(x=65,y=115)

#button
play_button=PhotoImage(file="play-1.png")
Button(root,image=play_button,bg="#FF69B4",bd=0,command=play_song).place(x=100,y=400)

stop_button=PhotoImage(file="stop.png")
Button(root,image=stop_button,bg="#FF69B4",bd=0,command=mixer.music.stop).place(x=30,y=500)

resume_button=PhotoImage(file="resume.png")
Button(root,image=resume_button,bg="#FF69B4",bd=0,command=mixer.music.unpause).place(x=115,y=500)

pause_button=PhotoImage(file="pause.png")
Button(root,image=pause_button,bg="#FF69B4",bd=0,command=mixer.music.pause).place(x=200,y=500)

#label
music=Label(root,text="",font=("arial",15),fg='white',bg="#FF69B4")
music.place(x=150,y=340,anchor="center")



#music
Menu=PhotoImage(file="menu.png")
Label(root,image=Menu,bg="#FF69B4").pack(padx=10,pady=50,side=RIGHT)

music_frame=Frame(root,bd=2,relief=RIDGE)
music_frame.place(x=330,y=350,width=560,height=250)

Button(root,text='open Folder',width=15,height=2,font=("arial",10,"bold"),fg="white",bg="#21b3de",command=open_folder).place(x=330,y=300)

scroll=Scrollbar(music_frame)
playlist=Listbox(music_frame,width=100,font=("arial",10),bg="#333333",fg="gray",selectbackground="lightblue",cursor="hand2",bd=0,yscrollcommand=scroll.set)

scroll.config(command=playlist.yview)
scroll.pack(side=RIGHT,fill=Y)
playlist.pack(side=LEFT,fill=BOTH)


root.mainloop()