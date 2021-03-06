# Resolution set to 1366x768
from tkinter import Tk, Canvas, ttk, StringVar, PhotoImage, Text
from time import perf_counter_ns
from random import randint, random
from math import floor
from serpent import Segment
from boat import Boat
from mine import Mine
import json


class Game:
    """docstring for Game."""
    tick_rate = 30
    GAME_STATES = ["main_menu", "pause", "in_game",
                   "dead", "leaderboard", "settings", "info"]
    boat_array = []
    mine_array = []
    segment_array = []
    key_binds = {"left": "a", "right": "d", "add_length": "0",
                 "escape": "escape", "boss_key": "b", "add_points": "9",
                 "remove_mine": "8", "add_boat": "7"}
    submitted = False
    boss_showing = False

    def __init__(self):
        # Creates game window
        self.root = Tk()
        self.root.title("Sea Serpant Game")
        self.root.geometry("1366x768")
        self.root.attributes("-fullscreen", True)

        # Loads all images to an array or variable
        self.boat_images = []
        self.boat_images.append(PhotoImage(file="Boat1.png"))
        self.boat_images.append(PhotoImage(file="Boat2.png"))
        self.boat_images.append(PhotoImage(file="Boat3.png"))
        # Mine image art from https://www.subpng.com/png-keknty/
        self.mine_image = PhotoImage(file="mine.png")
        # Info icon image from https://www.flaticon.com/free-icons/information
        self.info_image = PhotoImage(file="info.png")
        self.boss_key_image = PhotoImage(file="Boss-Key-Image.png")
        self.set_hotkey = "none"
        self.current_game_state = self.GAME_STATES[0]

        # Creates canvas' for each scene in the game
        self.canvas_game = Canvas(self.root, width="1366",
                                  height="768", bg="#add8e6")
        self.canvas_menu = Canvas(self.root, width="1366",
                                  height="768", bg="#add8e6")
        self.canvas_settings = Canvas(self.root, width="1366",
                                      height="768", bg="#add8e6")
        self.canvas_death_menu = Canvas(self.root, width="1366",
                                        height="768", bg="#add8e6")
        self.canvas_leaderboard = Canvas(self.root, width="1366",
                                         height="768", bg="#add8e6")
        self.canvas_pause_menu = Canvas(self.root, width="1366",
                                        height="768", bg="#add8e6")
        self.canvas_info = Canvas(self.root, width="1366",
                                  height="768", bg="#add8e6")

        self.initialise_info_menu()
        self.initialise_settings()
        self.initialise_menu()
        self.canvas_menu.pack()

        self.points = 0
        self.previous_time = perf_counter_ns()

    def switch_scene(self, next):
        """Switches between game states and initialises each menu"""
        # Checks current and next game step
        # Initialises next menu
        # Packs next canvas and forgets previous canvas

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
            elif next == "settings":
                self.canvas_menu.pack_forget()
                self.canvas_settings.pack()
            elif next == "info":
                self.canvas_menu.pack_forget()
                self.canvas_info.pack()
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
        elif self.current_game_state == "settings":
            if next == "main_menu":
                self.canvas_settings.pack_forget()
                self.canvas_menu.pack()
        elif self.current_game_state == "info":
            if next == "main_menu":
                self.canvas_info.pack_forget()
                self.canvas_menu.pack()
        self.current_game_state = next

    def initialise_menu(self):
        """Initialises the main menu"""
        self.root.config(cursor="sailboat")
        # Adds button to array and places them on canvas
        menu_buttons = []
        menu_buttons.append(ttk.Button(self.canvas_menu, text="Play Game",
                                       command=lambda:
                                       self.switch_scene(self.GAME_STATES[2])))
        menu_buttons.append(ttk.Button(self.canvas_menu, text="Leaderboard",
                                       command=lambda:
                                       self.switch_scene(self.GAME_STATES[4])))
        menu_buttons.append(ttk.Button(self.canvas_menu, text="Load Game",
                                       command=self.load_game))
        menu_buttons.append(ttk.Button(self.canvas_menu, text="Settings",
                                       command=lambda:
                                       self.switch_scene(self.GAME_STATES[5])))
        menu_buttons.append(ttk.Button(self.canvas_menu, text="Quit",
                                       command=exit))

        for index, button in enumerate(menu_buttons):
            y = 273 + 60 * index
            button.place(x="533", y=str(y), width="300", height="50")
        ttk.Button(self.canvas_menu, text="",
                   image=self.info_image,
                   command=lambda:
                       self.switch_scene(
                           self.GAME_STATES[6])).place(x="1311", y="5",
                                                       width="50", height="50")

    def initialise_settings(self):
        """Initialises the settings menu"""
        # Adds button to array and places them on canvas
        menu_buttons = []
        menu_buttons.append(ttk.Button(self.canvas_settings,
                                       text="Turn Left: <" +
                                       str(self.key_binds["left"]) + ">",
                                       command=lambda: self.set_key("left")))
        menu_buttons.append(ttk.Button(self.canvas_settings,
                                       text="Turn Right: <" +
                                       str(self.key_binds["right"]) + ">",
                                       command=lambda: self.set_key("right")))
        menu_buttons.append(ttk.Button(self.canvas_settings,
                                       text="Add Length: <" +
                                       str(self.key_binds["add_length"]) + ">",
                                       command=lambda:
                                       self.set_key("add_length")))
        menu_buttons.append(ttk.Button(self.canvas_settings, text="Return: <" +
                                       str(self.key_binds["escape"]) + ">",
                                       command=lambda: self.set_key("escape")))
        menu_buttons.append(ttk.Button(self.canvas_settings,
                                       text="Back to menu",
                                       command=lambda:
                                       self.switch_scene(self.GAME_STATES[0])))

        for index, button in enumerate(menu_buttons):
            y = 273 + 60 * index
            button.place(x="533", y=str(y), width="300", height="50")

    def set_key(self, key_bind):
        """Changes the key binds to the next key the user presses"""
        self.set_hotkey = key_bind
        self.canvas_settings.config(background="grey")

    def initialise_info_menu(self):
        ttk.Button(self.canvas_info,
                   text="Back to Main Menu",
                   command=lambda:
                   self.switch_scene(self.GAME_STATES[0])).place(x="533",
                                                                 y="600",
                                                                 width="300",
                                                                 height="50")
        ttk.Label(self.canvas_info,
                  text="Collect points by destroying boats\n"
                  "Avoid mines and your own tail\n"
                  "Hold A or D to turn\n"
                  "Press escape to return and B for boss key",
                  justify="center",
                  background="#add8e6",
                  font=("Arial", 40)).place(x="200", y="200")
        ttk.Label(self.canvas_info,
                  text="Cheat codes:\n"
                       "7 for add boat\n"
                       "8 for remove mine\n"
                       "9 for add points\n"
                       "0 for add length\n",
                  justify="center",
                  background="#add8e6",
                  font=("Arial",20)).place(x="1100",y="600")


    def initialise_pause_menu(self):
        """Initialises the pause screen"""
        # Adds button to array and places them on canvas
        self.root.config(cursor="sailboat")
        menu_buttons = []
        menu_buttons.append(ttk.Button(self.canvas_pause_menu,
                                       text="Resume",
                                       command=lambda:
                                       self.switch_scene(self.GAME_STATES[2])))
        menu_buttons.append(ttk.Button(self.canvas_pause_menu,
                                       text="Save Game",
                                       command=lambda:
                                       self.save_game(self.segment_array,
                                                      self.boat_array,
                                                      self.mine_array)))
        menu_buttons.append(ttk.Button(self.canvas_pause_menu,
                                       text="Back to Main Menu",
                                       command=lambda:
                                       self.switch_scene(self.GAME_STATES[0])))

        for index, button in enumerate(menu_buttons):
            y = 273 + 60 * index
            button.place(x="533", y=str(y), width="300", height="50")

    def initialise_death_screen(self):
        """Initialises the game over screen"""
        # Adds button to array and places them on canvas
        self.root.config(cursor="sailboat")
        menu_buttons = []
        menu_buttons.append(ttk.Button(self.canvas_death_menu,
                                       text="Play again?",
                                       command=lambda:
                                       self.switch_scene(self.GAME_STATES[2])))
        menu_buttons.append(ttk.Button(self.canvas_death_menu,
                                       text="Check leaderboard",
                                       command=lambda:
                                       self.switch_scene(self.GAME_STATES[4])))
        menu_buttons.append(ttk.Button(self.canvas_death_menu,
                                       text="Back to Main Menu",
                                       command=lambda:
                                       self.switch_scene(self.GAME_STATES[0])))
        for index, button in enumerate(menu_buttons):
            y = 473 + 60 * index
            button.place(x="533", y=str(y), width="300", height="50")

        game_over_label = ttk.Label(self.canvas_death_menu,
                                    text="GAME OVER",
                                    background="#add8e6",
                                    justify="center",
                                    font=("Arial", 100))
        game_over_label.place(x="300", y="50")
        score_label = ttk.Label(self.canvas_death_menu,
                                text="Score: " + str(self.points),
                                background="#add8e6",
                                justify="center",
                                font=("Arial", 70))
        score_label.place(x="500", y="300")

    def initialise_leaderboard_menu(self):
        """Initialises the leaderboard menu and loads leaderboard data"""
        # Adds button to array and places them on canvas
        menu_buttons = []
        menu_buttons.append(ttk.Button(self.canvas_leaderboard,
                                       text="Submit to leaderboard",
                                       command=lambda:
                                       self.submit_score(self.input_name.get(
                                                        "1.0", "end"),
                                                        self.points)))
        menu_buttons.append(ttk.Button(self.canvas_leaderboard,
                                       text="Back to Main Menu",
                                       command=lambda:
                                       self.switch_scene(self.GAME_STATES[0])))
        for index, button in enumerate(menu_buttons):
            y = 473 + 60 * index
            button.place(x="800", y=str(y), width="300", height="50")
        self.input_name = Text(self.canvas_leaderboard, width=20, height=1)
        self.input_name.configure(font=("Arial", 20))
        self.input_name.place(x="800", y="300")

        score_label = ttk.Label(self.canvas_leaderboard,
                                text="Score: " + str(self.points),
                                background="#add8e6",
                                justify="center",
                                font=("Arial", 70))
        score_label.place(x="500", y="50")
        ttk.Label(self.canvas_leaderboard, text="Username: ",
                  background="#add8e6",
                  font=("Arial", 20)).place(x="650", y="300")

        # Formats leaderboard data from json file to string
        leaderboard = json.load(open("leaderboard.json"))
        label_text = ""
        for key in leaderboard.keys():
            label_text += (f"{key}: {leaderboard[key]['name']}"
                           f" - {leaderboard[key]['score']}\n")
        # Creates label from string and places it on canvas
        self.leaderboard_label = ttk.Label(self.canvas_leaderboard,
                                           text=label_text,
                                           background="#add8e6",
                                           font=("Arial", 30))
        self.leaderboard_label.place(x="100", y="200")
        self.leaderboard_label.lower()

    def submit_score(self, name, score):
        """Adds current name and score to leaderboard"""
        name = name.strip()
        if name == "":
            return
        # Loads leaderboard data from json file
        # Iterates through each score and checks current score against it
        # If current score is larger, shift other scores downwards
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

        # Update Label for leaderboard
        label_text = ""
        for key in leaderboard.keys():
            label_text += (f"{key}: {leaderboard[key]['name']} "
                           f"- {leaderboard[key]['score']}\n")
        self.leaderboard_label["text"] = label_text
        self.leaderboard_label.lift()
        json.dump(leaderboard, open("leaderboard.json", "w"))

        self.submitted = True

    def initialise_game(self):
        """Sets up new game"""
        self.root.config(cursor="none")
        self.submitted = False
        self.points = 0
        self.points_counter = StringVar()
        self.points_counter.set(str(self.points))
        point_counter = ttk.Label(self.canvas_game,
                                  textvariable=self.points_counter,
                                  background="#add8e6",
                                  justify="center", font=("Arial", 40))
        point_counter.place(x="633", y="10", height="60")
        # Clears all arrays from previous games
        self.segment_array.clear()
        self.boat_array.clear()
        self.mine_array.clear()

        # Creates sea
        self.canvas_game.create_rectangle(0, 201, 1366, 768, fill="#86c5da")

        # Initialises the serpant and adds each segment to the array
        self.head = Segment(100, 400, self.canvas_game, 0)
        self.canvas_game.itemconfig(self.head.drawing, fill="green")
        self.segment_array.append(self.head)

        for i in range(10):
            self.segment_array.append(Segment(100 - 20 *
                                              len(self.segment_array),
                                      400, self.canvas_game, i + 1))
            self.head.canvas.lift(self.head.drawing)  # Optional make head pop

        self.canvas_game.create_line(0, 200, 1366, 200, fill="Blue")

    def save_game(self, segments, boats, mines):
        """Saves current game state to save_file.json"""
        segments_save = {}
        boats_save = {}
        mines_save = {}
        segments_save["direction"] = segments[0].direction
        # Enumerates through each segment adding its coordinates to a dictionary
        for index, segment in enumerate(segments):
            segments_save["x"+str(index)] = segment.canvas.coords(
                                            segment.drawing)[0]
            segments_save["y"+str(index)] = segment.canvas.coords(
                                            segment.drawing)[1]

        # Enumerates through each boat adding its coordinates to a dictionary
        for index, boat in enumerate(boats):
            boats_save["x"+str(index)] = boat.canvas.coords(boat.drawing)[0]
            boats_save["colour"+str(index)] = self.boat_images.index(
                                              boat.image)
            boats_save["speed"+str(index)] = boat.speed

        # Enumerates through each mine adding its coordinates to a dictionary
        for index, mine in enumerate(mines):
            mines_save["x"+str(index)] = mine.canvas.coords(mine.drawing)[0]
            mines_save["y"+str(index)] = mine.canvas.coords(mine.drawing)[1]

        # Combines all dictionaries into a single dictionary
        # Saves combined dictionary to a json file
        save = {}
        save["segments"] = segments_save
        save["boats"] = boats_save
        save["mines"] = mines_save
        save["points"] = self.points

        json.dump(save, open("save_file.json", "w"))

    def load_game(self):
        """loads a new game using game state stored in save_file.json"""
        save = json.load(open("save_file.json"))

        self.root.config(cursor="none")
        self.submitted = False
        # Adds point counter to top of screen
        self.points = save["points"]
        self.points_counter = StringVar()
        self.points_counter.set(str(self.points))
        point_counter = ttk.Label(self.canvas_game,
                                  textvariable=self.points_counter,
                                  background="#add8e6",
                                  justify="center", font=("Arial", 40))
        point_counter.place(x="633", y="10", height="60")

        # Clears arrays from previous games
        self.segment_array.clear()
        self.boat_array.clear()
        self.mine_array.clear()
        self.canvas_game.create_rectangle(0, 201, 1366, 768, fill="#86c5da")

        # Creates serpant from coordinates in save file
        keys = save.keys()
        self.head = Segment(save["segments"]["x0"],
                            save["segments"]["y0"], self.canvas_game, 0)
        self.head.direction = save["segments"]["direction"]
        self.canvas_game.itemconfig(self.head.drawing, fill="green")
        self.segment_array.append(self.head)

        for i in range(floor(len(save["segments"].keys())/2)):
            if i == 0:
                continue
            self.segment_array.append(Segment(save["segments"]["x"+str(i)],
                                              save["segments"]["y"+str(i)],
                                              self.canvas_game, i))
            self.head.canvas.lift(self.head.drawing)
        # Adds boats from coordinates in save file
        for i in range(floor(len(save["boats"].keys()) / 3)):
            self.boat_array.append(Boat(save["boats"]["x" + str(i)], 180,
                                        self.canvas_game,
                                        self.boat_images[save["boats"]
                                                             ["colour" +
                                                              str(i)]],
                                        save["boats"]["speed"+str(i)]))
        # Adds mines from coordinates in save file
        for i in range(floor(len(save["mines"].keys()) / 2)):
            self.mine_array.append(Mine(save["mines"]["x" + str(i)],
                                        save["mines"]["y" + str(i)],
                                        self.canvas_game,
                                        self.mine_image))

        self.canvas_game.create_line(0, 200, 1366, 200, fill="Blue")

        # sets current state to in game and restarts gameloop
        self.canvas_menu.pack_forget()
        self.canvas_game.pack()
        self.current_game_state = self.GAME_STATES[2]
        self.root.after(self.tick_rate, self.game_loop)

    def is_collided(self, x1, y1, x2, y2, h1, w1, h2, w2):
        """Checks if two rectangles are overlapping"""
        if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
            return True
        return False

    def main_loop(self):
        """Sets up game loop and tkinter loop"""
        self.root.after(self.tick_rate, self.game_loop)
        self.root.bind("<Key>", self.key_press)
        self.root.mainloop()

    def key_press(self, Key):
        """Controls how game responds to key presses depending on game state"""
        key = Key.keysym.lower()
        # If set_hotkey changes, a the key press is set to that hotkey
        if self.set_hotkey != "none":
            self.key_binds[self.set_hotkey] = key
            self.initialise_settings()
            self.canvas_settings.config(background="#add8e6")
            self.set_hotkey = "none"
        # Controls direction of serpant in game
        elif self.current_game_state == self.GAME_STATES[2]:
            if(key == self.key_binds["left"] and
                    self.head.canvas.coords(self.head.drawing)[1] > 200):
                self.head.direction -= 0.1
                self.head.velocity -= 0.1
            elif(key == self.key_binds["right"] and
                    self.head.canvas.coords(self.head.drawing)[1] > 200):
                self.head.direction += 0.1
                self.head.velocity -= 0.1
            elif(key == self.key_binds["add_length"]):
                coords = self.canvas_game.coords(self.segment_array[
                                    len(self.segment_array) - 1].drawing)
                self.segment_array.append(Segment(coords[0], coords[1],
                                                  self.canvas_game,
                                                  len(self.segment_array)))
                self.head.canvas.lift(self.head.drawing)
            elif(key == self.key_binds["add_points"]):
                self.points += 1000
            elif(key == self.key_binds["remove_mine"]):
                if(len(self.mine_array) > 0):
                    self.canvas_game.delete(self.mine_array[-1].drawing)
                    self.mine_array.remove(self.mine_array[-1])
            elif(key == self.key_binds["add_boat"]):
                self.boat_array.append(Boat(random() * 1366, 180,
                                            self.canvas_game,
                                            self.boat_images[randint(0, 2)],
                                            random() * 3 + 1))
            elif(key == self.key_binds["boss_key"]):
                self.switch_scene(self.GAME_STATES[1])
                self.boss_image = ttk.Label(self.canvas_pause_menu,
                                            image=self.boss_key_image)
                self.boss_image.place(x="0", y="0")
                self.boss_showing = True
        # Resets boss key image if pressed twice
        elif (self.current_game_state == self.GAME_STATES[1] and
                self.boss_showing and
                key == self.key_binds["boss_key"]):
            self.boss_showing = False
            self.boss_image.place_forget()
        # Either goes to pause, main menu, or exits depending on game state
        if(key == self.key_binds["escape"]):
            if self.current_game_state == self.GAME_STATES[0]:
                exit()
            elif self.current_game_state == self.GAME_STATES[2]:
                self.switch_scene(self.GAME_STATES[1])
            elif self.boss_showing:
                self.boss_showing = False
                self.boss_image.place_forget()
            else:
                self.switch_scene(self.GAME_STATES[0])

    def game_loop(self):
        """The loop used to control gameplay"""

        # Calculates difference in time between update loops
        # Adjusts tick rate depending on the difference
        difference = (100 / 3) - ((perf_counter_ns() -
                                  self.previous_time) / 1000000)
        self.tick_rate += round(difference)
        self.previous_time = perf_counter_ns()
        # Only does following code if in game
        if self.current_game_state != self.GAME_STATES[2]:
            return

        # Generates new boats if none are on screen. Maxed at 6 boats at a time
        if (len(self.boat_array) == 0 or
                (len(self.boat_array) < 6 and
                 randint(0, 200) == 1)):
            self.boat_array.append(Boat(random() * 1366, 180,
                                        self.canvas_game,
                                        self.boat_images[randint(0, 2)],
                                        random() * 3 + 1))

        # Randomly generates new mines. Maxed at 10 mines per game
        if (len(self.mine_array) < 11 and randint(0, 400) == 1):
            self.mine_array.append(Mine(random() * 1366,
                                        random() * 518 + 225,
                                        self.canvas_game,
                                        self.mine_image))
            # Checks if mine is placed on serpant. If so delete mine
            mine = self.mine_array[-1]
            for segment in self.segment_array:
                if self.is_collided(mine.canvas.coords(mine.drawing)[0] -
                                    mine.width / 2,
                                    mine.canvas.coords(mine.drawing)[1] -
                                    mine.height / 2,
                                    segment.canvas.coords(segment.drawing)[0],
                                    segment.canvas.coords(segment.drawing)[1],
                                    mine.height, mine.width,
                                    segment.radius, segment.radius):
                    self.canvas_game.delete(mine.drawing)
                    self.mine_array.remove(self.mine_array[-1])
                    break
        # Checks to see if boat is collided with the player
        # If so the boat is delete, points are added, and the serpant grows
        head = self.segment_array[0]
        for boat in self.boat_array:
            if self.is_collided(boat.canvas.coords(boat.drawing)[0] -
                                boat.width / 2,
                                boat.canvas.coords(boat.drawing)[1] -
                                boat.height / 2,
                                head.canvas.coords(head.drawing)[0],
                                head.canvas.coords(head.drawing)[1],
                                boat.height, boat.width,
                                head.radius, head.radius):
                self.boat_array.remove(boat)
                self.points += 1000

                tail_coords = self.canvas_game.coords(self.segment_array[
                                                      len(self.segment_array) -
                                                      1].drawing)
                for i in range(5):
                    self.segment_array.append(Segment(tail_coords[0],
                                                      tail_coords[1],
                                                      self.canvas_game,
                                                      len(self.segment_array)))

                boat.canvas.delete(boat.drawing)
                continue

            boat.move()
        # Checks to see if the head is collided with its body
        # If so the serpant dies and the player is taken to game over screen
        for index, segment in enumerate(self.segment_array):
            if index > 20 and self.is_collided(self.canvas_game.coords(
                                                   segment.drawing)[0],
                                               self.canvas_game.coords(
                                                   segment.drawing)[1],
                                               self.canvas_game.coords(
                                                   head.drawing)[0],
                                               self.canvas_game.coords(
                                                   head.drawing)[1],
                                               head.radius, head.radius,
                                               head.radius, head.radius):
                self.switch_scene(self.GAME_STATES[3])
                break
            segment.move_serpent(self.segment_array)

            # Checks to see if the head is collided with a mines
            # If so player dies and is taken to game over screen
            for mine in self.mine_array:
                if self.is_collided(mine.canvas.coords(mine.drawing)[0] -
                                    mine.width / 2,
                                    mine.canvas.coords(mine.drawing)[1] -
                                    mine.height / 2,
                                    segment.canvas.coords(segment.drawing)[0],
                                    segment.canvas.coords(segment.drawing)[1],
                                    mine.height, mine.width,
                                    segment.radius, segment.radius):
                    self.switch_scene(self.GAME_STATES[3])
                    break
            else:
                continue
            break

        # Points decrement over time
        if self.points > 0:
            self.points -= 1
        self.points_counter.set(str(self.points))

        self.root.after(self.tick_rate, self.game_loop)

if __name__ == '__main__':
    Game().main_loop()
