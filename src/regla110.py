from maquina_turing import MaquinaTuring

# Tabla de verdad de la Regla 110: patrón (izq, centro, der) -> nuevo estado de la celda.
REGLA_110 = {
    "111": "0",
    "110": "1",
    "101": "1",
    "100": "0",
    "011": "1",
    "010": "1",
    "001": "1",
    "000": "0",
}

BLANCO = "_"
MARCA = {"0": "X", "1": "Y"}          # bit -> bit marcado
VALOR = {"0": "0", "1": "1", "X": "0", "Y": "1"}  # símbolo -> bit que representa
BITS = "01"
ESTADO_INICIAL = "check"
ESTADO_FINAL = "halt"


def _control_k(d):
    """Fase A: si K es cero se detiene; si no, le resta 1 en binario."""
    d[("check", "0")] = ("check", "0", "R")
    d[("check", "1")] = ("finK", "1", "R")           # hay al menos un 1: K > 0
    d[("check", "#")] = (ESTADO_FINAL, "#", "S")     # K = 0: fin
    for s in BITS:
        d[("finK", s)] = ("finK", s, "R")
    d[("finK", "#")] = ("dec", "#", "L")
    d[("dec", "0")] = ("dec", "1", "L")              # préstamo: 0 -> 1 y sigue
    d[("dec", "1")] = ("irfin", "0", "R")            # 1 -> 0 y termina la resta


def _ubicar_generacion(d):
    """Fase B: lleva el cabezal a la primera celda de la última generación."""
    for s in "01#":
        d[("irfin", s)] = ("irfin", s, "R")
    d[("irfin", BLANCO)] = ("ulthash", BLANCO, "L")
    d[("ulthash", "#")] = ("inigen", "#", "L")
    for s in BITS:
        d[("inigen", s)] = ("inigen", s, "L")
    d[("inigen", "#")] = ("marcar", "#", "R")


def _marcar_celda(d):
    """Fase C: marca la celda actual y recuerda su valor (centro c)."""
    for c in BITS:
        d[("marcar", c)] = (f"izq_{c}", MARCA[c], "L")
    d[("marcar", "#")] = ("cerrar", "#", "R")        # no quedan celdas: generación terminada


def _vecino_izquierdo(d):
    """Fase D: lee el vecino izquierdo l (con salto cíclico a la última celda) y vuelve a la marca."""
    for c in BITS:
        for l in BITS:
            d[(f"izq_{c}", l)] = (f"mder_{l}{c}", l, "R")
        # Borde izquierdo: buscar la última celda de la generación.
        d[(f"izq_{c}", "#")] = (f"bult_{c}", "#", "R")
        for s in "01XY":
            d[(f"bult_{c}", s)] = (f"bult_{c}", s, "R")
        d[(f"bult_{c}", "#")] = (f"lult_{c}", "#", "L")
        for s in "01XY":
            d[(f"lult_{c}", s)] = (f"mizq_{VALOR[s]}{c}", s, "L" if s in BITS else "S")

    for l in BITS:
        for c in BITS:
            lc = l + c
            for s in BITS:
                d[(f"mder_{lc}", s)] = (f"mder_{lc}", s, "R")
                d[(f"mizq_{lc}", s)] = (f"mizq_{lc}", s, "L")
            for s in "XY":
                d[(f"mder_{lc}", s)] = (f"der_{lc}", s, "R")
                d[(f"mizq_{lc}", s)] = (f"der_{lc}", s, "R")


def _vecino_derecho_y_regla(d):
    """Fase E: lee el vecino derecho r (con salto cíclico a la primera celda) y aplica la Regla 110."""
    for l in BITS:
        for c in BITS:
            lc = l + c
            for r in BITS:
                d[(f"der_{lc}", r)] = (f"esc_{REGLA_110[lc + r]}", r, "R")
            # Borde derecho: buscar la primera celda de la generación.
            d[(f"der_{lc}", "#")] = (f"bpri_{lc}", "#", "L")
            for s in "01XY":
                d[(f"bpri_{lc}", s)] = (f"bpri_{lc}", s, "L")
            d[(f"bpri_{lc}", "#")] = (f"lpri_{lc}", "#", "R")
            for s in "01XY":
                d[(f"lpri_{lc}", s)] = (f"esc_{REGLA_110[lc + VALOR[s]]}", s, "R")


def _escribir_y_avanzar(d):
    """Fase F: escribe el resultado al final de la cinta, desmarca la celda y pasa a la siguiente."""
    for b in BITS:
        for s in "01#XY":
            d[(f"esc_{b}", s)] = (f"esc_{b}", s, "R")
        d[(f"esc_{b}", BLANCO)] = ("vmarca", b, "L")
    for s in "01#":
        d[("vmarca", s)] = ("vmarca", s, "L")
    for bit, marca in MARCA.items():
        d[("vmarca", marca)] = ("marcar", bit, "R")


def _cerrar_generacion(d):
    """Fase G: cierra la nueva generación con # y vuelve al inicio de la cinta."""
    for s in BITS:
        d[("cerrar", s)] = ("cerrar", s, "R")
    d[("cerrar", BLANCO)] = ("vini", "#", "L")
    for s in "01#":
        d[("vini", s)] = ("vini", s, "L")
    d[("vini", BLANCO)] = (ESTADO_INICIAL, BLANCO, "R")


def construir_transiciones():
    """Arma la tabla δ completa, fase por fase."""
    d = {}
    for fase in (
        _control_k,
        _ubicar_generacion,
        _marcar_celda,
        _vecino_izquierdo,
        _vecino_derecho_y_regla,
        _escribir_y_avanzar,
        _cerrar_generacion,
    ):
        fase(d)
    return d


def crear_maquina():
    """Devuelve una MaquinaTuring lista para simular la Regla 110."""
    return MaquinaTuring(construir_transiciones(), ESTADO_INICIAL, {ESTADO_FINAL}, BLANCO)
