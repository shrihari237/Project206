import socket
from tkinter import * 
import tkinter as tk
from  threading import Thread
import random
from PIL import ImageTk, Image
import platform


screen_width = None
screen_height = None

SERVER = None
PORT = None
IP_ADDRESS = None
playerName = None

canvas1 = None

nameEntry = None
nameWindow = None

ticketGrid = []
currentNumberList = []
    




def recivedMsg():
    pass

def createTicket():
    global gameWindow
    global ticketGrid

    #Ticket Frame
    mainLabel = Label(gameWindow,width=65,height=16,relief='ridge',borderwidth=5,bg="white")
    mainLabel.place(x=95,y=119)

    xPos = 105
    yPos = 130

    for row in range(0,3):
        rowList = []
        for col in range(0,9):
            if(platform.system()=='Darwin'):
                #for MAC users
                boxButton = Button(gameWindow,
                                   font=("Chalkboard SE",18),
                                   borderwidth=3,
                                   pady=23,
                                   padx=22,
                                   bg='#fff176', #initial yellow color
                                   highlightbackground="#fff176",
                                   activebackground='#c5ela5') #onpress green color

                boxButton.place(x=xPos,y=yPos,)
            else:
                #for windows users
                boxButton = tk.Button(gameWindow,font=("Chalkboard SE",30),width=3,height=2,borderwidth=5,bg='#fff176')
                boxButton.place(x=xPos,y=yPos)

            rowList.append(boxButton)
            xPos += 64
        #Creating nested array
        ticketGrid.append(rowList)
        xPos = 105
        yPos+=82

def placeNumber():
    global ticketGrid
    global currentNumberList

    for row in range(0,3):
        randomColList = []
        counter=0
        #getting random 5 cols
        while counter<=4:
            randomCol = random.randint(0,8)
            if(randomCol not in randomColList):
                randomColList.append(randomCol)
                counter+=1


    numberContainer={
        "0":[1,2,3,4,5,6,7,8,9],
        "1":[10,11,12,13,14,15,16,17,18,19],
        "2":[29,30,31,.32,33,34,35,36,37,38,39],
        "3":[40,41,42,43,44,45,46,47,48,49],
        "4":[50,51,52,53,54,55,56,57,58,59],
        "5":[60,61,62,63,64,65,66,67,68,69],
        "6":[70,71,72,73,74,75,76,77,78,79],
        "7":[80,81,82,83,84,85,86,87,87,88,89,90],
    } 

    counter = 0
    while (counter < len(randomColList)):
        colNum = randomColList[counter]
        numbersListByIndex = numberContainer[str(colNum)]
        randomNumber = random.choice(numbersListByIndex) 

        if(randomNumber not in currentNumberList):
            numberBox = ticketGrid[row][colNum]
            numberBox.configure(text=randomNumber, fg="black")
            currentNumberList.append(randomNumber)
            counter+=1          

def gameWindow():

    global gameWindow
    global canvas2
    global screen_width
    global screen_height
    global playerTurn
    global playerType
    global playerName



    gameWindow = Tk()
    gameWindow.title("Tambola Family Game")
    gameWindow.geometry('800x600')

    screen_width = gameWindow.winfo_screenwidth()
    screen_height = gameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas2 = Canvas( gameWindow, width = 500,height = 500)
    canvas2.pack(fill = "both", expand = True)

    # Display image
    canvas2.create_image( 0, 0, image = bg, anchor = "nw")

    # Add Text
    canvas2.create_text( screen_width/4.5,50, text = "Tambola Family Fun", font=("Chalkboard SE",50), fill="white")



    createTicket()
    placeNumber()
    gameWindow.resizable(True, True)
    gameWindow.mainloop()

def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()
    nameEntry.delete(0, END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())

    gameWindow()

def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1

    nameWindow  = Tk()
    nameWindow.title("Tambola Family Fun")
    nameWindow.geometry('800x600')


    screen_width = nameWindow.winfo_screenwidth()
    screen_height = nameWindow.winfo_screenheight()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas1 = Canvas( nameWindow, width = 500,height = 500)
    canvas1.pack(fill = "both", expand = True)
    # Display image
    canvas1.create_image( 0, 0, image = bg, anchor = "nw")
    canvas1.create_text( screen_width/4.5,screen_height/8, text = "Enter Name", font=("Chalkboard SE",60), fill="black")

    nameEntry = Entry(nameWindow, width=15, justify='center', font=('Chalkboard SE', 30), bd=5, bg='white')
    nameEntry.place(x = screen_width/7, y=screen_height/5.5 )


    button = Button(nameWindow, text="Save", font=("Chalkboard SE", 30),width=11, command=saveName, height=2, bg="#80deea", bd=3)
    button.place(x = screen_width/6, y=screen_height/4)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()



def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT  = 6000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    thread = Thread(target=recivedMsg)
    thread.start()

    askPlayerName()


setup()
