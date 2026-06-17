import numpy as np
import math

'''''
En este script se definen los elementos de maquinas orientados a objetos.
'''''

class Elemento:

    theta_deg = np.linspace(20, 60, 9)
    theta = np.radians(theta_deg)

    def __init__(self, nombre, E, Sy, Ssy=None):
        self.nombre = nombre
        self.Sy = Sy #Usar en Pa
        self.Ssy = Ssy if Ssy != None else 0.577*Sy 
        self.P = 20000
    

    def von_mises(sigma, tau):

        return np.sqrt(sigma**2 + 3.0*tau**2)
    
    def reaccion_nodo(self, tipo):

        c, s = np.cos(self.theta), np.sin(self.theta)
        if tipo == 1:
            Rx = self.P * c / (2 * s)
            Ry = self.P 
        else:  # tipo 2
            Rx = self.P * c / s
            Ry = 0
        return Rx, Ry



    def carga_interna(self):

        raise NotImplementedError

    def esfuerzo_critico(self):

        raise NotImplementedError
    
    def factor_seguridad(self):

        raise NotImplementedError

class Brazo(Elemento):
    #Datos Tabla-20 y Tabla 5 Shigley decima edicion
    material = "Acero SAE 1020 HR"
    E = 207e9
    Sy = 210e6
    def __init__(self, nombre, A, I, L, d, t, K=1.0, tension=bool, **kw):
        super().__init__(nombre, self.material, self.E, self.Sy, **kw)
        self.A = A                # area transversal              m^2
        self.I = I                # momento de inercia            m^4
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
 
 
    def esfuerzo_aplastamiento(self):
       
        return np.abs(self.carga_interna()) / (self.t * self.d)
 
    def esfuerzo_critico(self):
        if self.tension:
            return np.maximum(
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
            "angulo": self.theta_deg,
            "pandeo_johnson":        self.carga_critica_johnson() / F,   
            "fluencia_compresion":   self.Sy / self.esfuerzo_axial(),
            "aplastamiento":         self.Sy / self.esfuerzo_aplastamiento(),
        }
    else:
        
        def factor_seguridad(self):
            F = np.abs(self.carga_interna())
            return {
                "angulo": self.theta_deg,
                "fluencia_tension_neta": self.Sy / self.esfuerzo_tension_neta(),
                "aplastamiento":         self.Sy / self.esfuerzo_aplastamiento(),
        }
    
    class Pasador(Elemento):
         #Datos Tabla-20 y Tabla 5 Shigley decima edicion
            material = "Acero SAE 1020 CD"
            E = 207e9
            Sy = 390e6
            def __init__(self, nombre, d, t, tipo, **kw):

                super().__init__(nombre, self.material, self.E, self.Sy, **kw)

            self.d = d
            self.t = t
            self.tipo = tipo #1 o 2 como fue definido en el avance 2

            def carga_interna(self):
                Rx, Ry = self.reaccion_nodo(self.tipo)
                return np.hypot(Rx, Ry)
            
            def area_cortante(self):
                return (np.pi*self.d**2)/4
            
            def esfuerzo_cortante(self):
                return self.carga()/self.area_cortante()
            
            def esfuerzo_aplastamiento(self):
                return self.carga_interna()/(self.t*self.d)

            def esfuerzo_critico(self):
                return np.maximum(self.esfuerzo_cortante(), self.esfuerzo_aplastamiento())
            
            def factor_seguridad(self):
                return {
                    "angulo": self.theta_deg,
                    "cortante_von_mises": self.Ssy/self.esfuerzo_cortante(),

                    "aplastamiento": self.Sy/self.esfuerzo_aplastamiento(),
                }

class UnionArticulada(Elemento):
    #Datos Tabla-20 y Tabla 5 Shigley decima edicion
    material = "Acero SAE 1020 HR"
    E = 207e9
    Sy = 210e6
    def __init__(self, nombre, d, t, tipo, **kw):
        super().__init__(nombre, self.material, self.E, self.Sy, **kw)
        self.d = d                # diámetro del hueco de la oreja m
        self.t = t                # espesor de la oreja              m
        self.tipo = tipo
 
    def carga_interna(self):
        Rx, Ry = self.reaccion_nodo(self.tipo)
        return np.hypot(Rx, Ry)
 
    def esfuerzo_aplastamiento(self):
        return self.carga_interna() / (self.t * self.d)
 
    def esfuerzo_critico(self):
        return self.esfuerzo_aplastamiento()
 
    def factor_seguridad(self):
        return {
            "angulo": self.theta_deg,
            "aplastamiento": self.Sy / self.esfuerzo_aplastamiento()
            }


class TornilloDePotencia(Elemento):
    #Datos Tabla-20 y Tabla 5 Shigley decima edicion
    material = "Acero SAE 1020 HR"
    E = 207e9
    Sy = 390e6
    def __init__(self, nombre, d, dm, l, f=0.12, dr=None, **kw):
        super().__init__(nombre, self.material, self.E, self.Sy, **kw)
        self.d = d        # diámetro nominal de la rosca   m
        self.dm = dm      # diámetro medio de la rosca     m
        self.l = l        # avance de la rosca             m
        self.f = f        # coeficiente de fricción
        
        self.dr = dr if dr is not None else d - 1.226869 * l
 
    def carga_interna(self):
        
        return 2 * self.P * np.cos(self.theta) / np.sin(self.theta)
 
    def torque_requerido(self):
        
        Ft = self.carga_interna()
        return (Ft * self.dm / 2) * (
            (self.l + np.pi * self.f * self.dm) /
            (np.pi * self.dm - self.f * self.l)
        )
 
    def esfuerzo_axial(self):
        
        return 4 * self.carga_interna() / (np.pi * self.dr**2)
 
    def esfuerzo_cortante_torsion(self):
        
        return 16 * self.torque_requerido() / (np.pi * self.dr**3)
 
    def esfuerzo_von_mises(self):
        return self.von_mises(self.esfuerzo_axial(),
                              self.esfuerzo_cortante_torsion())
 
    def esfuerzo_critico(self):
        return self.esfuerzo_von_mises()
 
    def factor_seguridad(self):
        return {
            "angulo": self.theta_deg,
            "von_mises_combinado": self.Sy / self.esfuerzo_von_mises()
            }




        


    

    


