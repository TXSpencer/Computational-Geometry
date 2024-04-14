from msilib.schema import Directory
from threading import stack_size
from Segment import Segment
from TwoDPoint import TwoDPoint
from Polygon import Polygon
import tkinter as tk

pointA = TwoDPoint(0,0)
pointB = TwoDPoint(0,5)
pointC = TwoDPoint(1,3)

segment1 = Segment(pointA, pointB)
segment2 = Segment(pointA, pointC)

#Function orientation

def orientation(segment1, segment2):
    res = 0
    x1 = segment1.get_B().get_x() - segment1.get_A().get_x()
    y1 = segment1.get_B().get_y() - segment1.get_A().get_y()
    x2 = segment2.get_B().get_x() - segment2.get_A().get_x()
    y2 = segment2.get_B().get_y() - segment2.get_A().get_y()
    #determinant
    det = x1*y2 - x2*y1 
    
    if(det>0):
        res = 1
    return res
    
def orientation_point(arete, point):
    res = 0
    x1 = arete.get_A().get_x() - point.get_x()
    y1 = arete.get_A().get_y() - point.get_y()
    
    x2 = arete.get_B().get_x() - point.get_x()
    y2 = arete.get_B().get_y() - point.get_y()

    det = x1*y2 - x2*y1
    if(det>0):
        res = 1
    return res

liste_points = []
liste_segment = []
liste_inside = []

#Fonction qui creer les points entré par l'utilisateur
def clique(event):
    X = event.x
    Y = event.y
    r = 3
    surface.create_rectangle(X-r,Y-r,X+r,Y+r,outline = 'black', fill = 'black')
    point = TwoDPoint(X,Y)
    if(len(liste_points) != 0):
        value = liste_points[-1]
        surface.create_line(value.get_x(), value.get_y(), X, Y, width = 2)
    liste_points.append(point)
    
def point(event):
    X = event.x
    Y = event.y
    r = 3
    surface.create_oval(X-r,Y-r,X+r,Y+r, outline = 'black', fill='black')
    point = TwoDPoint(X,Y)
    liste_inside.append(point)
    isInside()
    
#Création des segments à partir des points
def Create_Segment():

    surface.create_line(liste_points[0].get_x(), liste_points[0].get_y(), liste_points[-1].get_x(), liste_points[-1].get_y())
    for i in range(len(liste_points)):
        if(i != len(liste_points) - 1):
            segment = Segment(liste_points[i], liste_points[i+1])
            liste_segment.append(segment)
        else:
            segment = Segment(liste_points[i], liste_points[0])
            liste_segment.append(segment)

def isConvex():

    convexe = True
    if(len(liste_segment) == 0):
        print("Segment non crées!")
    else:
        for i in range(len(liste_segment)):
            if(i != len(liste_segment)-1):
                if(orientation(liste_segment[i], liste_segment[i+1])==0):
                    convexe = False
            else:
                if(orientation(liste_segment[i],liste_segment[0])==0):
                    convexe = False
        print("\nConvexe: " + str(convexe))
        
    if(convexe==True):
        #Methode pour recupérer la valeur du point avec le clic droit
        surface.bind('<Button-3>', point)
        surface.pack(padx = 5, pady = 5)

def isInside():
    res = 0
    for segment in  liste_segment:
        if(orientation_point(segment, liste_inside[-1]) == 1):
            res += 1
    if((res == len(liste_segment)) or (res==0)):
        print("Le point est à l'intérieur du polygone.")
    else:
        print("Le point est à l'exterieur du polygone.")

#Dimension fenêtre
LARGEUR = 480
HAUTEUR = 320

#Création de la fenêtre
geo_app = tk.Tk()
geo_app.title("Application géometrique")

#Création d'une zone graphique
surface = tk.Canvas(geo_app, width=LARGEUR, height=HAUTEUR, bg="white")
surface.pack(padx = 5, pady = 5)

#Méthode bind permet de lier le clique gauche à la fonction clique
surface.bind('<Button-1>', clique)
surface.pack(padx = 5, pady = 5)

#Permet de valider l'input des points
tk.Button(geo_app, text = 'Valider les points', command = Create_Segment).pack(side='left')

#Permet de checker la convexité du polygone
tk.Button(geo_app, text = 'Convex', command = isConvex).pack(side='left')

#Permet de quitter la fenêtre
tk.Button(geo_app, text = 'Quitter', command = geo_app.destroy).pack(side='right')

geo_app.mainloop()


#Convex Hull

#Dimension fenêtre
LARGEUR = 480
HAUTEUR = 350

#Création de la fenêtre
geo_app = tk.Tk()
geo_app.title("Convex Hull")

#Création d'une zone graphique
surface = tk.Canvas(geo_app, width=LARGEUR, height=HAUTEUR, bg="white")
surface.pack(padx = 5, pady = 5)

import random 
import time

lst_pts = []
lst_smg = []
lst_smg_hull = []

def CreateRandomPoints():
    for  i in range(10):
        r = 3
        x = random.randint(10,250)
        y = random.randint(10,250)
        p = TwoDPoint(x,y)
        lst_pts.append(p) 
        surface.create_oval(x-r,y-r,x+r,y+r, outline = 'black', fill='black')

def ExtremeEdges():
    for point in lst_pts:
        for points in lst_pts[:lst_pts.index(point)] + lst_pts[lst_pts.index(point)+1:]:
            segment = Segment(point,points)
            lst_smg.append(segment)
    
    for segment in lst_smg:
        surface.create_line(segment.get_A().get_x(), segment.get_A().get_y(), segment.get_B().get_x(), segment.get_B().get_y())
        time.sleep(0.1)
        surface.update()
        surface.create_line(segment.get_A().get_x(), segment.get_A().get_y(), segment.get_B().get_x(), segment.get_B().get_y(), fill="white")

        res = 0
        for point in lst_pts:
            if(orientation_point(segment,point) == 1):
                res+=1
        if(res == len(lst_pts)-2):
            lst_smg_hull.append(segment)

    for s in lst_smg_hull:
        s.display_segment()
        surface.create_line(s.get_A().get_x(),s.get_A().get_y(),s.get_B().get_x(),s.get_B().get_y())
        time.sleep(0.2)
        surface.update()

def Jarvis():
    #Point le plus à gauche
    a = min(lst_pts, key=lambda point: point.get_x())
    index = lst_pts.index(a)

    #Selection des points du ConvexHall
    l = index
    res = []
    res.append(a)

    while(True):
        q = (l+1) % len(lst_pts)
        for i in range(len(lst_pts)):
            if(i==l):
                continue
            s = Segment(lst_pts[l],lst_pts[i])
            surface.create_line(s.get_A().get_x(), s.get_A().get_y(), s.get_B().get_x(), s.get_B().get_y())
            time.sleep(0.1)
            surface.update()
            surface.create_line(s.get_A().get_x(), s.get_A().get_y(), s.get_B().get_x(), s.get_B().get_y(), fill="white")

            if(orientation_point(s,lst_pts[q])==1):
                q = i
        l = q
        if(l == index):
            break
        res.append(lst_pts[q])
    
    #Relier les points du ConvexHall par des lignes
    for i in range(len(res)): 
        if(i != len(res)-1):
            surface.create_line(res[i].get_x(),res[i].get_y(),res[i+1].get_x(),res[i+1].get_y())
            time.sleep(0.1)
            surface.update()
        else:
            surface.create_line(res[-1].get_x(), res[-1].get_y(), res[0].get_x(), res[0].get_y())
            time.sleep(0.1)
            surface.update()

def MostLeft(p) :
    pointAGauche = lst_pts[0]
    for pointCandidat in lst_pts :
        if (pointAGauche) == p or (orientation_point(Segment(p,pointAGauche),pointCandidat)==1) :
            pointAGauche = pointCandidat
    return (pointAGauche)

def Tri() :
    mini =  min(lst_pts, key=lambda point: point.get_x())
    T = []
    T.append(mini)
    i = 0
    while 0 != len(lst_pts) :
        if i != 0 :
            T.append(MostLeft(mini))
            lst_pts.remove(MostLeft(mini))
        i+=1
    return T

def Graham() :
    T = []
    TabTrie = []
    TabTrie = Tri()
    T.append(TabTrie[0])
    T.append(TabTrie[1])

    i=2
    while (i!=len(TabTrie)):
        while(len(T)>=2) and (orientation_point(Segment(T[len(T)-2],T[len(T)-1]),TabTrie[i])==1) :
            T.remove(T[len(T)-1])
        T.append(TabTrie[i])
        surface.create_line(TabTrie[i].get_x(),TabTrie[i].get_y(), TabTrie[i-1].get_x(), TabTrie[i-1].get_y())
        time.sleep(0.3)
        surface.update()
        surface.create_line(TabTrie[i].get_x(),TabTrie[i].get_y(), TabTrie[i-1].get_x(), TabTrie[i-1].get_y(), fill="white")
        i+=1

    for i in range(len(T)): 
        if(i != len(T)-1):
            surface.create_line(T[i].get_x(),T[i].get_y(),T[i+1].get_x(),T[i+1].get_y())
            time.sleep(0.1)
            surface.update()
        else:
            surface.create_line(T[-1].get_x(), T[-1].get_y(), T[0].get_x(), T[0].get_y())
            time.sleep(0.1)
            surface.update()

def clear():
    surface.delete("all")
    lst_pts.clear()
    lst_smg.clear()
    lst_smg_hull.clear()

#Selectionner la méthode Générer point
tk.Button(geo_app, text = 'Generate Points', command = CreateRandomPoints).pack(side='left')

#Selectionner la méthode Extreme Edges
tk.Button(geo_app, text = 'Extreme Edges', command = ExtremeEdges).pack(side='left')

#Selectionner la méthode Jarvis
tk.Button(geo_app, text = 'Jarvis', command = Jarvis).pack(side='left')

#Selectionner la méthode Jarvis
tk.Button(geo_app, text = 'Graham', command = Graham).pack(side='left')

#Permet de quitter la fenêtre
tk.Button(geo_app, text = 'Quitter', command = geo_app.destroy).pack(side='right')

#Permet de quitter la fenêtre
tk.Button(geo_app, text = 'Clear', command = clear).pack(side='right')

geo_app.mainloop()
                  

