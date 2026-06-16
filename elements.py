import numpy as np
import math

'''''
En este script se definen los elementos de maquinas orientados a objetos.
'''''

class Elemento:

    theta_deg = np.linspace(20, 60, 4)
    theta = np.radians(theta_deg)

    def __init__(self, nombre, material, E, Sy, P=20000, Sut=None, Ssy=None):
        self.nombre = nombre
        self.material = material
        self.E = E #Usar en Pa
        self.Sy = Sy #Usar en Pa
        self.Sut = Sut #Usar en Pa
        self.Ssy = Ssy if Ssy != None else 0.577*Sy 
        self.P = P #Usar en N
    
    def carga_interna(self):

        raise NotImplementedError

    def esfuerzo_critico(self):

        raise NotImplementedError
    
    def factor_seguridad(self):

        raise NotImplementedError

class Brazo(Elemento):
    def __init__(self, nombre, material, E, Sy, A, I, L, d, t, K=1.0, tension=False):
        self.A = A                # area transversal              m^2
        self.I = I                # momento de inercia mínimo     m^4
        self.L = L                # longitud del brazo            m
        self.d = d                # diametro del hueco            m
        self.t = t                # espesor de la placa del brazo m
        self.K = K               
        self.tension = tension
    
    def carga_interna(self):
        F = self.P / (2 * np.sin(self.theta))
        return F if self.tension else -F  
    
        
    def esfuerzo_axial(self):

        return np.abs(self.carga_interna()) / self.A
 
    def area_neta(self):
        
        return self.A - self.d * self.t
 
    def esfuerzo_tension_neta(self):
       
        return np.abs(self.carga_interna()) / self.area_neta()
 
    def esfuerzo_aplastamiento(self):
       
        return np.abs(self.carga_interna()) / (self.t * self.d)
 
    def esfuerzo_critico(self):
        if self.tension:
            return np.maximum(self.esfuerzo_tension_neta(),
                              self.esfuerzo_aplastamiento())
        return np.maximum(self.esfuerzo_axial(),
                          self.esfuerzo_aplastamiento())
 

    if tension == False:
        
        def radio_giro(self):
            return np.sqrt(self.I / self.A)                
    
        def esbeltez(self):
            return self.K * self.L / self.radio_giro()     
    
        def constante_columna(self):
            
            return np.sqrt(2 * np.pi**2 * self.E / self.Sy)
    
        def carga_critica_johnson(self):
            
            return self.A * self.Sy * (
                1 - self.Sy * self.esbeltez()**2 / (4 * np.pi**2 * self.E)
            )
    
        def carga_critica_euler(self):
            
            return (np.pi**2 * self.E * self.I) / (self.K * self.L)**2
        
        def factor_seguridad(self):
            F = np.abs(self.carga_interna())
            return {
            "pandeo_johnson":        self.carga_critica_johnson() / F,   
            "fluencia_compresion":   self.Sy / self.esfuerzo_axial(),
            "aplastamiento":         self.Sy / self.esfuerzo_aplastamiento(),
        }
    else:
        
        def factor_seguridad(self):
            F = np.abs(self.carga_interna())
            return {
                "fluencia_tension_neta": self.Sy / self.esfuerzo_tension_neta(),
                "aplastamiento":         self.Sy / self.esfuerzo_aplastamiento(),
        }
    
    


 



        


    

    


