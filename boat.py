class Boat(object):
    """docstring for Boat."""
    direction = 0 #0 for right, 1 for left
    speed = 2;
    def __init__(self, x, y, canvas, src_image, speed):
        self.drawing = canvas.create_image(x,y,image = src_image)
        self.width = src_image.width()
        self.height = src_image.height()
        self.canvas = canvas
        self.speed = speed
        
    def move(self):
        if self.canvas.coords(self.drawing)[0] > 1341:
            self.direction = 1
        elif self.canvas.coords(self.drawing)[0] < 25:
            self.direction = 0
        self.canvas.move(self.drawing,-1 * self.direction * 2 * self.speed + self.speed, 0)
