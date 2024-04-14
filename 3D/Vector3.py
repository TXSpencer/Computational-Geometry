import math
from Vector4 import vec4

class vec3:

    #Constructeur
    def __init__(self, x , y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
    
    def get_z(self):
        return self.z

    def length(self):
        return(math.sqrt(math.pow(self.x,2) + math.pow(self.y,2) + math.pow(self.z,2)))

    def normalize(self):
        return vec3(self.x/self.length(), self.y/self.length(), self.z/self.length())

    def negative(self):
        return vec3(self.x*-1, self.y*-1,self.z*-1)
    
    def multiplication(self, k):
        return vec3(k*self.x, k*self.y, k*self.z)

    def division(self,k):
        return vec3(self.x/k,self.y/k,self.z/k)
        
    def addition(self, w):
        return vec3(self.x + w.get_x(), self.y + w.get_y(), self.z + w.get_z())
    
    def substraction(self, w):
        return vec3(self.x - w.get_x(), self.y - w.get_y(), self.z - w.get_z())
    
    def dot(self,w):
        return (self.x * w.get_x() + self.y * w.get_y() + self.z * w.get_z())

    def cross(self,w):
        return vec3(self.y*w.get_z() - self.z*w.get_y(), self.z*w.get_x() - self.x*w.get_z(), self.x*w.get_y() - self.y*w.get_x())
    
    def print(self):
        print("         |",self.x,"|")
        print("Vecteur: |",self.y,"|")
        print("         |",self.z,"|")

    def cart2hom(self):
        return vec4(self.x,self.y,self.z,1)
