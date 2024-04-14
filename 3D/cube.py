from multiprocessing.spawn import prepare
from Vector4 import vec4
from Vector3 import vec3
from mat4 import mat4
from math import *
import pygame
import math

pygame.init()
WINDOW_SIZE = 800
window = pygame.display.set_mode( (WINDOW_SIZE,WINDOW_SIZE))
clock = pygame.time.Clock()

cube_points = [n for n in range(8)]
triangle_points = [n for n in range(4)]

#Points du cube
cube_points[0] = vec4(0,0,0,1)
cube_points[1] = vec4(1,0,0,1)
cube_points[2] = vec4(1,1,0,1)
cube_points[3] = vec4(0,1,0,1)
cube_points[4] = vec4(0,0,1,1)
cube_points[5] = vec4(1,0,1,1)
cube_points[6] = vec4(1,1,1,1)
cube_points[7] = vec4(0,1,1,1)

#Points du triangle
triangle_points[0] = vec4(0,0,0,1)
triangle_points[1] = vec4(1,0,0,1)
triangle_points[2] = vec4(0.5,1,0,1)
triangle_points[3] = vec4(0.5,0.5,1,1)

ws = 800
hs = 800
ns = 0
fs = 0
sx = 0
sy = 0

viewport_matrix = mat4(
                       vec4(ws/2,0,0,0),
                       vec4(0,hs/2,0,0),
                       vec4(0,0,(fs-ns)/2,0),
                       vec4(sx+(ws/2),sy+(hs/2),(ns+fs)/2,1)
                       )
                       
r = 2
l = -2
t = 2
b = -2
f = 2
n = -2

ortographic_projection_matrix = mat4(
                                    vec4(2/(r-l),0,0,0),
                                    vec4(0,2/(t-b),0,0),
                                    vec4(0,0,-2/(f-n),0),
                                    vec4(-(r+l)/(r-l),-(t+b)/(t-b),-(f+n)/(f-n),1)
                                    )

a = 1
n = 0.1
f = 1000
teta = 45
di = 1/(tan(teta/2))

perspective_projection_matrix = mat4(
                                    vec4(di/a,0,0,0),
                                    vec4(0,di,0,0),
                                    vec4(0,0,(n+f)/(n-f),-1),
                                    vec4(0,0,(2*n*f)/(n-f),0)
                                    ) 
fill = False
carre = False
triangle = False
ortographic = True
perspective = False

angle_x = angle_y = angle_z = tx = ty = tz = cam_angle_x = cam_angle_z = cam_angle_y = 0.0
sc = 1.0
res = 1
g=0.5
j=0.5

axes = [vec4(0,0,0,1),vec4(1.2,0,0,1),vec4(0,1.2,0,1),vec4(0,0,1.5,1)]

def connect_points(i,j,points):
    pygame.draw.line(window, (255,255,255), (points[i][0], points[i][1]), (points[j][0], points[j][1])) 

def GetEulerAngles():
    matrice = model_matrix.get_listeVecteur()
    sy = math.sqrt(matrice[0].get_x()*matrice[0].get_x() + matrice[0].get_y()*matrice[0].get_y())
    singular = sy<1e-6

    if(not singular):
        x = math.atan2(matrice[1].get_z(),matrice[2].get_z())
        y = math.atan2(-matrice[0].get_z(),sy)
        z = math.atan2(matrice[0].get_y(),matrice[0].get_x())
    else:
        x = math.atan2(-matrice[2].get_y(),matrice[1].get_y())
        y = math.atan2(-matrice[0].get_z(),sy)
        z = 0    
    return((round(x,2),round(y,2),round(z,2)))

while(True):
    clock.tick(60)
    window.fill((0,0,0))
    
    font = pygame.font.Font('freesansbold.ttf', 15)
    if(ortographic):
        text1 = font.render("state = ortographic", True, (255,255,255), (0,0,0))
    else:
        text1 = font.render("state = perspective", True, (255,255,255), (0,0,0))   

    textRect = text1.get_rect()
    textRect.center = (80, 20)
    window.blit(text1,textRect)

    #Roll
    rotation_x = mat4(
                        vec4(1,0,0,0),
                        vec4(0, cos(angle_x), sin(angle_x),0),
                        vec4(0, -sin(angle_x), cos(angle_x),0),
                        vec4(0,0,0,1)
                    )
    #Pitch
    rotation_y = mat4(
                        vec4(cos(angle_y), 0, -sin(angle_y),0),
                        vec4(0, 1, 0, 0),
                        vec4(sin(angle_y), 0, cos(angle_y),0),
                        vec4(0,0,0,1)
                    )
    #Yaw
    rotation_z = mat4(
                        vec4(cos(angle_z), sin(angle_z), 0, 0),
                        vec4(-sin(angle_z), cos(angle_z), 0, 0),
                        vec4(0,0,1,0),
                        vec4(0,0,0,1)
                    )
    
    cam_rotation_x = mat4(
                        vec4(1,0,0,0),
                        vec4(0, cos(cam_angle_x), sin(cam_angle_x),0),
                        vec4(0, -sin(cam_angle_x), cos(cam_angle_x),0),
                        vec4(0,0,0,1)
                    )

    cam_rotation_y = mat4(
                        vec4(cos(cam_angle_y), 0, -sin(cam_angle_y),0),
                        vec4(0, 1, 0, 0),
                        vec4(sin(cam_angle_y), 0, cos(cam_angle_y),0),
                        vec4(0,0,0,1)
                    )

    cam_rotation_z = mat4(
                        vec4(cos(cam_angle_z), sin(cam_angle_z), 0, 0),
                        vec4(-sin(cam_angle_z), cos(cam_angle_z), 0, 0),
                        vec4(0,0,1,0),
                        vec4(0,0,0,1)
                    )
    
    # Roll * Pitch * Yaw
    Euler_matrix = (rotation_x.mat_mat_mul(rotation_y)).mat_mat_mul(rotation_z)

    scale_matrix = mat4(
                        vec4(sc,0,0,0),
                        vec4(0,sc,0,0),
                        vec4(0,0,sc,0),
                        vec4(0,0,0,1)
                    ) 
    
    translation_matrix = mat4(
                              vec4(1,0,0,0),
                              vec4(0,1,0,0),
                              vec4(0,0,1,0),
                              vec4(tx,ty,tz,1)
                            )
                        
    model_matrix = translation_matrix.mat_mat_mul(scale_matrix.mat_mat_mul((rotation_z.mat_mat_mul(rotation_y.mat_mat_mul(rotation_x)))))

    d = vec3(0,0,-1)
    k = vec3(0,1,0)

    z = d.negative().division(d.length())
    x = d.cross(k).division((d.cross(k)).length())
    y = z.cross(x)
    
    tr = vec3(g,j,5)

    cam = mat4(
            vec4(x.get_x(),y.get_x(),z.get_x(),0),
            vec4(x.get_y(),y.get_y(),z.get_y(),0),
            vec4(x.get_z(),y.get_z(),z.get_z(),0),
            vec4(tr.get_x(),tr.get_y(),tr.get_z(),1)
            ) 

    if(carre == True):
        
        #Create origin axes
        pts = [0 for _ in range(len(axes))]
        i=0
        for axe in axes: 
            view_matrix = (cam_rotation_z.mat_mat_mul(cam_rotation_y.mat_mat_mul(cam_rotation_x))).mat_mat_mul(cam.inv())         
            point = viewport_matrix.mat_vec_mul(perspective_projection_matrix.mat_vec_mul((view_matrix.mat_vec_mul(axe))))
            point = point.perspective_div()
            pts[i] = (point.get_x(),point.get_y())
            i+=1

        pygame.draw.line(window, (255,0,0), (pts[0][0], pts[0][1]), (pts[1][0], pts[1][1])) 
        pygame.draw.line(window, (0,255,0), (pts[0][0], pts[0][1]), (pts[2][0], pts[2][1])) 
        pygame.draw.line(window, (0,0,255), (pts[0][0], pts[0][1]), (pts[3][0], pts[3][1])) 
            
        points = [0 for _ in range(len(cube_points))]
        i=0
        for point in cube_points:
            
            #Model Matrix: Translate - Scale - Rotate | Object Coordinate to World Coordinate
            point_2d = model_matrix.mat_vec_mul(point)

            #View Matrix
            view_matrix = (cam_rotation_z.mat_mat_mul(cam_rotation_y).mat_mat_mul(cam_rotation_x)).mat_mat_mul(cam.inv())
            pt = view_matrix.mat_vec_mul(point_2d)
            
            #Projection
            if(ortographic):
                p = ortographic_projection_matrix.mat_vec_mul(pt)
            else:
                p = perspective_projection_matrix.mat_vec_mul(pt)

            #Perspective division  
            p = p.perspective_div()

            #Viewport matrix
            f = viewport_matrix.mat_vec_mul(p)
            
            #Récupération des coordonnées x et y
            x = f.get_x()
            y = f.get_y()
            
            points[i] = (x,y)
            i += 1
            pygame.draw.circle(window, (0,0,255), (x,y), 2) 
        
        #Face1
        connect_points(0,4,points)
        connect_points(4,5,points)
        connect_points(5,0,points)
        connect_points(0,5,points)
        connect_points(5,1,points)
        connect_points(1,0,points)

        #Face2
        connect_points(1,5,points)
        connect_points(5,6,points)
        connect_points(6,1,points)
        connect_points(1,6,points)
        connect_points(6,2,points)
        connect_points(2,1,points)

        #Face3
        connect_points(2,6,points)
        connect_points(6,7,points)
        connect_points(7,2,points)
        connect_points(2,7,points)
        connect_points(7,3,points)
        connect_points(3,2,points)

        #Face4
        connect_points(3,7,points)
        connect_points(7,4,points)
        connect_points(4,3,points)
        connect_points(3,4,points)
        connect_points(4,0,points)
        connect_points(0,3,points)
        
        #Face5
        connect_points(5,4,points)
        connect_points(4,7,points)
        connect_points(7,5,points)
        connect_points(5,7,points)
        connect_points(7,6,points)
        connect_points(6,5,points)

        #Face6
        connect_points(1,0,points)
        connect_points(0,3,points)
        connect_points(3,1,points)
        connect_points(1,3,points)
        connect_points(3,2,points)
        connect_points(2,1,points)

        if(fill == True):
            pygame.gfxdraw.filled_polygon(window, [points[0],points[4],points[5]], (0,0,255))
            pygame.gfxdraw.filled_polygon(window, [points[0],points[5],points[1]], (0,0,255))
            pygame.gfxdraw.filled_polygon(window, [points[1],points[5],points[6]], (0,0,255))
            pygame.gfxdraw.filled_polygon(window, [points[1],points[6],points[2]], (0,0,255))
            pygame.gfxdraw.filled_polygon(window, [points[2],points[6],points[7]], (0,0,255))
            pygame.gfxdraw.filled_polygon(window, [points[2],points[7],points[3]], (0,0,255))
            pygame.gfxdraw.filled_polygon(window, [points[3],points[7],points[4]], (0,0,255))
            pygame.gfxdraw.filled_polygon(window, [points[3],points[4],points[0]], (0,0,255))
            pygame.gfxdraw.filled_polygon(window, [points[5],points[4],points[7]], (0,0,255))
            pygame.gfxdraw.filled_polygon(window, [points[5],points[7],points[6]], (0,0,255))
            pygame.gfxdraw.filled_polygon(window, [points[1],points[0],points[3]], (0,0,255))
            pygame.gfxdraw.filled_polygon(window, [points[1],points[3],points[2]], (0,0,255))

    if(triangle == True):
        points = [0 for _ in range(len(triangle_points))]
        i=0
        for point in triangle_points:

            #Rotate point
            rotate_x = rotation_x.mat_vec_mul(point)
            rotate_y = rotation_y.mat_vec_mul(rotate_x)
            rotate_z = rotation_z.mat_vec_mul(rotate_y)
            
            #Scale point
            scaled_point = scale_matrix.mat_vec_mul(rotate_z)

            #translated point
            translated_point = translation_matrix.mat_vec_mul(scaled_point)

            #print(translated_point.get_x(),"",translated_point.get_y(),"",translated_point.get_z(),"",translated_point.get_w())
            
            #Ortographic projection
            point_2d = translated_point

            #Récupération des coordonnées x et y
            x = (point_2d.get_x() * 100) + WINDOW_SIZE/2
            y = (point_2d.get_y() * 100) + WINDOW_SIZE/2
            points[i] = (x,y)
            i += 1
            pygame.draw.circle(window, (0,0,255), (x,y), 4) 

        def connect_points(i,j,points):
            pygame.draw.line(window, (255,255,255), (points[i][0], points[i][1]), (points[j][0], points[j][1]))  

        connect_points(0,1,points)
        connect_points(1,3,points)
        connect_points(3,0,points)

        connect_points(1,2,points)
        connect_points(2,3,points)
        connect_points(3,1,points)

        connect_points(2,0,points)
        connect_points(0,3,points)
        connect_points(3,2,points)

        connect_points(0,1,points)
        connect_points(1,2,points)
        connect_points(2,0,points)

    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
        
        keys = pygame.key.get_pressed()

        #Reset object
        if(keys[pygame.K_r]):
            angle_x = angle_y = angle_z = tx = ty = tz = 0
            sc = 1
            g = j = 0.5
            cam_angle_z = cam_angle_x = cam_angle_y = 0

        #Rotate cube
        if(keys[pygame.K_z]):
            angle_y += 0.05
            rotation_y.print()
            print(" ")
            print(GetEulerAngles())
            print(" ")
        if(keys[pygame.K_d]):
            angle_x += 0.05
            rotation_x.print()
            print(" ")
            print(GetEulerAngles())
            print(" ")
        if(keys[pygame.K_q]):
            angle_z += 0.05
            rotation_z.print()
            print(" ")
            print(GetEulerAngles())
            print(" ")

        #Scale cube
        if(keys[pygame.K_p]):
            sc += 0.05
        if(keys[pygame.K_m]):
            sc -= 0.05
        
        #Translate cube
        if(keys[pygame.K_LEFT]):
            tx -= 0.05
        if(keys[pygame.K_RIGHT]):
            tx += 0.05
        if(keys[pygame.K_UP]):
            ty -= 0.05
        if(keys[pygame.K_DOWN]):
            ty += 0.05

        #Translate cam
        if(keys[pygame.K_g]):
            g-=0.2
        if(keys[pygame.K_j]):
            g+=0.2
        if(keys[pygame.K_y]):
            j-=0.2
        if(keys[pygame.K_h]):
            j+=0.2

        #Rotate cam
        if(keys[pygame.K_v]):
            cam_angle_z+=0.1
        if(keys[pygame.K_KP_1]):
            cam_angle_x+=0.1
        if(keys[pygame.K_KP_2]):
            cam_angle_y+=0.1
        
        #Switch obejct
        if(keys[pygame.K_b]):
            triangle = False
            carre = True
        if(keys[pygame.K_n]):
            carre = False
            triangle = True
        
        #Toggle between ortographic and perspective
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_x):
                if(perspective == False):
                    ortographic = False
                    perspective = True
                elif(ortographic == False):
                    perspective = False
                    ortographic = True
        #Fill cube
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_SPACE):
                if(fill == False):
                    fill = True
                elif(fill == True):
                    fill = False

    pygame.display.update()

