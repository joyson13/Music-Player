import os
import pygame
from tkinter import *
from tkinter import filedialog
from tkinter import Listbox
from tkinter import messagebox
from mutagen.mp3 import MP3
from tkinter import Entry
import sqlite3
import vlc
import pafy
from time import gmtime,strftime
from tkinter import ttk
from pytube import YouTube
import eyed3
from eyed3 import id3
from ttkthemes import themed_tk as tk

time = ""
SongName = ""
SongLen = 0
SongAlbum = ""
conn = ""
url =""
current = ""
directoryfile = ""
textbox3 = ""
current1 = ""
root3 = ""

root = tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")

root.title('Opus')
root.iconbitmap(r'Opus(icon).ico')
root.minsize(800,410)
root.resizable(False,False)


listofsongs = []

global Listbox
global scrollbar
global directory

def Listb():
    global l
    global Listbox
    global scrollbar
    listofsongs.reverse()
    for items in listofsongs:
        Listbox1.insert(0, items)
    listofsongs.reverse()
    l=len(listofsongs)

def directorychooser():
    global countindex
    global directory
    global index
    global current
    countindex = 0
    index = 0
    if len(listofsongs)==0:
        directory = filedialog.askdirectory()
        os.chdir(directory)
        for files in os.listdir(directory):
            if files.endswith(".mp3"):
                listofsongs.append(files)
                countindex += 1
        if len(listofsongs) > 0:
            Listb()
    else:
        global listbox
        global scrollbar
        listofsongs.clear()
        Listbox1.delete(0,-1)
        index = 0
        pygame.mixer.music.stop()
        directorychooser()

def close():
    root2.destroy()

global paused
paused = False

def stopsong(event):
    global paused
    paused = False
    pygame.mixer.music.stop()
    status['text'] = 'Music has Stopped'

def pause(event):
    pygame.mixer.music.pause()
    global paused
    paused = True
    status['text'] = 'Music Paused'

def show_details(index):
    filelabel['text'] = 'Playing' + ' ' + listofsongs[index]
    audio = MP3(listofsongs[index])
    total_length = audio.info.length
    mins,sec = divmod(total_length,60)
    mins=round(mins)
    sec=round(sec)
    timeformat = '{:02d}:{:02d}'.format(mins,sec)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

def play():
    global paused
    if  paused:
        pygame.mixer.music.unpause()
        status['text'] = 'Playing Music' + ' ' + listofsongs[index]
    else :
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(listofsongs[index])
            pygame.mixer.music.play()
            status['text'] = 'Playing Music' + ' ' + listofsongs[index]
            show_details(index)
        except:
            messagebox.showerror("File not found","Please select a file")
    #AddData()

def nextsong(event):
    global countindex
    global index

    if  index != countindex or index >countindex:
        index = (index + 1)%l
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.play()
        status['text'] = 'Playing Music' + ' ' + listofsongs[index]
        show_details(index)
        AddData()

def previoussong(event):
    global countindex
    global index

    if  index != countindex or index <countindex:
        index = (index - 1)%l
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.play()
        status['text'] = 'Playing Music' + ' ' + listofsongs[index]
        show_details(index)
        AddData()

def set_vol(val):
    pygame.mixer.init()
    volume = float(val)/100
    pygame.mixer.music.set_volume(volume)

def about():
    messagebox.showinfo('About Opus',"This application was created on 20-3-2019\nby a skilled team consisting of Joyson Gaurea and Tejas Chendekar\ncontact us at jng05929@gmail.com or tejaschendekar@yahoo.com\nThank you for using Opus")

mu = False
def mute():
    global mu
    if mu:
        pygame.mixer.music.set_volume(0.53)
        volbutton.configure(image = speakim)
        scale.set(53)
        mu = False
    else:
        pygame.mixer.music.set_volume(0)
        volbutton.configure(image = muteim)
        scale.set(0)
        mu =True

def enter(event = None):
	global index
	n = e1.get()
	if n.isdigit():
		n1 = int(n)
		if n1 > len(listofsongs):
			messagebox.showerror("Error","Invalid index")
		else:
			index = n1-1
			pygame.mixer.music.load(listofsongs[index])
			pygame.mixer.music.play()
			status['text'] = 'Playing Music' + ' ' + listofsongs[index]
			show_details(index)
	else:
		messagebox.showerror("Error","Invalid index")


def stream():
    global textbox1
    global root2
    root2 = Tk()
    root2.title('Opus')
    root2.iconbitmap(r'Opus(icon).ico')
    root2.minsize(300,300)
    root2.resizable(False,False)
    root2.configure(bg = 'pale turquoise')
    LabelStreaming = Label(root2, text='    Youtube - Streamer    ', font='italic', bg='navajo white')
    LabelStreaming.pack()
    LabelInvisible1 = Label(root2, text='', font='italic', bg='pale turquoise')
    LabelInvisible1.pack()
    LabelInvisible2 = Label(root2, text='', font='italic', bg='pale turquoise')
    LabelInvisible2.pack()
    LabelInvisible3 = Label(root2, text='', font='italic', bg='pale turquoise')
    LabelInvisible3.pack()
    LabelStreaming1 = Label(root2, text='Enter YouTube URL', font='italic', bg='navajo white')
    LabelStreaming1.pack()
    LabelInvisible5 = Label(root2, text='', font='italic', bg='pale turquoise')
    LabelInvisible5.pack()
    textbox1=Entry(root2, width=40)
    textbox1.pack()
    LabelInvisible4 = Label(root2, text='', font='italic', bg='pale turquoise')
    LabelInvisible4.pack()
    StartStreaming = Button(root2,text = 'Start Streaming', activebackground='indigo',bg='navajo white')
    StartStreaming.pack()
    LabelInvisible6= Label(root2, text='', font='italic', bg='pale turquoise')
    LabelInvisible6.pack()
    StopStreaming = Button(root2,text = 'Stop Streaming', activebackground='indigo',bg='navajo white')
    StopStreaming.pack()
    LabelInvisible7=  Label(root2, text='', font='italic', bg='pale turquoise')
    LabelInvisible7.pack()
    DownloadStream = Button(root2,text = 'Download', activebackground='indigo',bg='navajo white')
    DownloadStream.pack()
    StartStreaming.bind("<Button -1>",StreamPlay)
    StopStreaming.bind("<Button - 1>",StopVlc)
    DownloadStream.bind("<Button -1>",YouTubeDownloader)
    root2.protocol("WM_DELETE_WINDOW",close)
    root2.mainloop()

def StopVlc(Event):
    player.stop()

def StreamPlay(Event):
    global player
    global conn
    currone = conn.cursor()
    pygame.mixer.quit()
    url = textbox1.get()
    video = pafy.new(url)
    best = video.getbest()
    playurl = best.url
    Instance = vlc.Instance()
    player = Instance.media_player_new()
    Media = Instance.media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)
    player.play()
    timeone = strftime("%Y-%m-%d %H:%M:%S",gmtime())
    currone.execute("INSERT INTO STREAMING (URL,time) VALUES (?,?)",(url,timeone))
    conn.commit()


def DataBaseConnect():
    global conn
    conn = sqlite3.connect('DataBase.db')

    #curr = conn.cursor()
    if(conn):
        return True

def DataBaseTable():
    global conn
    curr = conn.cursor()
    curr.execute("INSERT INTO RECORDS (NAME,ALBUM,DATE_TIME,SONG_LENGTH,directory) VALUES (?,?,?,?,?)",(SongName,SongAlbum,time,SongLen,directory))
    print("HERE")
    conn.commit()
    
def AddData():
    global time
    global index
    global SongLen
    global SongAlbum
    global SongName
    time = strftime("%Y-%m-%d %H:%M:%S",gmtime())
    tag = id3.Tag()
    audio = MP3(listofsongs[index])
    tag.parse(listofsongs[index])
    SongLen = audio.info.length
    SongName = tag.title
    SongAlbum = tag.album
    #DataBaseTable()

def YouTubeDownloader(event):
    url1 = textbox1.get()
    yt = YouTube(url1) 
    directory1 = filedialog.askdirectory()
    print("Downloading has now begun")
    messagebox.showinfo("YouTubeDownloader","Downloading has begun")
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(output_path=directory1)
    #currtwo = conn.cursor()
    #timetwo = strftime("%Y-%m-%d %H:%M:%S",gmtime())
    #currtwo.execute("INSERT INTO YouTubeDownloader (URL,time,directory) VALUES (?,?,?)",(url1,timetwo,directory1))
    #conn.commit()
    messagebox.showinfo("YouTubeDownloader","Downloading has been completed")
    print("Downloading is completed")


'''
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------GUI STARTS FROM HERE---------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''

status = ttk.Label(root, text = "Welcome to Opus",relief = 'sunken',anchor = 'w', font = 'Courier 10 normal')
status.pack(side='bottom',fill = 'both',pady=5)


#creating a menubar
menubar = Menu(root)
root.configure(menu=menubar)

#creating submenus
submenu = Menu(menubar,tearoff = 0)
menubar.add_cascade(label='File',menu = submenu)
submenu.add_command(label = 'Open',command = directorychooser)
submenu.add_command(label = 'Stream',command = stream)
submenu.add_command(label = 'Exit',command = root.destroy)


submenu = Menu(menubar,tearoff = 0)
menubar.add_cascade(label='Help',menu = submenu)
submenu.add_command(label = 'About us',command = about)

leftframe = Frame(root,)
leftframe.pack(side = 'left',padx= 20)
bot2frame = Frame(leftframe)
bot2frame.pack(side= 'bottom')
rightframe = Frame(root)
rightframe.pack()

global e1
Label(bot2frame, text = 'Enter Index').grid(row=0,padx=10,pady=20)
e1=Entry(bot2frame)
e1.grid(row=0,column=1,padx=10,pady=20)


label2 = ttk.Label(leftframe, text = "-=YOUR PLAYLIST=-",font='Arial 12 bold')#,fg = 'teal')
label2.pack(side = 'top',pady=20)

scrollbar = ttk.Scrollbar(leftframe, orient = "horizontal")
Listbox1 = Listbox(leftframe ,width = 50 ,xscrollcommand = scrollbar.set ,highlightcolor = "teal")
scrollbar.config(command = Listbox1.xview)
Listbox1.pack(side='top',padx=3)
scrollbar.pack()

midframe = Frame(rightframe)
botframe = Frame(rightframe)
topframe = Frame(rightframe)
topframe.pack()

playim = PhotoImage(file = 'play-button (1).png')
stopim = PhotoImage(file = 'cancel.png')
pausim = PhotoImage(file = 'pause.png')
previm = PhotoImage(file = 'previous.png')
nextim = PhotoImage(file = 'next.png')
muteim = PhotoImage(file = 'speaker.png')
speakim = PhotoImage(file = 'speaker(1).png')


filelabel = ttk.Label(rightframe, text = "-=OPUS MUSIC PLAYER=-",font='Arial 12 bold')
filelabel.pack(pady=10)

lengthlabel = ttk.Label(rightframe,text = 'Total length - 00:00')
lengthlabel.pack(pady=10)

playbutton = ttk.Button(midframe, image = playim, command = play)
playbutton.grid(row=0,column=2,padx=5)

stopbutton = ttk.Button(midframe, image = stopim)
stopbutton.grid(row=0,column=1,padx=5)

pausebutton = ttk.Button(midframe, image = pausim)
pausebutton.grid(row=0,column=0,padx=5)

nextbutton = ttk.Button(midframe, image = nextim)
nextbutton.grid(row=1,column=2,padx=5,pady=5)

previousbutton = ttk.Button(midframe, image = previm)
previousbutton.grid(row=1,column=0,padx=5,pady=5)

volbutton = ttk.Button(botframe, image = speakim, command = mute)
volbutton.grid(row=0,column = 2,padx = 3,pady = 3)

midframe.pack(padx=50,pady=30)

label = ttk.Label(botframe, text = "Volume",font='arial',anchor='s')#,fg = 'black')
label.grid(row=0,column=0,padx=5,pady=5)

scale = ttk.Scale(botframe,from_=0,to=100,orient = 'horizontal',command= set_vol)
scale.set(53)
pygame.mixer.init()
pygame.mixer.music.set_volume(53)
scale.grid(row=0,column=1,padx= 20)
botframe.pack()

stopbutton.bind("<Button -1>", stopsong)
pausebutton.bind("<Button -1>", pause)
nextbutton.bind("<Button -1>", nextsong)
previousbutton.bind("<Button -1>", previoussong)
e1.bind('<Return>',enter)

root.mainloop()