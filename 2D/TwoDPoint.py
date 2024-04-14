class TwoDPoint:
    
    #Constructeur
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def display_point(self):
        print("Point (", self.x, ",", self.y, ")")