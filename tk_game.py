import tkinter as tk
import time
from playsound import playsound
from threading import Thread



from PIL import Image, ImageTk, ImageDraw

class TK_HEXAGON:
    def __init__(self, idx, game):
        self.idx = idx
        self.game = game
        self.left_wall = False
        self.right_wall = False
        self.bottom_wall = False
        self.neighbors=[]
    
    def click_event(self, event):
        self.game.hexagon_clicked(self.idx)
        print('Clicked object at: ', self.idx)

class GAME_WINDOW:
    def __init__(self, game):
        self.game = game
        self.width = 1024
        self.height = 768
        #self.hexagons = hexagons

        self.hex_height = 100
        self.hex_width = int(0.867 * self.hex_height)  

        self.window = tk.Tk()
        self.window.geometry(str(self.width)+"x"+str(self.height))
        self.window.title("KVIZ")

        self.load_images()

        self.can = tk.Canvas(self.window)
        self.can.pack(anchor='nw', fill='both', expand=1)
        self.can.create_image(0, 0, image=self.bg_image, anchor='nw')

        self.draw_names()
        self.draw_hexagons()


    def load_images(self):
        #background
        self.bg_image = Image.open("pics/background.png")
        self.bg_image = self.bg_image.resize( (self.width,self.height) )
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        #white hexagon
        self.hexagon_image_white = Image.open("pics/hexagon.png")
        self.hexagon_image_white = self.hexagon_image_white.resize((self.hex_width,self.hex_height))
        self.hexagon_image_white = ImageTk.PhotoImage(self.hexagon_image_white)

        #black hexagon
        self.hexagon_image_black = Image.open("pics/hexagon_black.png")
        self.hexagon_image_black = self.hexagon_image_black.resize((self.hex_width,self.hex_height))
        self.hexagon_image_black = ImageTk.PhotoImage(self.hexagon_image_black)

        #blue
        self.hexagon_image_blue = Image.open("pics/hexagon_blue.png")
        self.hexagon_image_blue = self.hexagon_image_blue.resize((self.hex_width,self.hex_height))
        self.hexagon_image_blue = ImageTk.PhotoImage(self.hexagon_image_blue)

        #orange
        self.hexagon_image_orange = Image.open("pics/hexagon_orange.png")
        self.hexagon_image_orange = self.hexagon_image_orange.resize((self.hex_width,self.hex_height))
        self.hexagon_image_orange = ImageTk.PhotoImage(self.hexagon_image_orange)

        #white question hexagon
        self.hexagon_question_white = Image.open("pics/hexagon.png")
        self.hexagon_question_white = self.hexagon_question_white.resize(( int(self.width*0.6) , int(self.height*0.8) ))
        self.hexagon_question_white = ImageTk.PhotoImage(self.hexagon_question_white)

    def canvas_click_event(self, event):
        print('Clicked canvas: ', event.x, event.y, event.widget)

    def draw_names(self):
        #print("self.game.player1 value is ", self.game.player1)
        self.can.create_rectangle(50,self.height-100,250,self.height-10,outline ="blue",fill ="white",width = 2)
        self.can.create_text(150, self.height-50, fill="blue",font="Times 20 bold", text=self.game.player1)
        self.can.create_rectangle(self.width-250,self.height-100,self.width-50,self.height-10,outline ="orange",fill ="white",width = 2)
        self.can.create_text(self.width-150, self.height-50, fill="orange",font="Times 20 bold", text=self.game.player2)

    def draw_hexagons(self):
        self.spots = []
        #self.hexagons = []
        idx = 0
        for row in range(8):
            hex_y = 3 + row * self.hex_height*0.8
            for col in range(row):
                #print("idx", idx)
                hex_x = self.width/2 - row*self.hex_width/2*1.1 + col*self.hex_width*1.1

                #h = self.hexagons[idx]
                h = TK_HEXAGON(idx, self.game)
                h_text_x = hex_x+self.hex_width/2
                h_text_y = hex_y+self.hex_height/2


                spot = self.draw_hexagon(idx, hex_x, hex_y)
                spot_text = self.can.create_text(h_text_x, h_text_y, fill="black",font="Times 20 bold", text=str(h.idx))
                
                #spot = self.can.create_image(hex_x, hex_y, image=self.hexagon_image_white, anchor='nw')
                #spot = self.can.create_image(0, 0, image=self.hexagon_image_white)
                self.spots.append(spot)

                #self.can.tag_bind(spot, '<Button-1>', self.hexagons[idx].click_event)
                self.can.tag_bind(spot, '<Button-1>', h.click_event)
                idx += 1

    def draw_hexagon(self, idx, x, y):
        hexagon = self.game.hexagons[idx]
        state = hexagon.state
        
        if state == "white":
            return self.can.create_image(x, y, image=self.hexagon_image_white, anchor='nw')
        if state == "blue":
            return self.can.create_image(x, y, image=self.hexagon_image_blue, anchor='nw')
        if state == "orange":
            return self.can.create_image(x, y, image=self.hexagon_image_orange, anchor='nw')
        if state == "black":
            return self.can.create_image(x, y, image=self.hexagon_image_black, anchor='nw')

    def redraw_hexagon(self, hexagon_idx, new_state):
        h = self.hexagons[hexagon_idx-1]
        if new_state == "blue":
            self.can.itemconfig(self.spots[hexagon_idx-1], image=self.hexagon_image_blue)
        if new_state == "orange":
            self.can.itemconfig(self.spots[hexagon_idx-1], image=self.hexagon_image_orange)
        if new_state == "black":
            self.can.itemconfig(self.spots[hexagon_idx-1], image=self.hexagon_image_black)
            self.can.create_text(h.text_x, h.text_y, fill="white",font="Times 20 bold", text=str(h.idx))

    def clear(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        print("kreslim bg")
        self.can.create_image(0, 0, image=self.bg_image, anchor='nw')

    def exit(self):
        self.window.destroy()
    
    def redraw(self):
        self.can.delete('all')
        self.can.create_image(0, 0, image=self.bg_image, anchor='nw')
        self.draw_hexagons()
        self.draw_names()

    def show_question(self, abbreviation):
        self.can.delete('all')
        self.can.create_image(0, 0, image=self.bg_image, anchor='nw')
        self.draw_names()
        self.show_timer(10, abbreviation)

    def update_timer(self):
        if self.game.question_outcome is not None:
            self.tenths_left = 0
            return
        degrees = int( 360 * (1- (self.tenths_left/self.tenths_total) ) )
        self.tenths_left -= 1
        self.can.create_arc(self.width//4-5, self.height//5-5, 3*self.width//4+5, 3*self.height//4+5, start=0, extent=degrees, outline="white", width=10, style="arc")
        if self.tenths_left % 10 == 0:
            thread = Thread(target=lambda: playsound('sounds/tick.mp3') )
            thread.start()

    def start_timer(self):
        if self.tenths_left < self.tenths_total:
            return
        for i in range(self.tenths_total+1):
            self.window.after(100 * i, self.update_timer)

    def show_timer(self, seconds, text):
        text_y = self.height/2
        text_x = self.width/2
        timer_hex = self.can.create_image(200, 50, image=self.hexagon_question_white, anchor='nw')
        timer_text = self.can.create_text(text_x, text_y, fill="black",font="Times 70 bold", text=text)

        self.can.create_oval(self.width//4, self.height//5, 3*self.width//4, 3*self.height//4,width=3)
        self.can.create_oval(self.width//4-10, self.height//5-10, 3*self.width//4+10, 3*self.height//4+10, width=3)
        
        #probably just replace by an oval
        self.can.create_arc(self.width//4-5, self.height//5-5, 3*self.width//4+5, 3*self.height//4+5, start=0, extent=359, outline="orange", width=10, style="arc")

        self.tenths_total = 10*seconds
        self.tenths_left = self.tenths_total

    def blue_wins(self):
        self.clear()
        empty_label = tk.Label(self.window, text=" ", font="Times 25 bold")
        final_label = tk.Label(self.window, text="MODREJ VÍTĚZÍ", font="Times 40 bold", fg="BLUE")
        empty_label.pack()
        final_label.pack()

    def orange_wins(self):
        self.clear()
        empty_label = tk.Label(self.window, text=" ", font="Times 25 bold")
        final_label = tk.Label(self.window, text="ORANŽOVEJ VÍTĚZÍ", font="Times 40 bold", fg="ORANGE")
        empty_label.pack()
        final_label.pack()

    def show(self):
        self.window.mainloop()