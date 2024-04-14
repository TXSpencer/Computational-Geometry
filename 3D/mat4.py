from Vector4 import vec4
import numpy as np

class mat4:

    def __init__(self,v1,v2,v3,v4):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.v4 = v4
        self.listeVecteur = [v1,v2,v3,v4]
    
    def get_v1(self):
        return self.v1
    
    def get_v2(self):
        return self.v2

    def get_v3(self):
        return self.v3

    def get_v4(self):
        return self.v4
    
    def get_listeVecteur(self):
        return self.listeVecteur
    
    def somme(self,m):
        res = mat4(
            vec4(self.get_v1().get_x() + m.get_v1().get_x(),self.get_v1().get_y() + m.get_v1().get_y(), self.get_v1().get_z() + m.get_v1().get_z(),self.get_v1().get_w() + m.get_v1().get_w()),
            vec4(self.get_v2().get_x() + m.get_v2().get_x(),self.get_v2().get_y() + m.get_v2().get_y(), self.get_v2().get_z() + m.get_v2().get_z(),self.get_v2().get_w() + m.get_v2().get_w()),
            vec4(self.get_v3().get_x() + m.get_v3().get_x(),self.get_v3().get_y() + m.get_v3().get_y(), self.get_v3().get_z() + m.get_v3().get_z(),self.get_v3().get_w() + m.get_v3().get_w()),
            vec4(self.get_v4().get_x() + m.get_v4().get_x(),self.get_v4().get_y() + m.get_v4().get_y(), self.get_v4().get_z() + m.get_v4().get_z(),self.get_v4().get_w() + m.get_v4().get_w())
        )
        return res
    
    def scalar_mul(self,k): 
        matrice = mat4(self.v1.multiplication(k), self.v2.multiplication(k), self.v3.multiplication(k), self.v4.multiplication(k))
        return matrice
        
    def mat_vec_mul(self,vecteur):
        res = vec4(
            self.v1.get_x() * vecteur.get_x() + self.v2.get_x() * vecteur.get_y() + self.v3.get_x() * vecteur.get_z() + self.v4.get_x() * vecteur.get_w(),
            self.v1.get_y() * vecteur.get_x() + self.v2.get_y() * vecteur.get_y() + self.v3.get_y() * vecteur.get_z() + self.v4.get_y() * vecteur.get_w(),
            self.v1.get_z() * vecteur.get_x() + self.v2.get_z() * vecteur.get_y() + self.v3.get_z() * vecteur.get_z() + self.v4.get_z() * vecteur.get_w(),
            self.v1.get_w() * vecteur.get_x() + self.v2.get_w() * vecteur.get_y() + self.v3.get_w() * vecteur.get_z() + self.v4.get_w() * vecteur.get_w()
        )
        return res

    def mat_mat_mul(self,matrice):
        
        liste_vecteur = matrice.get_listeVecteur()

        v1 = self.mat_vec_mul(liste_vecteur[0])
        v2 = self.mat_vec_mul(liste_vecteur[1])
        v3 = self.mat_vec_mul(liste_vecteur[2])
        v4 = self.mat_vec_mul(liste_vecteur[3])

        return mat4(v1,v2,v3,v4)

    def print(self):
        print("|",self.v1.get_x()," ", self.v2.get_x()," ", self.v3.get_x()," ",self.v4.get_x(),"|")
        print("|",self.v1.get_y()," ", self.v2.get_y()," ", self.v3.get_y()," ",self.v4.get_y(),"|")
        print("|",self.v1.get_z()," ", self.v2.get_z()," ", self.v3.get_z()," ",self.v4.get_z(),"|")
        print("|",self.v1.get_w()," ", self.v2.get_w()," ", self.v3.get_w()," ",self.v4.get_w(),"|")

    def inv(self):
        liste_vecteur = self.get_listeVecteur()

        v1 = []
        v1.append(liste_vecteur[0].get_x())
        v1.append(liste_vecteur[0].get_y())
        v1.append(liste_vecteur[0].get_z())
        v1.append(liste_vecteur[0].get_w())

        v2 = []
        v2.append(liste_vecteur[1].get_x())
        v2.append(liste_vecteur[1].get_y())
        v2.append(liste_vecteur[1].get_z())
        v2.append(liste_vecteur[1].get_w())

        v3 = []
        v3.append(liste_vecteur[2].get_x())
        v3.append(liste_vecteur[2].get_y())
        v3.append(liste_vecteur[2].get_z())
        v3.append(liste_vecteur[2].get_w())

        v4 = []
        v4.append(liste_vecteur[3].get_x())
        v4.append(liste_vecteur[3].get_y())
        v4.append(liste_vecteur[3].get_z())
        v4.append(liste_vecteur[3].get_w())

        A = np.array((v1,v2,v3,v4))
        A_inv = np.linalg.inv(A)

        a = vec4(A_inv[0][0], A_inv[0][1], A_inv[0][2], A_inv[0][3])
        b = vec4(A_inv[1][0], A_inv[1][1], A_inv[1][2], A_inv[1][3])
        c = vec4(A_inv[2][0], A_inv[2][1], A_inv[2][2], A_inv[2][3])
        d = vec4(A_inv[3][0], A_inv[3][1], A_inv[3][2], A_inv[3][3])

        return mat4(a,b,c,d)
