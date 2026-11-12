from regla110 import REGLA_110


def siguiente_generacion(gen):
    """Aplica la Regla 110 a cada celda con frontera cíclica."""
    n = len(gen)
    return "".join(REGLA_110[gen[i - 1] + gen[i] + gen[(i + 1) % n]] for i in range(n))


def evolucionar(gen, k):
    """Devuelve la lista [gen0, gen1, ..., genK]."""
    generaciones = [gen]
    for _ in range(k):
        generaciones.append(siguiente_generacion(generaciones[-1]))
    return generaciones
