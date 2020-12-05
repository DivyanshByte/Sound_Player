import pygame
from tkinter import *
from tkinter import filedialog
from tkinter import Menu
from tkinter.ttk import *
from mutagen.mp3 import MP3
import time
import threading

window = Tk()

window_icon = PhotoImage(file="window_icon.png")
window.iconphoto(False,window_icon)

sound_list = []
playing_sound = False
pygame.mixer.init()
audio_mutagen = None
current_time = 0
first_time = True


volume_label = Label(window, text="Volume")
volume_label.place(rely=0.98,relx=0.02,anchor=SW)
full_volume_icon = PhotoImage(file="full_volume_icon.png")
low_volume_icon = PhotoImage(file="low_volume_icon.png")
mute_volume_icon = PhotoImage(file="mute_volume_icon.png")


def open():
    files1 = filedialog.askopenfilenames(filetypes=[("Mp3 Files", "*.mp3")])
    files = list(files1)
    sound_list_in_list = sound_list_box.curselection()
    for audio1 in files:
        audio = audio1.replace(' ','%20')
        sound_list.append(audio)
        sound_list_box.insert(len(sound_list)+files.index(audio1),'🎵'+audio1.split('/')[-1].replace('.'+audio1.split('.')[-1],' '))
    play_sound.configure(state="normal")
    delete_sound.configure(state="normal")


def play():
    global playing_sound,current_time
    sound_list_in_list = sound_list_box.curselection()
    for sound in sound_list_in_list:
        pygame.mixer.music.unload()
        pygame.mixer.music.load(sound_list[sound].replace('%20',' '))
        pygame.mixer.music.play()
        playing_sound = True
        pause_sound.configure(state="normal",text="Pause")
        pause_sound.configure(image=pause_icon)
        global audio_mutagen,current_time,first_time
        audio_mutagen = None
        audio_mutagen = MP3(sound_list[sound].replace('%20',' '))
        total_length = audio_mutagen.info.length
        mins, secs = divmod(total_length, 60)
        mins = round(mins)
        secs = round(secs)
        total_seconds = (mins*60)+secs
        song_time.configure(from_=0,to=total_seconds)
        song_time.state(["!disabled"])
        song_time.set(0)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        song_full_time.configure(text=timeformat)
        song_now_time.configure(text="00:00")
        current_time = 0
        if first_time is True:
            t1 = threading.Thread(target=start_count, args=(total_length,))
            t1.start()
        first_time = False

def start_count(t):
    global playing_sound,current_time
    while current_time <= t and pygame.mixer.music.get_busy():
        if playing_sound == False:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            song_now_time.configure(text = timeformat)
            song_time.set(current_time)
            time.sleep(1)
            current_time += 1


def pause():
    global playing_sound
    if playing_sound:
        pygame.mixer.music.pause()
        playing_sound = False
        pause_sound.configure(text="Resume")
        pause_sound.configure(image=resume_icon)
        song_time.state(["disabled"])
    else:
        pygame.mixer.music.unpause()
        playing_sound = True
        pause_sound.configure(text="Pause")
        pause_sound.configure(image=pause_icon)
        song_time.state(["!disabled"])

def delete():
    sound_list_in_list = sound_list_box.curselection()
    for sound in sound_list_in_list:
        sound_list_box.delete(sound)
        sound_list.remove(sound_list[sound])
    if len(sound_list) == 0:
        global t1
        play_sound.configure(state="disabled")
        pause_sound.configure(state="disabled",text="Pause")
        pause_sound.configure(image=pause_icon)
        delete_sound.configure(state="disabled")
        song_time.configure(from_=0,to=0)
        song_time.state(['disabled'])
        song_full_time.configure(text='00:00')
        song_now_time.configure(text='00:00')
        playing_sound = False
        pygame.mixer.music.unload()

def volume(value):
    pygame.mixer.music.set_volume(float(value)/100)
    value = int(float(value))
    global volume_label
    if value < 101 and value > 75:
        volume_label.configure(image=full_volume_icon)
    elif value<76 and value>0:
        volume_label.configure(image=low_volume_icon)
    else:
        volume_label.configure(image=mute_volume_icon)

def change_time(value):
    global current_time
    if current_time is not int(float(value)):
        pygame.mixer.music.play(-1, int(float(value)))
        current_time = int(float(value))


open_files = Button(window,text="Open Files", command=open)
open_files.place(rely=0.98, relx=0.95, anchor=SE)
open_icon = PhotoImage(file="open_icon.png")
open_files.configure(image=open_icon,compound = LEFT)


play_sound = Button(window,text="Play",command=play, state="disabled")
play_sound.place(rely=0.98,relx=0.45,anchor=S)
play_icon = PhotoImage(file="play_icon.png")
play_sound.configure(image=play_icon)

pause_sound = Button(window,text="Pause",command=pause, state="disabled")
pause_sound.place(rely=0.98,relx=0.30,anchor=S)
pause_icon = PhotoImage(file="pause_icon.png")
resume_icon = PhotoImage(file="resume_icon.png")
pause_sound.configure(image=pause_icon)

delete_sound = Button(window,text="Delete",command=delete, state="disabled")
delete_sound.place(rely=0.98,relx=0.60,anchor=S)
delete_icon = PhotoImage(file="delete_icon.png")
delete_sound.configure(image=delete_icon)

volume_sound = Scale(window,from_=0,to=100,command=volume,orient=HORIZONTAL)
volume_sound.place(rely=0.98,relx=0.055,anchor=SW)
volume_sound.set(100)
volume_label.configure(image=full_volume_icon)

sound_list_box = Listbox(window,width=71,foreground=("#%02x%02x%02x" %(217, 72, 221) ), background="yellow")
sound_list_box.place(relx=0.5, rely=0,anchor=N,height=575)

song_full_time = Label(window,text="00:00")
song_full_time.place(relx=0.95,rely=0.93,anchor=SE)

song_now_time = Label(window,text="00:00")
song_now_time.place(relx=0.020,rely=0.93,anchor=SW)

song_time = Scale(window,from_=0,to=10,orient=HORIZONTAL,command=change_time)
song_time.place(relx=0.485,rely=0.93,anchor=S,width=517,height=20)
song_time.state(['disabled'])

window.title('Music Player')
window.geometry('650x650')
window.resizable(False, False)
window.mainloop()