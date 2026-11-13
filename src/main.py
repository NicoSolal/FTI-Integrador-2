import argparse
import re
import sys

from referencia import evolucionar
from regla110 import crear_maquina

FORMATO_ENTRADA = re.compile(r"^([01]+)#([01]+)#$")


def leer_casos(ruta):
    """Lee un caso de prueba por línea, ignorando líneas vacías."""
    with open(ruta, encoding="utf-8") as f:
        return [linea.strip() for linea in f if linea.strip()]


def ejecutar_caso(mt, entrada, traza=False):
    """Corre la MT sobre una entrada, la compara con el oráculo e imprime el resultado. Devuelve True si coincide."""
    coincidencia = FORMATO_ENTRADA.match(entrada)
    if not coincidencia:
        print(f"[ERROR] Formato inválido: {entrada!r} (se espera K#celdas#)")
        return False
    k_bin, gen0 = coincidencia.groups()
    k = int(k_bin, 2)

    print(f"Entrada: {entrada}   (K = {k}, N = {len(gen0)})")
    if len(gen0) < 8:
        print("  Aviso: el enunciado pide N >= 8")

    mt.cargar(entrada)
    mt.ejecutar(traza=(lambda m: print("  ", m.configuracion())) if traza else None)
    cinta = mt.contenido()

    # Cinta completa esperada: K en cero (misma longitud) seguido de todas las generaciones.
    generaciones = evolucionar(gen0, k)
    esperada = "0" * len(k_bin) + "#" + "#".join(generaciones) + "#"

    # Resumen: contador final y última generación.
    partes = cinta.split("#")
    final = f"{partes[0]}#{partes[-2]}#"

    for i, gen in enumerate(partes[1:-1]):
        print(f"  Gen {i:02d}: {' '.join(gen)}")
    print(f"  Cinta completa: {cinta}")
    print(f"  Cinta final: {final}")
    print(f"  Pasos de la MT: {mt.pasos}")

    ok = cinta == esperada
    print(f"  {'OK' if ok else 'FALLA'}")
    if not ok:
        print(f"  Esperada:    {esperada}")
    print()
    return ok


def main():
    parser = argparse.ArgumentParser(description="MT que simula la Regla 110")
    parser.add_argument("casos", nargs="?", default="casos_prueba.txt")
    parser.add_argument("--traza", action="store_true")
    parser.add_argument("--tabla", metavar="ARCHIVO")
    args = parser.parse_args()

    mt = crear_maquina()
    estados = {e for e, _ in mt.transiciones} | mt.estados_finales
    print(f"Máquina de Turing: {len(estados)} estados, {len(mt.transiciones)} transiciones\n")

    if args.tabla:
        with open(args.tabla, "w", encoding="utf-8") as f:
            f.write(mt.tabla_markdown() + "\n")
        print(f"Tabla de transiciones exportada a {args.tabla}\n")

    casos = leer_casos(args.casos)
    resultados = [ejecutar_caso(mt, c, args.traza) for c in casos]
    print(f"Resultado: {sum(resultados)}/{len(resultados)} casos correctos")
    sys.exit(0 if all(resultados) else 1)


if __name__ == "__main__":
    main()
