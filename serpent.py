from math import pi, sin, cos, atan2, sqrt

class Segment:
    """docstring for Segment."""
    radius = 50
    acceleration = 1
    max_velocity = 8
    velocity = 0
    x_velocity = 0
    y_velocity = 0

    direction = 0
    GRAVITY = 0.15

    def __init__(self, x, y, canvas, id):
        self.drawing = canvas.create_oval(x, y, self.radius + x, self.radius + y, fill="blue")
        self.canvas = canvas
        self.id = id

    def move_serpent(self, segment_array):
        current_coords = self.canvas.coords(self.drawing)
        #print(current_coords)
        if current_coords[0] < 0:
            self.canvas.coords(self.drawing, 0, current_coords[1], self.radius, current_coords[1] + self.radius)
            self.direction = 0
        elif current_coords[0] + self.radius > 1366:
            self.canvas.coords(self.drawing, 1366 - self.radius, current_coords[1], 1366, current_coords[1] + self.radius)
            self.direction = pi
        elif current_coords[1] + self.radius > 768:
            self.canvas.coords(self.drawing, current_coords[0], 768 - self.radius, current_coords[0] + self.radius, 768)
            self.direction = 1.5 * pi

        if self.id != 0:
            prev = segment_array[self.id - 1].canvas.coords(segment_array[self.id - 1].drawing)
            vector = (prev[0] - current_coords[0], prev[1] - current_coords[1])
            x_change = prev[0] - current_coords[0]
            new_direction = atan2(vector[1], vector[0])
            self.direction = new_direction

            #Adjust speed
            distance = sqrt(vector[0]**2 + vector[1]**2)
            if distance > 30:
                self.max_velocity =  9 #Max Vel at 8
            elif distance < 4:
                self.max_velocity = 0
            elif distance < 10:
                self.max_velocity = 3
            elif distance < 20:
                self.max_velocity = 6
            else:
                self.max_velocity = 8

    #                print(segment.velocity)
        if current_coords[1] > 200 or self.id != 0:
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
