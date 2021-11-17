#Resolution set to 1366x768
from tkinter import Tk, Canvas
from time import perf_counter_ns
from serpent import *

class Game:
    """docstring for Game."""
    segment_array = []
    tick_rate = 30

    def __init__(self):
        self.root = Tk()
        self.root.title("Sea Serpant Game")
        self.root.geometry("1366x768")
        self.root.attributes("-fullscreen", True)
        self.root.config(cursor = "pirate")

        self.canvas = Canvas(self.root, width="1366", height="768")
        self.canvas.pack()

        self.head = Segment(100,400,self.canvas, 0)
        self.canvas.itemconfig(self.head.drawing, fill="green")
        self.segment_array.append(self.head)
        for i in range(10):
            self.segment_array.append(Segment(100 - 20 * len(self.segment_array),400,self.canvas, i + 1))
        #self.segment_array.append(Segment(100 - 50 * len(self.segment_array),100,self.canvas))

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
            coords = self.canvas.coords(self.segment_array[len(self.segment_array) - 1].drawing)
            self.segment_array.append(Segment(coords[0],coords[1],self.canvas, len(self.segment_array)))



    def game_loop(self):

        #Calculates difference in time between update loops and adjusts tick rate
        difference = (100/3) - ((perf_counter_ns() - self.previous_time)/1000000)
        self.tick_rate += round(difference)
        self.previous_time = perf_counter_ns()
        self.root.after(self.tick_rate, self.game_loop)

        for segment in self.segment_array:
            segment.move_serpent(self.segment_array)



#    def draw():

if __name__ == '__main__':
    Game().main_loop()
