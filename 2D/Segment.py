class Segment:
    
    #Constructeur
    def __init__(self, A, B):
        self.A = A
        self.B = B
    
    def get_A(self):
        return self.A
    
    def get_B(self):
        return self.B

    def display_segment(self):
        print("[(",self.A.get_x(),",",self.A.get_y(),");(",self.B.get_x(),",",self.B.get_y(),")]")
