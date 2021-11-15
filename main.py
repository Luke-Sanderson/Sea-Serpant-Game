#Resolution set to 1366x768
import tkinter as tk


class segment:
    """docstring for segment."""
    radius = 50
    x_velocity = 0
    y_velocity = 0
    def __init__(self, x, y, canvas):

        self.drawing = canvas.create_oval(x, y, self.radius + x, self.radius + y, fill="blue")
        self.canvas = canvas

    def update(self):
        self.x_velocity += 1
        self.y_velocity += 1

        self.canvas.move(self.drawing, self.x_velocity, self.y_velocity)

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
        self.window.mainloop()

    def gameloop(self):
        self.window.after(200, self.gameloop)
        self.head.update()
        #self.canvas.delete("all")
        #self.canvas.move(self.head.drawing,10,10)

#    def draw():

if __name__ == '__main__':
    Game().mainloop()
