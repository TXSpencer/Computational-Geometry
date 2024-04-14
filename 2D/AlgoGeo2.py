from TwoDPoint import TwoDPoint
from Arete import Arete
from Triangle import Triangle

import tkinter as tk
from tkinter import *

import math

liste_point = []
liste_triangle = []
liste_arete = []

def orientation(arete, point):
    res = 0
    x1 = arete.get_point1().get_x() - point.get_x()
    y1 = arete.get_point1().get_y() - point.get_y()
    
    x2 = arete.get_point2().get_x() - point.get_x()
    y2 = arete.get_point2().get_y() - point.get_y()

    det = x1*y2 - x2*y1
    if(det>0):
        res = 1
    return res

def create_points(event):
    X = event.x
    Y = event.y
    r=5
    surface.create_oval(X-r,Y-r,X+r,Y+r, outline = 'black', fill='black')
    point = TwoDPoint(X,Y)
    if(len(liste_point)!=0):
        arete = Arete(liste_point[-1], point)
        liste_arete.append(arete)
        value = liste_point[-1]
        surface.create_line(value.get_x(), value.get_y(), X, Y, width=2)        
    liste_point.append(point)

def isInside(point):
    res = 0
    for arete in  liste_arete:
        if(orientation(arete, point) == 1):
            res += 1
    if((res == len(liste_arete)) or (res==0)):
        return True
import time

def NaiveTriangulation():
    point = liste_point[0]
    for i in range(1,len(liste_point)):
        surface.create_line(point.get_x(), point.get_y(), liste_point[i].get_x(), liste_point[i].get_y(), fill="blue")
        time.sleep(0.2)
        surface.update()
    for i in range(1,len(liste_point)-1):
        arete1 = Arete(point, liste_point[i])
        arete2 = Arete(liste_point[i], liste_point[i+1])
        arete3 = Arete(liste_point[i+1], point)
        triangle = Triangle(arete1,arete2,arete3)
        liste_triangle.append(triangle)
    print(len(liste_triangle))

def FindTriangle(point):
    
    for triangle in liste_triangle:
        liste_arete = []
        arete1 = triangle.get_arete1()
        liste_arete.append(arete1)
        arete2 = triangle.get_arete2()
        liste_arete.append(arete2)
        arete3 = triangle.get_arete3()
        liste_arete.append(arete3)
    
        res = 0
        for arete in liste_arete:
            if(orientation(arete,point) == 1):
                res+=1
        if(res == 3):
            return(triangle)

def InsertPoint(triangle, point):

    arete1 = triangle.get_arete1()
    arete2 = triangle.get_arete2()
    arete3 = triangle.get_arete3()

    surface.create_line(arete1.get_point1().get_x(), arete1.get_point1().get_y(), point.get_x(), point.get_y())
    surface.create_line(arete2.get_point1().get_x(), arete2.get_point1().get_y(), point.get_x(), point.get_y())
    surface.create_line(arete3.get_point1().get_x(), arete3.get_point1().get_y(), point.get_x(), point.get_y())

def last_line():
    surface.create_line(liste_point[-1].get_x(),liste_point[-1].get_y(), liste_point[0].get_x(),liste_point[0].get_y())

def newTriangle(t,p):

    arete1 = t.get_arete1()
    arete2 = Arete(arete1.get_point2(), p)
    arete3 = Arete(p, arete1.get_point1())
    triangle = Triangle(arete1,arete2,arete3)
    liste_triangle.append(triangle)

    arete1 = t.get_arete2()
    arete2 = Arete(arete1.get_point2(), p)
    arete3 = Arete(p, arete1.get_point1())
    triangle = Triangle(arete1,arete2,arete3)
    liste_triangle.append(triangle)

    arete1 = t.get_arete3()
    arete2 = Arete(arete1.get_point2(), p)
    arete3 = Arete(p, arete1.get_point1())
    triangle = Triangle(arete1,arete2,arete3)
    liste_triangle.append(triangle)
    
    i = liste_triangle.index(t)
    del liste_triangle[i]

def Delauney_Test(t,p):
    res=0
    x1 = t.get_arete1().get_point1().get_x() - p.get_x()
    x2 = t.get_arete1().get_point2().get_x() - p.get_x()
    x3 = t.get_arete2().get_point2().get_x() - p.get_x()

    y1 = t.get_arete1().get_point1().get_y() - p.get_y()
    y2 = t.get_arete1().get_point2().get_y() - p.get_y()
    y3 = t.get_arete2().get_point2().get_y() - p.get_y()

    z1 = math.pow(x1,2) + math.pow(y1,2)
    z2 = math.pow(x2,2) + math.pow(y2,2)
    z3 = math.pow(x3,2) + math.pow(y3,2)

    det = x1*y2*z3 + x2*y3*z1 + y1*z2*x3 - (x3*y2*z1 + x2*y1*z3 + x1*y3*z2)
    if(det>0):
        res=1 #inside
    return res

def getVoisin(t):
    lst_tri = []
    tmp_lst = liste_triangle.copy()

    a = t.get_arete1().get_point1()
    b = t.get_arete1().get_point2()
    c = t.get_arete2().get_point2()

    tmp_lst.remove(t)
    for triangle in tmp_lst:
        lst_p = []
        p1 = triangle.get_arete1().get_point1()
        p2 = triangle.get_arete1().get_point2()
        p3 = triangle.get_arete2().get_point2()    
        lst_p.append(p1)
        lst_p.append(p2)
        lst_p.append(p3)
        if((a in lst_p and b in lst_p) or (b in lst_p and c in lst_p) or (c in lst_p and a in lst_p)):
            lst_tri.append(triangle)

    return lst_tri            
           
def SlowDelaunay():
    for t in liste_triangle:

        liste_voisin = getVoisin(t)
        
        a = t.get_arete1().get_point1()
        b = t.get_arete1().get_point2()
        c = t.get_arete2().get_point2()
        lst1 = []
        lst1.extend([a,b,c])

        for voisin in liste_voisin:
            d = voisin.get_arete1().get_point1()
            e = voisin.get_arete1().get_point2()
            f = voisin.get_arete2().get_point2()
            lst2 = []
            lst2.extend([d,e,f])

            for p in lst1:
                if(p not in lst2):
                    tmp = p #point du triangle initial

            for p in lst2:
                if(p not in lst1):
                    point = p #point exterieur

            lst2.remove(point)
            seg = Arete(lst2[0], lst2[1]) #Segent commun

            res = Delauney_Test(t,point)
        
            if(res==1): #Si le point réside dans le cercle circonscrit à t1
                surface.create_line(seg.get_point1().get_x(), seg.get_point1().get_y(), seg.get_point2().get_x(), seg.get_point2().get_y(), fill="white")
                surface.create_line(tmp.get_x(),tmp.get_y(),point.get_x(), point.get_y(), fill="black")

                s = Arete(tmp,point) #nouveau segment
                arete1 = s
                arete2 = Arete(s.get_point2(),lst2[0])
                arete3 = Arete(lst2[0],tmp)
                t1 = Triangle(arete1,arete2,arete3)

                s = Arete(point,tmp)
                arete4 = s
                arete5 = Arete(tmp,lst2[1])
                arete6 = Arete(lst2[1],point)
                t2 = Triangle(arete4,arete5,arete6)

                liste_triangle.remove(voisin)
                liste_triangle.remove(t)
                liste_triangle.append(t1)
                liste_triangle.append(t2)
                
    
def getAngle(a,b,c):
    angle = math.degrees(math.atan2(c.get_y()-b.get_y(), c.get_x() - b.get_x()) - math.atan2(a.get_y()-b.get_y(), a.get_x() - b.get_x()))
    return -angle if angle < 0 else 360 - angle

def SlowDelaunayDraft():
    for i in range(len(liste_triangle)-1):
        
        #Delauney test
        t1 = liste_triangle[i]
        t2 = liste_triangle[i+1]
        
        a = t1.get_arete1().get_point1()
        b = t1.get_arete1().get_point2()
        c = t1.get_arete2().get_point2()
        d = t2.get_arete2().get_point2()

        sum_angles = getAngle(a,b,c) + getAngle(c,d,a)
        
        #Flip
        if(sum_angles>180):
            
            surface.create_line(a.get_x(),a.get_y(),c.get_x(),c.get_y(), fill="white") 
            surface.create_line(b.get_x(),b.get_y(),d.get_x(),d.get_y(), fill="black")
            
            arete1 = t1.get_arete1()
            arete2 = Arete(b,d)
            arete3 = t2.get_arete3()

            arete4 = t1.get_arete2()
            arete5 = t2.get_arete2()
            arete6 = Arete(d,b)

            t = Triangle(arete1,arete2,arete3)
            ind = liste_triangle.index(t1)
            del liste_triangle[ind]
            liste_triangle.insert(ind,t)

            t = Triangle(arete4,arete5,arete6)
            ind = liste_triangle.index(t2)
            del liste_triangle[ind]
            liste_triangle.insert(ind,t)
                
def selectionner_point(event):
    X = event.x
    Y = event.y
    r=3
    p = TwoDPoint(X,Y)

    #Je créer le segment qui relie le dernier point au premier
    if(len(liste_point)!=0):
        arete = Arete(liste_point[-1], liste_point[0])
        liste_arete.append(arete)
    
        if(isInside(p) == True):
            surface.create_oval(X-r,Y-r,X+r,Y+r, outline = 'black', fill='black')
            t = FindTriangle(p)
            InsertPoint(t, p)
            newTriangle(t, p)

import random
lst_pts = []

def CreateRandomPoints():
    for  i in range(10):
        r = 3
        x = random.randint(100,250)
        y = random.randint(100,250)
        p = TwoDPoint(x,y)
        lst_pts.append(p) 
        surface.create_oval(x-r,y-r,x+r,y+r, outline = 'black', fill='black')

def MetaTriangle():
    left = min(lst_pts, key=lambda point: point.get_x())
    right = max(lst_pts, key=lambda point: point.get_x())
    up = min(lst_pts, key=lambda point: point.get_y())
    down = max(lst_pts, key=lambda point: point.get_y())

    top_left_corner = TwoDPoint(left.get_x()-30, up.get_y()-30)
    top_right_corner = TwoDPoint(right.get_x()+30, up.get_y()-30)
    bot_left_corner = TwoDPoint(left.get_x()-30, down.get_y()+30)
    bot_right_corner = TwoDPoint(right.get_x()+30, down.get_y()+30)

    d1 = math.sqrt(math.pow((top_right_corner.get_x()-top_left_corner.get_x()),2) + math.pow((top_right_corner.get_y()-top_left_corner.get_y()),2))
    d2 = math.sqrt(math.pow((bot_left_corner.get_x()-top_left_corner.get_x()),2) + math.pow((bot_left_corner.get_y()-top_left_corner.get_y()),2))
    
    shift = abs(d2-d1)
    print(shift)
    
    surface.create_rectangle(top_left_corner.get_x(), top_left_corner.get_y(), bot_right_corner.get_x(), bot_right_corner.get_y())

    """ 
    surface.create_line(top_left_corner.get_x(),top_left_corner.get_y(), top_right_corner.get_x(), top_right_corner.get_y())
    surface.create_line(top_right_corner.get_x(), top_right_corner.get_y(), bot_right_corner.get_x(), bot_right_corner.get_y())
    surface.create_line(bot_right_corner.get_x(), bot_right_corner.get_y(), bot_left_corner.get_x(), bot_left_corner.get_y())
    surface.create_line(bot_left_corner.get_x(), bot_left_corner.get_y(), top_left_corner.get_x(), top_left_corner.get_y())
    """
    
def clear():
    surface.delete("all")
    liste_point.clear()
    liste_triangle.clear()
    liste_arete.clear()
    lst_pts.clear()

                                #Interface graphique 
#dimension fenêtre
LARGEUR = 480
HAUTEUR = 320

#Création de la fenêtre
triangle_app = tk.Tk()
triangle_app.title("Application Triangle")

#Création d'une zone graphique
surface = tk.Canvas(triangle_app, width=LARGEUR, height=HAUTEUR, bg="white")
surface.pack(padx = 5, pady = 5)

#Méthode bind permet de lier le clique gauche à la fonction clique
surface.bind('<Button-1>', create_points)
surface.pack(padx = 5, pady = 5)

#Méthode pour valider les points
tk.Button(triangle_app, text = 'Valider Points', command = last_line).pack(side='left')

#Méthode pour effectuer la triangulation naive
tk.Button(triangle_app, text = 'Naive', command = NaiveTriangulation).pack(side='left')

#Methode pour recupérer la valeur du point avec le clic droit
surface.bind('<Button-3>', selectionner_point)
surface.pack(padx = 5, pady = 5)

#Méthode 
tk.Button(triangle_app, text = 'SlowDelaunay', command = SlowDelaunay).pack(side='left')

#Selectionner la méthode Random Points
tk.Button(triangle_app, text = 'Create Random', command = CreateRandomPoints).pack(side='left')

#Creer le méta Square
tk.Button(triangle_app, text = 'Meta', command = MetaTriangle).pack(side='left')

#Permet de valider l'input et quitter la fenêtre
tk.Button(triangle_app, text = 'Quitter', command = triangle_app.destroy).pack(side='right')

#Permet de clear la surface
tk.Button(triangle_app, text = 'Clear', command = clear).pack(side='right')

triangle_app.mainloop()




