from elements import TornilloDePotencia
from elements import Pasador
from elements import Brazo



FS_OBJETIVO = 1.5      # factor de seguridad minimo exigido
PASO = 0.5e-3          # incremento de dimension por iteracion (0.5 mm)
CRITICO = 0            # este es el índice donde se encuentra el fs crítico


def iterar_tornillo(d_inicial=10e-3, l=1.5e-3):

    fs = 0
    d = d_inicial
    while fs < FS_OBJETIVO:
        d = d + PASO
        tornillo = TornilloDePotencia("Tornillo de Potencia", d, l)
        factores = tornillo.factor_seguridad()
        fs = factores["von_mises_combinado"][CRITICO]
        print("  d =", round(d * 1e3, 2), "mm   ->   FS =", round(fs, 3))
    print("  -> Tornillo OK con d =", round(d * 1e3, 2), "mm\n")
    return d


def iterar_pasador(nombre, d_inicial, t, tipo, Sy_apoyo=None):

    fs = 0
    d = d_inicial
    while fs < FS_OBJETIVO:
        d = d + PASO
        pasador = Pasador(nombre, d, t, tipo, Sy_apoyo=Sy_apoyo)
        factores = pasador.factor_seguridad()
        fs = min(factores["cortante_von_mises"][CRITICO],
                 factores["aplastamiento"][CRITICO])
        print("  d =", round(d * 1e3, 2), "mm   ->   FS =", round(fs, 3))
    print("  ->", nombre, "OK con d =", round(d * 1e3, 2), "mm\n")
    return d


def iterar_brazo(A, I, L, d_1, d_2, t_inicial, K=1.0):

    fs = 0
    t = t_inicial
    while fs < FS_OBJETIVO:
        t = t + PASO
        brazo_c = Brazo("Brazo Compresion", A, I, L, d_1, d_2, t, K, False)
        brazo_t = Brazo("Brazo Tension", A, I, L, d_1, d_2, t, K, True)
        fc = brazo_c.factor_seguridad()
        ft = brazo_t.factor_seguridad()
        fs = min(
            fc["pandeo_johnson"][CRITICO],
            fc["fluencia_compresion"][CRITICO],
            fc["aplastamiento_hueco_1"][CRITICO],
            fc["aplastamiento_hueco_2"][CRITICO],
            ft["fluencia_tension_neta"][CRITICO],
            ft["aplastamiento_hueco_1"][CRITICO],
            ft["aplastamiento_hueco_2"][CRITICO],
        )
        print("  t =", round(t * 1e3, 2), "mm   ->   FS =", round(fs, 3))
    print("  -> Brazo OK con t =", round(t * 1e3, 2), "mm\n")
    return t
