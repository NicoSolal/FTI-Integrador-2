MOVIMIENTOS = {"L": -1, "R": 1, "S": 0}


class MaquinaTuring:
    """Máquina de Turing definida por δ: (estado, símbolo) -> (estado, escribir, mover)."""

    def __init__(self, transiciones, estado_inicial, estados_finales, blanco="_"):
        self.transiciones = transiciones
        self.estado_inicial = estado_inicial
        self.estados_finales = set(estados_finales)
        self.blanco = blanco
        self.cargar("")

    def cargar(self, entrada):
        """Escribe la entrada en la cinta y ubica el cabezal en el primer símbolo."""
        self.cinta = dict(enumerate(entrada))
        self.cabezal = 0
        self.estado = self.estado_inicial
        self.pasos = 0

    def detenida(self):
        """Indica si la máquina alcanzó un estado final."""
        return self.estado in self.estados_finales

    def paso(self):
        """Ejecuta una transición. Lanza RuntimeError si δ no está definida."""
        simbolo = self.cinta.get(self.cabezal, self.blanco)
        clave = (self.estado, simbolo)
        if clave not in self.transiciones:
            raise RuntimeError(
                f"δ{clave} no definida (paso {self.pasos}, cabezal {self.cabezal})"
            )
        nuevo_estado, escribir, mover = self.transiciones[clave]
        self.cinta[self.cabezal] = escribir
        self.cabezal += MOVIMIENTOS[mover]
        self.estado = nuevo_estado
        self.pasos += 1

    def ejecutar(self, max_pasos=10_000_000, traza=None):
        """Ejecuta hasta detenerse. `traza(mt)` se llama antes de cada paso si se indica."""
        while not self.detenida():
            if self.pasos >= max_pasos:
                raise RuntimeError(f"Se superó el límite de {max_pasos} pasos")
            if traza:
                traza(self)
            self.paso()
        return self.pasos

    def contenido(self):
        """Contenido de la cinta sin los blancos de los extremos."""
        usadas = [i for i, s in self.cinta.items() if s != self.blanco]
        if not usadas:
            return ""
        return "".join(
            self.cinta.get(i, self.blanco) for i in range(min(usadas), max(usadas) + 1)
        )

    def configuracion(self):
        """Configuración instantánea en la forma  izquierda[estado]derecha."""
        inicio = min(min(self.cinta, default=0), self.cabezal)
        fin = max(max(self.cinta, default=0), self.cabezal)
        celdas = [self.cinta.get(i, self.blanco) for i in range(inicio, fin + 1)]
        pos = self.cabezal - inicio
        return "".join(celdas[:pos]) + f"[{self.estado}]" + "".join(celdas[pos:])

    def tabla_markdown(self):
        """Tabla de transiciones en formato Markdown, agrupada por estado."""
        filas = ["| Estado | Lee | Nuevo estado | Escribe | Mueve |", "|---|---|---|---|---|"]
        for (estado, lee), (nuevo, escribe, mueve) in self.transiciones.items():
            filas.append(f"| {estado} | {lee} | {nuevo} | {escribe} | {mueve} |")
        return "\n".join(filas)
