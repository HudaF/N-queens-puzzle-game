#integration
#import pygame
#from pygame.locals import *
import pyglet 
from pyglet.window import Window
from pyglet.window import mouse
from tkinter import *
from tkinter import messagebox
'''
###music
pygame.mixer.pre_init(44100,16,2,4096)
pygame.init()

###Music
def play_music():
    pygame.mixer.music.load("game.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
def stop_music_game_close(event):
    pygame.mixer.music.load("game.wav")
    pygame.mixer.music.set_volume(0)
    pygame.mixer.music.play(-1)
def stop_music():
    pygame.mixer.music.load("game.wav")
    pygame.mixer.music.set_volume(0)
    pygame.mixer.music.play(-1)


play_music()

Y = 1
def music(event):
    global Y
    if Y%2==0:
        play_music()
        Y = Y+1
    else:
        stop_music()
        Y = Y+1   
####
'''

danger=False
win=False
Queen_Storage = []
number_queens = 0

queen_sprite,cursor_sprite,red_queen_sprite = 0,0,0
cursor_co  = (0,0)

########## Main_Chess ################
def play():
    back_image1 = pyglet.resource.image('resources/1.jpg')     ##Cream Box
    back_image2 = pyglet.resource.image('resources/2.png')     ##Black Box
    red_queen = pyglet.resource.image("resources/queen_red.png")        ##Red queen
    queen = pyglet.resource.image("resources/queen.png")         ##Queen which is being placed on the board
    cursor_image = pyglet.resource.image("resources/Snowball_Cursor.png") ##Spot Cursor

    Chess_Window= Window(back_image1.width * (number_queens), back_image2.height *(number_queens),
                         resizable=False,  # Make sure it is not resizable
                         caption="*** N QUEENS ***",  # Caption of window
                         config=pyglet.gl.Config(double_buffer=True),  # Avoids flickers
                         vsync=False  # For flicker-free animation
                         )  # Calling base class constructor
    Chess_Window.set_visible(False) #The main window for the game

    global queen_sprite,cursor_sprite,red_queen_sprite

    cimage = pyglet.image.load(("resources/cursor.png"))
    cursor = pyglet.window.ImageMouseCursor(cimage, 0, 50)
    Chess_Window.set_mouse_cursor(cursor)


    queen_sprite = [[0 for x in range(number_queens)] for y in range(number_queens)]
    cursor_sprite = [[0 for x in range(number_queens)] for y in range(number_queens)]
    red_queen_sprite = [[0 for x in range(number_queens)] for y in range(number_queens)]

    def sprite(): #spreading the images over the constructed nxn matrix. One for each type of icon/image
        global number_queens,queen_sprite,cursor_sprite,red_queen_sprite
        queen_sprite = [[0 for x in range(number_queens)] for y in range(number_queens)]
        cursor_sprite = [[0 for x in range(number_queens)] for y in range(number_queens)]
        red_queen_sprite = [[0 for x in range(number_queens)] for y in range(number_queens)]
        for i in range(number_queens):
            for j in range(number_queens):
                queen_sprite[j][i]=(pyglet.sprite.Sprite(queen, (j * 60), (i * 60)))
                red_queen_sprite[j][i]=(pyglet.sprite.Sprite(red_queen, (j * 60), (i * 60)))
                cursor_sprite[j][i]=(pyglet.sprite.Sprite(cursor_image, (j * 60), (i * 60)))
                queen_sprite[j][i].visible = False
                cursor_sprite[j][i].visible = False
                red_queen_sprite[j][i].visible = False


    def resize(): #resizing the chess window according to selected number of queens
        Chess_Window.set_size(back_image1.width * (number_queens+2), back_image2.height *(number_queens))
        Chess_Window.set_visible(True)

    def on_mouse_motion(x, y, dx, dy): #for appearance of bulls-eye cursor on chess board when mouse is kept within chess board

        global cursor_co
        for index_11 in range(number_queens):
            for index_12 in range(number_queens):
                if (index_12 * 60 <= x < (index_12 + 1) * 60) and (index_11 * 60 <= y < (index_11 + 1) * 60):   
                    cursor_sprite[index_12][index_11].visible = True
                    cursor_co=(index_12,index_11)
                    
                else:
                    cursor_sprite[index_12][index_11].visible = False

    def queen_checker(): #function that checks for queens in forbidden area. Highlights the wrongly placed queens and
        #runs on every click
        global number_queens,queen_sprite,cursor_sprite,red_queen_sprite
        for y in range(number_queens):  #y is row number
            for x in range(number_queens):  #x is column numer
                if queen_sprite[x][y].visible == True:   ##Check if Queen is placed somewhere
                    for ind in range(number_queens):
                        ##Checks if no queen is already placed in the same row
                        if ind != x: #consider ind as column number 
                            if queen_sprite[ind][y].visible:
                                red_queen_sprite[ind][y].visible = True
                                red_queen_sprite[x][y].visible = True
                                danger = True

                        ##Checks if no queen is already placed in the same column
                        if ind != y:  #consider ind as row number
                            if queen_sprite[x][ind].visible:        
                                red_queen_sprite[x][ind].visible = True
                                red_queen_sprite[x][y].visible = True
                                danger = True
                                
                        if ind>0:
                            if x+ind<=(number_queens-1) and y+ind<=(number_queens-1):   ##for the secondary diagonal
                                if queen_sprite[x+ind][ind+y].visible:
                                    red_queen_sprite[ind+x][ind+y].visible=True
                                    red_queen_sprite[x][y].visible=True
                                    danger = True

                            if x+ind<=(number_queens-1) and y-ind>=0:  ##for the main diagonal
                                if queen_sprite[x+ind][y-ind].visible:
                                    red_queen_sprite[x+ind][y-ind].visible=True
                                    red_queen_sprite[x][y].visible=True
                                    danger = True


    def replay(): #function for setting all variables to initial stages and replaying game from start.
        global win
        global danger
        for c in range(number_queens):
            for d in range(number_queens):
                queen_sprite[d][c].visible = False   ##No queen is placed on the board
                cursor_sprite[d][c].visible = False   ##No cursor sprite visible at the start
                red_queen_sprite[d][c].visible = False   ##No error sprite appears
            del Queen_Storage[:] ##deleting all the members of the list
        danger = False  ##No Queen then in danger
        win = False     ##Not won the game

    @Chess_Window.event()
    def on_mouse_press(x, y, button, modifiers):
        global number_queens,win,danger,Queen_Storage,queen_sprite,cursor_sprite,red_queen_sprite,cursor_co
        if x>=0 and x<=(number_queens*60):# loops running within the dimensions of the chessboard
            if y>=0 and y<=(number_queens*60):
                if button == mouse.LEFT: ## if left mouse button is clicked
                    if not win:     ##Only allows execution of game is not won after starting it. Once won it stops working until play again execution.
                        for v in range(number_queens):
                            for w in range(number_queens):
                                if (w * 60 <= x < (w + 1) * 60) and (v * 60 <= y < (v + 1) * 60):
                                    if queen_sprite[w][v].visible != True:   ##Checking if queen is already not placed
                                        if len(Queen_Storage) > ((number_queens)-1):      ##Don't allow the placement of queens of the number exceed the 8.
                                            queen_sprite[w][v].visible = False

                                        else:
                                            queen_sprite[w][v].visible = True
                                            Queen_Storage.append(queen_sprite[w][v].visible)     ##If queen is added to the board then it is also added to storage
                                            #print("Queen on Board: ", Queen_Storage) ##print the number of queens on board on console
                                            #print("Queen added at box (" + str(w+1) + "," + str(v+1) + ")\n") ##print the coordinates for the queen on console

                                    else:
                                        queen_sprite[w][v].visible = False #if queen is already placed, then making dissapear.
                                        Queen_Storage.pop()     ##If queen is removed from the board then it is also deleted from the storage

                        for index1 in range(number_queens):
                            for index2 in range(number_queens): #setting all error queens to invisible so that  each queen be checked
                                red_queen_sprite[index2][index1].visible = False
                        danger = False
                        queen_checker()
        elif x>(number_queens*60):
            if y>=123 and y<=180:
                danger=False
                win=False
                Queen_Storage = []
                number_queens = 0
                queen_sprite,cursor_sprite,red_queen_sprite = 0,0,0
                cursor_co  = (0,0)
                Chess_Window.close()
                
            elif y>=229 and y<=281:
                replay()

    @Chess_Window.event
    def on_mouse_motion(x, y, dx, dy): #for appearance of bulls-eye cursor on chess board when mouse is kept within chess board

        global cursor_co
        for index_11 in range(number_queens):
            for index_12 in range(number_queens):
                if (index_12 * 60 <= x < (index_12 + 1) * 60) and (index_11 * 60 <= y < (index_11 + 1) * 60):   
                    cursor_sprite[index_12][index_11].visible = True
                    cursor_co=(index_12,index_11)
                    
                else:
                    cursor_sprite[index_12][index_11].visible = False

                        
    def on_draw2(): #function for making visible the chess board and icons/images related to it
        global main
        global number_queens,queen_sprite,cursor_sprite,red_queen_sprite
        Chess_Window.clear()
    
        game_options=pyglet.sprite.Sprite(pyglet.image.load(("resources/game_options.jpg")),60*(number_queens),0)
        tile1 = back_image1 ##Setting images to new variables
        tile2 = back_image2
        for index_1 in range(number_queens):    ##Nested loops to draw total nxn boxes
            for index_2 in range(number_queens):
                if number_queens%2==0: 
                    if index_1 % 2 == 0:
                        tile1.blit(index_1 * 60, index_2 * 60)  ##Drawing Tile2 image
                        tile1, tile2 = tile2, tile1   ##Swaping the tiles
                    else:
                        tile2.blit(index_1 *60 , index_2 * 60)  ####Drawing Tile1 image
                        tile1, tile2 = tile2, tile1
                else:
                    if index_1 % 1 == 0:
                        tile1.blit(index_1 * 60, index_2 * 60)  ##Drawing Tile2 image
                        tile1, tile2 = tile2, tile1   ##Swaping the tiles
                    else:
                        tile2.blit(index_1 *60 , index_2 * 60)  ####Drawing Tile1 image
                        tile1, tile2 = tile2, tile1
        for p in range(number_queens): #drawing all the images on the matrix, visible and invisible
            for q in range(number_queens):
                queen_sprite[q][p].draw()
                red_queen_sprite[q][p].draw()
                cursor_sprite[q][p].draw()

        game_options.draw()
        game_options.visible=True

    # Updating the Window
    def update(d):
        on_draw2()
    
    resize()
    sprite()
    
    # Se    tting the time interval to update
    pyglet.clock.schedule_interval(update, 1 / 120)

    # Running Pyglet
    pyglet.app.run()






############ GUI_CODE ############
root = Tk()
root.geometry("1000x1000")


def command():
    top = Toplevel(root)
    top.resizable(0,0)
    background_image2 =PhotoImage(file="instructions.png")
    bg2 = Label(top, image = background_image2)
    bg2.pack(fill=BOTH, expand = 1)
    top.title("Instructions")
    button = Button(top, text="Back", command=top.destroy)
    button.place(height = 100, width = 200, x = 320, y = 570)
    top.mainloop()

def Play_Game():
    
    top2 = Toplevel(root)
    top2.geometry("1000x1000")
    top2.resizable(0,0)
    top2.title("Number Of Screens")
    canvas = Canvas(top2,width=1920,height=1200,bg="black") # a canvas that will draw the background image in the window
    canvas.place(x=0,y=0) # it will start placing it from this coordinate
    bgPhoto = PhotoImage(file = "bg.png")
    canvas.create_image(0,0,image=bgPhoto,anchor = NW)
    theLabel = Label(top2,text="Select Number of Queens",font="Broadway")
    theLabel.pack(fill=X)
    
    def button1(event): ## these are the button click functions, which are to be updated as per teh code depending upon teh level of difficulty selected
        global number_queens
        number_queens = 6
        play()
    def button2(event):
        global number_queens
        number_queens = 7
        play()
    def button3(event):
        global number_queens
        number_queens = 8
        play()
    def button4(event):
        global number_queens
        number_queens = 9
        play()
    def button5(event):
        global number_queens
        number_queens = 10
        play()
    def button6(event):
        global number_queens
        number_queens = 11
        play()
    def backButton(event):
        pass
        #print("back button clicked, back to main menu")
    def InstructButton(event):
        pass
        #print("Instruction page needs to be uploaded")
        
    button_1 = Button(top2, text = "N = 6",height=5,width=15, fg="black",bg="violet")
    button_1.bind("<Button-1>",button1)

    button_1.place(x=460,y=30)


    button_2 = Button(top2, text = "N = 7",height=5,width=15, bg="violet")
    button_2.bind("<Button-1>",button2)

    button_2.place(x=460,y=140)

    button_3 = Button(top2, text = "N = 8",height=5,width=15, bg="violet")
    button_3.bind("<Button-1>",button3)

    button_3.place(x=460,y=260)

    button_4 = Button(top2, text = "N = 9",height=5,width=15, bg="violet")
    button_4.bind("<Button-1>",button4)

    button_4.place(x=460,y=380)

    button_5 = Button(top2, text = "N = 10",height=5,width=15, bg="violet")
    button_5.bind("<Button-1>",button5)
    button_5.place(x=460,y=500)


    button_6 = Button(top2, text = "N = 11",height=5,width=15, bg="violet")
    button_6.bind("<Button-1>",button6)
    button_6.place(x=460,y=618)

    BackButton = Button(top2, text = "Back", height = 2  , width = 15, bg="violet", command = top2.destroy)
    BackButton.bind("<Button-1>",backButton)

    BackButton.place(x = 0,y = 662)
    top2.mainloop()

    

### background photo
bg_photo=PhotoImage(file="Nqueen.png")
bg=Label(root,image=bg_photo)
bg.pack(fill=BOTH, expand = 1)
##
root.title("N-Queen")
top_text =Label(bg,text="N-Queen",fg="white",bg="black")
top_text.pack()

              
button1=Button(bg,text="PLAY",fg="black",bg="white",command = Play_Game)
button2=Button(bg,text="SOUND",fg="black",bg="white")
button4=Button(bg,text="QUIT",fg="black",bg="white",command=root.destroy)
button3 = Button(bg, text = "INSTRUCTIONS", fg = "Black",bg = "white", command=command)
button1.place(height = 100, width = 200, x = 50, y = 50)

#button2.bind("<Button-1>",music)
button2.place(height = 100, width = 200, x = 50, y = 170)

#
#button4.bind("<Button-1>",stop_music_game_close)
button3.place(height = 100, width = 200, x = 50, y = 290)
button4.place(height = 100, width = 200, x = 50, y = 410)
root.mainloop()

