class Mine:
    def __init__(self, x, y, canvas, src_image):
        self.drawing = canvas.create_image(x, y, image=src_image)
        self.canvas = canvas
        self.width = src_image.width() - 10
        self.height = src_image.height() - 10
