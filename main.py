#Resolution set to 1366x768
import tkinter as tk
import math

class segment:
    """docstring for segment."""
    radius = 50
    # x_velocity = 0
    # y_velocity = 0
    velocity = 10
    direction = 0
    def __init__(self, x, y, canvas):

        self.drawing = canvas.create_oval(x, y, self.radius + x, self.radius + y, fill="blue")
        self.canvas = canvas
        #self.canvas.bind("<Button-1>",self.centre)
    def update(self):
        x_velocity = math.cos(self.direction) * self.velocity
        y_velocity = math.sin(self.direction) * self.velocity
        self.canvas.move(self.drawing, x_velocity, y_velocity)
    def centre(self, KeyPress):
        print(KeyPress)
        self.canvas.coords(self.drawing, 0,0,50 , 50)
class Game:
    """docstring for Game."""
    sprites = []

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sea Serpant Game")
        self.window.geometry("1366x768")

        self.canvas = tk.Canvas(self.window, width="1366", height="768")
        self.canvas.pack()

        self.head = segment(100,100,self.canvas)

        self.sprites.append(self.head)

    def mainloop(self):
        self.window.after(200, self.gameloop)
        self.window.bind("<Key>", self.KeyPress)
        self.window.mainloop()
    def KeyPress(self, Key):
        if(Key.keysym == "a"):
            self.head.direction -= 0.1
        elif(Key.keysym == "d"):
            self.head.direction += 0.1
    def gameloop(self):
        self.window.after(200, self.gameloop)
        self.head.update()
        #self.canvas.delete("all")
        #self.canvas.move(self.head.drawing,10,10)

#    def draw():

if __name__ == '__main__':
    Game().mainloop()
