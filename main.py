#Resolution set to 1366x768
import tkinter as tk
from math import sin, cos, atan2, pi, sqrt
from time import perf_counter_ns

class Segment:
    """docstring for Segment."""
    radius = 50
    acceleration = 1
    max_velocity = 8
    velocity = 0
    x_velocity = 0
    y_velocity = 0

    direction = 0
    GRAVITY = 0.2

    def __init__(self, x, y, canvas, id):
        self.drawing = canvas.create_oval(x, y, self.radius + x, self.radius + y, fill="blue")
        self.canvas = canvas
        self.id = id
    def update(self):
        if self.canvas.coords(self.drawing)[1] > 200 or self.id != 0:
            self.velocity += self.acceleration
            if self.velocity > self.max_velocity: self.velocity = self.max_velocity
            self.x_velocity = cos(self.direction) * self.velocity
            self.y_velocity = sin(self.direction) * self.velocity
        else:
           self.y_velocity += self.GRAVITY
           self.velocity = self.y_velocity
           if self.direction > pi:
               self.direction = 2*pi -self.direction
           elif self.direction < 0:
               self.direction = -self.direction

        self.canvas.move(self.drawing, self.x_velocity, self.y_velocity)

class Game:
    """docstring for Game."""
    serpent = []
    tick_rate = 50

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sea Serpant Game")
        self.root.geometry("1366x768")
        self.root.attributes("-fullscreen", True)
        self.root.config(cursor = "man")

        self.canvas = tk.Canvas(self.root, width="1366", height="768")
        self.canvas.pack()

        self.head = Segment(100,400,self.canvas, 0)
        self.head.head = 1
        self.canvas.itemconfig(self.head.drawing, fill="green")
        self.serpent.append(self.head)
        for i in range(10):
            self.serpent.append(Segment(100 - 20 * len(self.serpent),400,self.canvas, i + 1))
        #self.serpent.append(Segment(100 - 50 * len(self.serpent),100,self.canvas))

        self.sea = self.canvas.create_line(0,200,1366,200, fill="Blue")

        self.previous_time = perf_counter_ns()

    def main_loop(self):
        self.root.after(self.tick_rate, self.game_loop)
        self.root.bind("<Key>", self.key_press)
        self.root.mainloop()

    def key_press(self, Key):

        if(Key.keysym.lower() == "a" and self.head.canvas.coords(self.head.drawing)[1] > 200):
            self.head.direction -= 0.1
            self.head.velocity -= 0.1
        elif(Key.keysym.lower() == "d" and self.head.canvas.coords(self.head.drawing)[1] > 200):
            self.head.direction += 0.1
            self.head.velocity -= 0.1
        elif(Key.keysym == "Escape"):
            exit()
        elif(Key.keysym.lower() == "c"):
            coords = self.canvas.coords(self.serpent[len(self.serpent) - 1].drawing)
            self.serpent.append(Segment(coords[0],coords[1],self.canvas, len(self.serpent)))

    def move_serpent(self):

        for index, segment in enumerate(self.serpent):

            if index != 0:
                prev = self.serpent[index - 1].canvas.coords(self.serpent[index - 1].drawing)
                cur = segment.canvas.coords(segment.drawing)
                vector = (prev[0] - cur[0], prev[1] - cur[1])
                x_change = prev[0] - cur[0]
                new_direction = atan2(vector[1], vector[0])
                segment.direction = new_direction

                #Adjust speed
                distance = sqrt(vector[0]**2 + vector[1]**2)
                if distance > 30:
                    segment.max_velocity =  9 #Max Vel at 8
                elif distance < 20:
                    segment.max_velocity = 6
                elif distance < 5:
                    segment.max_velocity = 1
                else:
                    segment.max_velocity = 8

#                print(segment.velocity)

            segment.update()

            prev = segment.canvas.coords(segment.drawing)


    def game_loop(self):

        #Calculates difference in time between update loops and adjusts tick rate
        difference = (100/3) - ((perf_counter_ns() - self.previous_time)/1000000)
        self.tick_rate += round(difference)
        self.previous_time = perf_counter_ns()
        self.root.after(self.tick_rate, self.game_loop)

        self.move_serpent()


#    def draw():

if __name__ == '__main__':
    Game().main_loop()
