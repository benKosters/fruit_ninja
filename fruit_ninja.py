"""Fruit Ninja Gui - Final Project

This is a version of the game Fruit Ninja, a game made by Halfbrick Studios and primarily played on a mobile device.
Fruit Ninja is a game where fruit will fly up accross the screen, and the user is supposed to slice through each fruit in order to get points.
If the fruit falls to the bottom of the screen, the user loses a life. The user begins with three lives, and when all three lives are gone
the game will end. The user will then have the option to save their score if they desire.

@author: Ben Kosters (bak32)
@author: Tyler Bylsma (tjb65)
@date: December, 2022

"""
from guizero import App, Drawing, Text, TextBox, Box, PushButton, Window, Picture
from random import randint
import random
from fruit import Fruit
from player import Player
from timer import Timer
from guizero.utilities import GUIZeroImage


def add_image_to_drawing(drawing, image, x, y, anchor="nw", **kwargs):
    '''
    Method taken directly from the ui_images file created by kvlinden.
    Draws an image on a canvas at a given location.

    drawing: a GuiZero Drawing widget
    image:   a GUIZeroImage object
    x, y:    coordinates of the top left corner of where to draw the image
    anchor:  defaults to "nw" (northwest); alternatives include "center", "ne", "sw", "se", "e", ...
    '''
    return drawing.tk.create_image(x, y, image=image.tk_image, anchor=anchor, **kwargs)

class FruitNinja:
    """The FruitNinja class runs the gui application for the game. The ParticleSimulation class was used as a template for this class.
    """

    def __init__(self, app):
        """Instantiate the simulation GUI app."""
        self.app =  app
        app.hide()
        if app.hide == True:
            self.window.visible = True

        
        #Welcome window widgets
        self.window = Window(app, title='Player Info', width = 300, height = 400)
        self.window.bg = '#FF8C00'
        info_window_box = Box(self.window, layout = 'grid')
        welcome_message = Text(info_window_box, text='Welcome to Fruit Ninja!', grid = [0,0], align='top',size = 20, color = 'black')
        self.name = TextBox(info_window_box,grid = [0,1],align = 'right')
        enter_name = Text(info_window_box, text='Enter a Name:',grid = [0,1], align='left')

        picture = Picture(info_window_box,grid = [0,2],align = 'bottom', image ="Images/fruit_ninja_picture.jpg")
        
        #Play,score, and quit buttons underneath the image
        #x_button.PNG found at https://www.bing.com/images/search?view=detailV2&ccid=iZAT7IXO&id=8A998396706F073ED4411CA02B54CF890F0D1FEC&thid=OIP.iZAT7IXOzSzhj1jUFBtROQHaHA&mediaurl=https%3a%2f%2fopenclipart.org%2fimage%2f800px%2fsvg_to_png%2f78613%2fx_button.png&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.899013ec85cecd2ce18f58d4141b5139%3frik%3d7B8ND4nPVCugHA%26pid%3dImgRaw%26r%3d0&exph=757&expw=800&q=x+button&simid=607998182302108598&FORM=IRPRST&ck=0EB2484FF34B267FD36E67F58A96C042&selectedIndex=68&ajaxhist=0&ajaxserp=0
        #play_picture.PNG found at https://www.bing.com/images/search?view=detailV2&ccid=9IRXhMjp&id=08CA414B3281C2F52890A0D3A8FC617960D69C04&thid=OIP.9IRXhMjpnLKSuvQPnMj-AwHaCQ&mediaurl=https%3a%2f%2fwww.pngarts.com%2ffiles%2f3%2fPlay-Now-Button-PNG-Image-Transparent.png&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.f4845784c8e99cb292baf40f9cc8fe03%3frik%3dBJzWYHlh%252fKjToA%26pid%3dImgRaw%26r%3d0&exph=166&expw=545&q=play+now+button&simid=608025867661557399&FORM=IRPRST&ck=EA44D677EF17325BB57E023B9EAB0828&selectedIndex=58&ajaxhist=0&ajaxserp=0
        quit_button = PushButton(info_window_box, image='Images/x_button.PNG', command = app.destroy, grid = [0,4], align='right', width = 52, height =50)
        play_button = PushButton(info_window_box, image = 'Images/play_picture.PNG', command = self.start_game, grid = [0,3], width = 132, height = 40)
        scores_button = PushButton(info_window_box, text = "See High Scores", command = self.see_scores, args = ['scores.txt'],grid = [0,4], align='left')
        
        
        
        #variables for GUI app
        app.title = 'Fruit Ninja'
        self.app.bg ='#FF8C00'
        UNIT = 500
        CONTROL_UNIT = 50
        app.width = UNIT
        app.height = UNIT + CONTROL_UNIT

        # Widgets for GUI window.
        box = Box(app, layout='grid', width=UNIT, height=UNIT + CONTROL_UNIT)
        self.drawing = Drawing(box, width=UNIT, height=UNIT, grid=[0,0,2,1])
        
        #This object is used to store information about the player
        self.player_information = Player()
        self.fruit_list = []
        
        self.player_name_text = Text(box, text = "Name:", grid = [0,1], align = 'left')
        self.player_score = Text(box, text = "Score:", grid = [1,1], align = 'left')
        self.player_lives = Text(box, text = f'Lives: {self.player_information.get_lives()}', grid = [1,1])
        self.quit = PushButton(box, image = 'Images/x_button.PNG', command = app.destroy, grid = [1,1], align = 'right', width = 50, height = 52)
        
        #timer widgets
        self.timer = Timer()
        self.timer_text = Text(box, text = f'Time:{self.timer.get_time()}', grid = [0,1],align = 'right')
        
        
        self.drawing.when_mouse_dragged = self.check_remove_fruit
        app.repeat(50,self.draw_frame)
        
        #images used for the fruit objects and background
        #Watermelon.PNG was drawn by Joshua Park, who allowed us to use it for this game
        self.watermelon_picture = GUIZeroImage("Images/Watermelon.PNG", width = 75, height = 75)
        #banana.PNG was taken from: https://www.google.com/search?q=cartoon+banana&client=firefox-b-1-d&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiQ36nTzvr7AhXglWoFHbBACwwQ_AUoAXoECAEQAw&biw=766&bih=826&dpr=1.25#imgrc=yK1898uiIaJfWM
        self.banana_picture = GUIZeroImage("Images/banana.PNG", width = 75, height = 75)
        #apple.PNG was taken from: https://www.google.com/search?q=cartoon+apple&tbm=isch&ved=2ahUKEwij153Vzvr7AhVzFN4AHV5lDkIQ2-cCegQIABAA&oq=cartoon+apple&gs_lcp=CgNpbWcQAzIICAAQgAQQsQMyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6BwgAELEDEEM6BAgAEEM6CAgAELEDEIMBUJkDWIEaYLIbaABwAHgAgAGHAYgByAiSAQQxMy4xmAEAoAEBqgELZ3dzLXdpei1pbWewAQDAAQE&sclient=img&ei=eIuaY6O7HvOo-LYP3sq5kAQ&bih=826&biw=766&client=firefox-b-1-d#imgrc=EZRaf5Q_YQi_3M
        self.apple_picture = GUIZeroImage("Images/apple.PNG", width = 75, height = 75)
        #wood_background.JPG was taken from: https://www.google.com/search?client=firefox-b-1-d&q=cartoon+wood+texture#imgrc=l1i2yLT7jb0Z1M
        self.background_image = GUIZeroImage("Images/wood_background.JPG" , width = UNIT, height = UNIT)
        self.pictures = {"Watermelon": self.watermelon_picture, "Banana" : self.banana_picture, "Apple" : self.apple_picture}

    
    def update_clock(self):
        """
            Here, we update the value of the timer display on the GUI.
            This method is taken directly from the timer module by kvlinden
        """
        self.timer_text.value = 'Time:{:.1f}'.format(self.timer.get_time())

        
    def draw_frame(self):
        """ This method handles drawing each frame by clearing, moving each fruit in the list, redrawing the fruit, and checking
            if each fruit is in range of the screen. This code was lightly modified from the draw_frame method in the ParticleSimulation class

        """

        self.drawing.clear()
        add_image_to_drawing(drawing = self.drawing, image = self.background_image, x = 0, y = 0)
        for fruit in self.fruit_list:
            fruit.move(self.drawing)
            add_image_to_drawing(drawing = self.drawing, image = self.pictures[fruit.fruit_type], x = fruit.x, y = fruit.y)
            self.in_range()
            
        
    def add_fruit(self):
        """creates an instance of the fruit class, and adds it to a list of fruit objects. This method is heavly based from the ParticleSimulation class
        """
        x = randint(25,self.drawing.width)
        y = self.drawing.height
        y_velocity = randint(2,5)
        x_velocity = randint(2,5)
        #using the initial starting point of the widget determines which direction the widget moves
        #we must store the variable separately so it does not change when the fruit is moved so we can reference the direction
        starting_point = x
        if starting_point < self.drawing.height/2:
            self.pos_direction = False
        
        #checks to see which direction the fruit travels
        if x > 250:
            x_velocity*=-1
            
        fruit_type = self.get_random_fruit()
    
        fruit = Fruit(x, y, x_velocity,y_velocity, 0.25,3 , 25, fruit_type = fruit_type)
        if self.player_information.get_lives() != 0:
            self.fruit_list.append(fruit)
        else:
            self.end_game()
            
    def get_random_fruit(self):
        """This method randomly picks which image will be used for each fruit object
        """
        return random.choice(["Watermelon","Banana","Apple"])
        
    def in_range(self):
        """This method checks to see if each fruit object is within the range of the window each time the frame is drawn.
            If the fruit falls below the canvas, the fruit is removed from the fruit list and a life is taken away and updated on the screen
            The check_remove_particle method in the ParticleSimulation class was used as a reference for this method.
        """
        copy = self.fruit_list[:]
        for fruit in copy:
            if fruit.y > app.height:
                #removes the fruit
                self.fruit_list.remove(fruit)
                #removes a life and updates the canvas
                self.player_information.remove_life()
        self.player_lives.value = "Lives:" + str(self.player_information.get_lives())
        
                
    def check_remove_fruit(self, event):
        """ This method is used to check if the user drags the mouse across a fruit object. If the user does so, the fruit is removed and the
            user's score increases and is updated on the canvas. The check_remove_particle from the ParticleSimulation class was used as a base
            for this method.
        """
        copy = self.fruit_list[:]
        for fruit in copy:
            if fruit.slices(event.x, event.y,self.watermelon_picture):
                self.fruit_list.remove(fruit)
                self.player_information.increment_score()
        self.player_score.value = 'Score:'+ str(self.player_information.get_score())
    
                
                
    def start_game(self):
        """This method is called when the play button on the welcome window is pressed. It sets the name of the user, makes the welcome window
            invisible, starts the timer and the fruit starts appearing on the screen.
        """
        value = self.name.value
        self.player_information.set_name(value)
        self.player_name_text.value += value
        self.window.visible = False
        app.visible = True
        app.repeat(randint(1000,1500), self.add_fruit)
        self.timer.reset()
        app.repeat(10, self.update_clock)
        
    def end_game(self):
        """ This method is called when the number of player lives reaches zero. It stopps the app and timer, and a popup window appears asking
            the user if they wish to save their score.
        """
        self.app.cancel(self.draw_frame)
        self.app.cancel(self.add_fruit)
        self.app.cancel(self.update_clock)
        if app.yesno('Game over', 'Game over!\nSave Score?'):
            self.save_score('scores.txt')
            self.reset()
        else:
            self.reset()
        
    def reset(self):
        """ This method is called when the game ends and after the user decides if they wish to save their score or not.
            This will reset the values of the player object and clear the screen.
        """
        
        self.window.visible = True
        self.player_information = Player()
        self.player_name_text.value = 'Player Name:'
        self.player_score.value = 'Score:'
        self.fruit_list = []
        self.drawing.clear()
        app.repeat(50,self.draw_frame)
        self.timer.reset()
    
    def see_scores(self, filename):
        """Elements taken from CS 108 lecture slides week 7, slide 19. This method allows the user to see scores in descending order.
            Thank you to Prof. Wieringa for helping us with ordering the scores!
        """
        scores = {}
        with open(filename, 'r') as file:
            
            for line in file:
                x = line.strip().split(',')
                scores[int(x[0])] = x[1]
            
            print(f'{"Scores":<16}{"Player Name":<16}')
            print('-' * 30)
            for player in sorted(scores, reverse=True):
                print( f'Score: {player:<16}{scores[player]:<16}')
            
    def save_score(self, filename):
        """Saves the scores to a file so it can be referenced when the user wishes to see the scores.
        """
        with open(filename, 'a') as file:
            file.write(f'{self.player_information.get_score()},{self.player_information.get_name()}\n')
            
        
        
    


app = App()
FruitNinja(app)
app.display()

