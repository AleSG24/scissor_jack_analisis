from elements import Brazo
from elements import Pasador
from elements import TornilloDePotencia

def main():
    #Ahora, construiré la gata utilizando los objetos creados

   brazo_c = Brazo("Brazo#1",418.84e-6, 23046.51e-12,145e-3,10e-3,8e-3,5e-3, 1.0,False)
   brazo_t = Brazo("Brazo#2",418.84e-6, 23046.51e-12,145e-3,10e-3,8e-3,5e-3, 1.0,True)
   factores_t = brazo_t.factor_seguridad()
   factores_c = brazo_c.factor_seguridad()
   print("Brazo en Compresión:\n")
   print("angulo:", factores_c["angulo"], "\n")
   print("pandeo_jhonson:", factores_c["pandeo_johnson"], "\n")
   print("fluencia_compresion:", factores_c["fluencia_compresion"], "\n")
   print("aplastamiento_hueco_1:", factores_c["aplastamiento_hueco_1"], "\n")
   print("aplastamiento_hueco_2:", factores_c["aplastamiento_hueco_2"], "\n")

   print("Brazo en Tensión:\n")
   print("angulo:", factores_t["angulo"], "\n")
   print("fluencia_tension_neta:", factores_t["fluencia_tension_neta"], "\n")
   print("aplastamiento_hueco_1:", factores_t["aplastamiento_hueco_1"], "\n")
   print("aplastamiento_hueco_2:", factores_t["aplastamiento_hueco_2"], "\n")
 
 
   #El perno tipo 1 apoya contra las placas de acero SAE 1020 (210 MPa), material mas debil del par
   pasador1 = Pasador("pasador1", 8e-3,8e-3,1, Sy_apoyo=210e6)
   pasador2 = Pasador("pasador2", 10e-3, 8e-3,2)
 
   factores_1 = pasador1.factor_seguridad()
   factores_2 = pasador2.factor_seguridad()
 
   print("Pasador Tipo 1:\n")
   print("angulo:", factores_1["angulo"], "\n")
   print("cortante_von_mises:", factores_1["cortante_von_mises"], "\n")
   print("aplastamiento:", factores_1["aplastamiento"], "\n")
 
   print("Pasador Tipo 2:\n")
   print("angulo:", factores_2["angulo"], "\n")
   print("cortante_von_mises:", factores_2["cortante_von_mises"], "\n")
   print("aplastamiento:", factores_2["aplastamiento"], "\n")
 
   Tornillo_P = TornilloDePotencia("Tornillo de Potencia", 10e-3, 1.5e-3)
 
   factorestor = Tornillo_P.factor_seguridad()
 
   print("Tornillo de Potencia:\n")
   print("angulo:", factorestor["angulo"], "\n")
   print("Torque requerido:", factorestor["Torque requerido"], "\n")
   print("von_mises_combinado:", factorestor["von_mises_combinado"], "\n")






 #Todo esto solo se utilizó para iterar el diametro correcto del tornillo de potencia
'''
   fs_20 = 0
   d = 10e-3
   while fs_20 < 1.5:
    d = d + 0.5e-3
    Tornillo_P = TornilloDePotencia("Tornillo de Potencia", d, 1.5e-3)
    fs = Tornillo_P.factor_seguridad()
    fs_20 = fs["von_mises_combinado"][0]
    print(fs_20)
    print(d)

    resultados de iteración:

    el orden está:
    fs
    d

0.8093292396834133
0.013000000000000003
0.8865446313818205
0.013500000000000003
0.9672629003265445
0.014000000000000004
1.0514834579038999
0.014500000000000004
1.1392057975008636
0.015000000000000005
1.2304294808900391
0.015500000000000005
1.3251541272044303
0.016000000000000004
1.423379403952894
0.016500000000000004
1.5251050196543112
0.017000000000000005
'''





    




main()