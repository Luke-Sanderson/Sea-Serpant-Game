#Resolution set to 1366x768
import tkinter as tk
from math import sin, cos, atan, pi
from time import perf_counter_ns

class Segment:
    """docstring for Segment."""
    radius = 33
    # x_velocity = 0
    # y_velocity = 0
    velocity = 2
    direction = 0
    def __init__(self, x, y, canvas):

        self.drawing = canvas.create_oval(x, y, self.radius + x, self.radius + y, fill="blue")
        self.canvas = canvas
        #self.canvas.bind("<Button-1>",self.centre)
    def update(self):
        x_velocity = cos(self.direction) * self.velocity
        y_velocity = sin(self.direction) * self.velocity
        self.canvas.move(self.drawing, x_velocity, y_velocity)

class Game:
    """docstring for Game."""
    serpent = []
    tick_rate = 50

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sea Serpant Game")
        self.window.geometry("1366x768")
        self.window.attributes("-fullscreen", True)

        self.canvas = tk.Canvas(self.window, width="1366", height="768")
        self.canvas.pack()

        self.head = Segment(100,100,self.canvas)
        self.serpent.append(self.head)
        self.serpent.append(Segment(100 - 50 * len(self.serpent),100,self.canvas))


        self.previous_time = perf_counter_ns()

    def main_loop(self):
        self.window.after(self.tick_rate, self.game_loop)
        self.window.bind("<Key>", self.key_press)
        self.window.mainloop()

    def key_press(self, Key):
        if(Key.keysym.lower() == "a"): #Keep to lower
            self.head.direction -= 0.1
        elif(Key.keysym == "d"):
            self.head.direction += 0.1
        elif(Key.keysym == "Escape"):
            exit()

    def move_serpent(self):

        for index, segment in enumerate(self.serpent):

            if index != 0:
                prev = self.serpent[index - 1].canvas.coords(self.serpent[index - 1].drawing)
                cur = segment.canvas.coords(segment.drawing)
                x_change = prev[0] - cur[0]
                if x_change != 0:
                    new_direction = atan((prev[1] - cur[1])/(prev[0] - cur[0]))
                    if new_direction < 0:
                        new_direction += 2*pi
                    segment.direction = new_direction

        
            segment.update()

            prev = segment.canvas.coords(segment.drawing)


    def game_loop(self):

        #Calculates difference in time between update loops and adjusts tick rate
        #print((perf_counter_ns() - self.previous_time)/1000000)
        difference = (100/3) - ((perf_counter_ns() - self.previous_time)/1000000)
        self.tick_rate += round(difference)
        self.previous_time = perf_counter_ns()

        self.window.after(self.tick_rate, self.game_loop)

        self.move_serpent()

        #self.canvas.delete("all")
        #self.canvas.move(self.head.drawing,10,10)

#    def draw():

if __name__ == '__main__':
    Game().main_loop()
