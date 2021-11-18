class Boat(object):
    """docstring for Boat."""

    def __init__(self, x, y, canvas, src_image):
        self.drawing = canvas.create_image(x,y,image = src_image)
