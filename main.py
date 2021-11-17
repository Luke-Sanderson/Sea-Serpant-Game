#Resolution set to 1366x768
from tkinter import Tk, Canvas, ttk
from time import perf_counter_ns
from serpent import *

class Game:
    """docstring for Game."""
    tick_rate = 30
    GAME_STATES = ["main_menu", "pause", "in_game"]

    def __init__(self):
        self.root = Tk()
        self.root.title("Sea Serpant Game")
        self.root.geometry("1366x768")
        self.root.attributes("-fullscreen", True)
        self.root.config(cursor = "pirate")

        self.current_game_state = self.GAME_STATES[0]

        self.canvas_game = Canvas(self.root, width="1366", height="768")
        self.canvas_menu = Canvas(self.root, width="1366", height="768")

        self.initialise_menu()
        self.canvas_menu.pack()

        self.previous_time = perf_counter_ns()

    def switch_scene(self, next):

        if self.current_game_state == "main_menu":
            if next == "in_game":
                self.canvas_menu.pack_forget()
                self.canvas_game.delete("all")
                self.initialise_game()
                self.canvas_game.pack()
                self.root.after(self.tick_rate, self.game_loop)

        elif self.current_game_state == "in_game":
            if next == "main_menu":
                self.canvas_game.pack_forget()
                self.canvas_menu.pack()

        self.current_game_state = next

    def initialise_menu(self):
        self.menu_buttons = []
        self.menu_buttons.append(ttk.Button(self.canvas_menu, text = "Play game", command=lambda: self.switch_scene(self.GAME_STATES[2])))
        self.menu_buttons.append(ttk.Button(self.canvas_menu, text = "Settings"))
        self.menu_buttons.append(ttk.Button(self.canvas_menu, text = "Quit", command=exit))

        for index, button in enumerate(self.menu_buttons):
            y= 273 + 60*index
            button.place(x="533",y=str(y),width="300", height="50")


    def initialise_game(self):
        self.segment_array = []

        self.head = Segment(100,400,self.canvas_game, 0)
        self.canvas_game.itemconfig(self.head.drawing, fill="green")
        self.segment_array.append(self.head)


        for i in range(10):
            self.segment_array.append(Segment(100 - 20 * len(self.segment_array),400,self.canvas_game, i + 1))
            self.head.canvas.lift(self.head.drawing) #Optional make head pop

        self.sea = self.canvas_game.create_line(0,200,1366,200, fill="Blue")

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
            self.switch_scene(self.GAME_STATES[0])
        elif(Key.keysym.lower() == "c"):
            coords = self.canvas_game.coords(self.segment_array[len(self.segment_array) - 1].drawing)
            self.segment_array.append(Segment(coords[0],coords[1],self.canvas_game, len(self.segment_array)))



    def game_loop(self):

        #Calculates difference in time between update loops and adjusts tick rate
        difference = (100/3) - ((perf_counter_ns() - self.previous_time)/1000000)
        self.tick_rate += round(difference)
        self.previous_time = perf_counter_ns()
        if self.current_game_state == self.GAME_STATES[2]:
            for segment in self.segment_array:
                segment.move_serpent(self.segment_array)
            self.root.after(self.tick_rate, self.game_loop)



#    def draw():

if __name__ == '__main__':
    Game().main_loop()
