#Resolution set to 1366x768
from tkinter import Tk, Canvas, ttk, StringVar, PhotoImage, Text
from time import perf_counter_ns
from random import randint,random
from serpent import *
from boat import *
import json #read json file. json.loads(txt) makes dictionary

class Game:
    """docstring for Game."""
    tick_rate = 30
    GAME_STATES = ["main_menu", "pause", "in_game", "dead", "leaderboard"]
    boat_array = []
    segment_array = []
    submitted = False
    def __init__(self):
        self.root = Tk()
        self.root.title("Sea Serpant Game")
        self.root.geometry("1366x768")
        self.root.attributes("-fullscreen", True)

        self.boat_image = PhotoImage(file="Boat1.png") #TODO: Add more boat sprites to an array. Make it randomly choose the sprite

        self.current_game_state = self.GAME_STATES[0]

        self.canvas_game = Canvas(self.root, width="1366", height="768")
        self.canvas_menu = Canvas(self.root, width="1366", height="768")
        self.canvas_death_menu = Canvas(self.root, width="1366", height="768")
        self.canvas_leaderboard = Canvas(self.root, width="1366", height="768")
        self.canvas_pause_menu = Canvas(self.root, width="1366", height="768")

        self.initialise_menu()
        self.canvas_menu.pack()

        self.points = 0
        self.previous_time = perf_counter_ns()

    def switch_scene(self, next):

        if self.current_game_state == "main_menu":
            if next == "in_game":
                self.canvas_menu.pack_forget()
                self.initialise_game()
                self.canvas_game.pack()
                self.root.after(self.tick_rate, self.game_loop)
            elif next == "leaderboard":
                self.canvas_menu.pack_forget()
                self.canvas_leaderboard.delete("all")
                self.initialise_leaderboard_menu()
                self.canvas_leaderboard.pack()

        elif self.current_game_state == "in_game":
            if next == "pause":
                self.initialise_pause_menu()
                self.canvas_game.pack_forget()
                self.canvas_pause_menu.pack()
            elif next == "dead":
                self.canvas_game.pack_forget()
                self.canvas_game.delete("all")
                self.initialise_death_screen()
                self.canvas_death_menu.pack()
        elif self.current_game_state == "dead":
            if next == "main_menu":
                self.canvas_death_menu.pack_forget()
                self.canvas_death_menu.delete("all")
                self.canvas_menu.pack()
            elif next == "in_game":
                self.canvas_death_menu.pack_forget()
                self.canvas_death_menu.delete("all")
                self.initialise_game()
                self.canvas_game.pack()
                self.root.after(self.tick_rate, self.game_loop)
            elif next == "leaderboard":
                self.canvas_death_menu.pack_forget()
                self.canvas_death_menu.delete("all")
                self.initialise_leaderboard_menu()
                self.canvas_leaderboard.pack()
        elif self.current_game_state == "leaderboard":
            if next == "main_menu":
                self.canvas_leaderboard.pack_forget()
                self.canvas_leaderboard.delete("all")
                self.canvas_menu.pack()
        elif self.current_game_state == "pause":
            if next == "in_game":
                self.canvas_pause_menu.pack_forget()
                self.canvas_pause_menu.delete("all")
                self.canvas_game.pack()
                self.root.after(self.tick_rate, self.game_loop)
            if next == "main_menu":
                self.canvas_game.delete("all")
                self.canvas_game.pack_forget()
                self.canvas_pause_menu.delete("all")
                self.canvas_pause_menu.pack_forget()
                self.canvas_menu.pack()

        self.current_game_state = next

    def initialise_menu(self):
        self.root.config(cursor = "sailboat")
        menu_buttons = []
        menu_buttons.append(ttk.Button(self.canvas_menu, text = "Play game", command=lambda: self.switch_scene(self.GAME_STATES[2])))
        menu_buttons.append(ttk.Button(self.canvas_menu, text = "Leaderboard", command=lambda: self.switch_scene(self.GAME_STATES[4])))
        menu_buttons.append(ttk.Button(self.canvas_menu, text = "Settings"))
        menu_buttons.append(ttk.Button(self.canvas_menu, text = "Quit", command=exit))

        for index, button in enumerate(menu_buttons):
            y = 273 + 60 * index
            button.place(x="533", y = str(y), width = "300", height = "50")
    def initialise_pause_menu(self):
        self.root.config(cursor = "sailboat")
        menu_buttons = []
        menu_buttons.append(ttk.Button(self.canvas_pause_menu, text = "Resume", command=lambda: self.switch_scene(self.GAME_STATES[2])))
        menu_buttons.append(ttk.Button(self.canvas_pause_menu, text = "Save Game"))
        menu_buttons.append(ttk.Button(self.canvas_pause_menu, text = "Back to Main Menu", command=lambda: self.switch_scene(self.GAME_STATES[0])))

        for index, button in enumerate(menu_buttons):
            y = 273 + 60 * index
            button.place(x="533", y = str(y), width = "300", height = "50")

    def initialise_death_screen(self):
        self.root.config(cursor = "sailboat")
        menu_buttons = []
        menu_buttons.append(ttk.Button(self.canvas_death_menu, text = "Play again?", command=lambda: self.switch_scene(self.GAME_STATES[2])))
        menu_buttons.append(ttk.Button(self.canvas_death_menu, text = "Check leaderboard", command = lambda: self.switch_scene(self.GAME_STATES[4])))
        menu_buttons.append(ttk.Button(self.canvas_death_menu, text = "Back to Main Menu",command = lambda: self.switch_scene(self.GAME_STATES[0])))
        for index, button in enumerate(menu_buttons):
            y = 473 + 60 * index
            button.place(x="533", y = str(y), width = "300", height = "50")

        game_over_label = ttk.Label(self.canvas_death_menu, text = "GAME OVER", justify="center", font=("Arial",100))
        game_over_label.place(x="300", y="50")
        score_label = ttk.Label(self.canvas_death_menu, text = "Score: " + str(self.points), justify="center", font=("Arial",70))
        score_label.place(x="500",y="300")

    def initialise_leaderboard_menu(self):
        menu_buttons = []
        menu_buttons.append(ttk.Button(self.canvas_leaderboard, text = "Submit to leaderboard",command=lambda: self.submit_score(self.input_name.get("1.0","end"),self.points)))
        menu_buttons.append(ttk.Button(self.canvas_leaderboard, text = "Back to Main Menu",command = lambda: self.switch_scene(self.GAME_STATES[0])))
        for index, button in enumerate(menu_buttons):
            y = 473 + 60 * index
            button.place(x="533", y = str(y), width = "300", height = "50")
        self.input_name = Text(self.canvas_leaderboard, width = 40, height = 1)
        self.input_name.place(x="700",y="400")

        score_label = ttk.Label(self.canvas_leaderboard, text = "Score: " + str(self.points), justify="center", font=("Arial",70))
        score_label.place(x="500",y="50")

        leaderboard = json.load(open("leaderboard.json"))
        label_text = ""
        for key in leaderboard.keys():
            label_text += f"{key}: {leaderboard[key]['name']} - {leaderboard[key]['score']}\n"
        self.leaderboard_label = ttk.Label(self.canvas_leaderboard, text = label_text, font=("Arial",30))
        self.leaderboard_label.place(x="200",y="300")
        self.leaderboard_label.lower()
    def submit_score(self, name, score): # TODO: on second submit, score doesnt update.
        name = name.strip()
        leaderboard = json.load(open("leaderboard.json"))
        for key in leaderboard.keys():
            if score <= int(leaderboard[key]["score"]) or self.submitted:
                continue
            tmp_score = int(leaderboard[key]["score"])
            tmp_name = leaderboard[key]["name"]
            leaderboard[key]["score"] = str(score)
            leaderboard[key]["name"] = name
            score = tmp_score
            name = tmp_name

        label_text = ""
        for key in leaderboard.keys():
            label_text += f"{key}: {leaderboard[key]['name']} - {leaderboard[key]['score']}\n"
        self.leaderboard_label["text"] = label_text
        json.dump(leaderboard,open("leaderboard.json","w"))

        self.submitted = True

    def initialise_game(self):
        self.root.config(cursor = "none")
        self.submitted = False
        self.points = 0
        self.points_counter = StringVar()
        self.points_counter.set(str(self.points))
        point_counter = ttk.Label(self.canvas_game, textvariable = self.points_counter, justify="center", font=("Arial",40))
        point_counter.place(x="633",y="10", height="60")


        self.segment_array.clear()
        self.boat_array.clear()


        self.head = Segment(100,400,self.canvas_game, 0)
        self.canvas_game.itemconfig(self.head.drawing, fill="green")
        self.segment_array.append(self.head)


        for i in range(10):
            self.segment_array.append(Segment(100 - 20 * len(self.segment_array),400,self.canvas_game, i + 1))
            self.head.canvas.lift(self.head.drawing) #Optional make head pop

        self.sea = self.canvas_game.create_line(0,200,1366,200, fill="Blue")

    def is_collided(self, x1, y1, x2, y2, h1, w1, h2, w2):
        if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
            return True
        return False
        coords_a = a.canvas.coords(a.drawing)
        coords_b = b.canvas.coords(b.drawing)
        coords_a[0] -= a.width/2
        coords_a[1] -= a.height/2
        if coords_a[0] < coords_b[2] and coords_a[0] + a.width > coords_b[0] and coords_a[1] < coords_b[3] and coords_a[1] + a.height > coords_b[1]:
            return True
        return False

    def main_loop(self):
        self.root.after(self.tick_rate, self.game_loop)
        self.root.bind("<Key>", self.key_press)
        self.root.mainloop()

    def key_press(self, Key):
        if self.current_game_state == self.GAME_STATES[2]:
            if(Key.keysym.lower() == "a" and self.head.canvas.coords(self.head.drawing)[1] > 200):
                self.head.direction -= 0.1
                self.head.velocity -= 0.1
            elif(Key.keysym.lower() == "d" and self.head.canvas.coords(self.head.drawing)[1] > 200):
                self.head.direction += 0.1
                self.head.velocity -= 0.1
            elif(Key.keysym.lower() == "c"):
                coords = self.canvas_game.coords(self.segment_array[len(self.segment_array) - 1].drawing)
                self.segment_array.append(Segment(coords[0],coords[1],self.canvas_game, len(self.segment_array)))
                self.head.canvas.lift(self.head.drawing) #Optional make head pop

        if(Key.keysym == "Escape"):
            if self.current_game_state == self.GAME_STATES[0]:
                exit()
            elif self.current_game_state == self.GAME_STATES[2]:
                self.switch_scene(self.GAME_STATES[1])
            else:
                self.switch_scene(self.GAME_STATES[0])

    def game_loop(self):
        # print(self.current_game_state)
        # self.points += 1
        # self.points_counter.set(str(self.points))

        #Calculates difference in time between update loops and adjusts tick rate
        difference = (100/3) - ((perf_counter_ns() - self.previous_time)/1000000)
        self.tick_rate += round(difference)
        self.previous_time = perf_counter_ns()

        if self.current_game_state != self.GAME_STATES[2]:
            return

        if len(self.boat_array) == 0 or (len(self.boat_array) < 5 and randint(0,200) == 1):
            self.boat_array.append(Boat(random()*1366,180,self.canvas_game, self.boat_image, random()*3+1))


        head = self.segment_array[0]

        for boat in self.boat_array:
            if self.is_collided(boat.canvas.coords(boat.drawing)[0]-boat.width/2,
                                boat.canvas.coords(boat.drawing)[1]-boat.height/2,
                                head.canvas.coords(head.drawing)[0],
                                head.canvas.coords(head.drawing)[1],
                                boat.height, boat.width,
                                head.radius, head.radius):
                self.boat_array.remove(boat)
                self.points += 1000

                tail_coords = self.canvas_game.coords(self.segment_array[len(self.segment_array)-1].drawing)
                for i in range (5):
                    self.segment_array.append(Segment(tail_coords[0],tail_coords[1],self.canvas_game, len(self.segment_array)))

                boat.canvas.delete(boat.drawing)
                continue

            boat.move()

        for index, segment in enumerate(self.segment_array):
            if index > 20 and self.is_collided(  self.canvas_game.coords(segment.drawing)[0],
                                                self.canvas_game.coords(segment.drawing)[1],
                                                self.canvas_game.coords(head.drawing)[0],
                                                self.canvas_game.coords(head.drawing)[1],
                                                head.radius, head.radius, head.radius, head.radius):
                self.switch_scene(self.GAME_STATES[3])
                break

            segment.move_serpent(self.segment_array)

        if self.points > 0:
            self.points -= 1
        self.points_counter.set(str(self.points))

        self.root.after(self.tick_rate, self.game_loop)


#    def draw():

if __name__ == '__main__':
    Game().main_loop()
