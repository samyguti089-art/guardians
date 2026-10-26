import pytest
from personajes import Personaje, Guerrero, Mago, Arquero, Combate

def ejecutar_pruebas_manuales():
    print("=========================================")
    print("   PRUEBAS DEL SISTEMA DE COMBATE POO    ")
    print("=========================================\n")

    # 1. Creacion correcta de los tres tipos de personajes
    print("--- Caso 1: Creacion de personajes validos ---")
    g1 = Guerrero("Arthas", 100, 30, 20)
    m1 = Mago("Gandalf", 80, 40, 10)
    a1 = Arquero("Legolas", 90, 35, 15)
    print("Creados con exito:")
    print(g1.mostrar_estado())
    print(m1.mostrar_estado())
    print(a1.mostrar_estado())

    # 2. Rechazo de personajes con vida superior a 100 o negativa
    print("\n--- Caso 2: Validacion de vida invalida ---")
    try:
        Guerrero("Clon", 150, 20, 10)
    except ValueError as e:
        print("Vida > 100 rechazada correctamente:", e)

    try:
        Mago("Clon2", -10, 20, 10)
    except ValueError as e:
        print("Vida negativa rechazada correctamente:", e)

    # 3. Rechazo de nombres vacios
    print("\n--- Caso 3: Validacion de nombre vacio ---")
    try:
        Arquero("   ", 80, 25, 10)
    except ValueError as e:
        print("Nombre vacio rechazado correctamente:", e)

    # 4. Rechazo de ataques y defensas invalidos
    print("\n--- Caso 4: Validacion de ataque y defensa invalidos ---")
    try:
        Guerrero("Arturo", 100, 0, 10)
    except ValueError as e:
        print("Ataque <= 0 rechazado correctamente:", e)

    try:
        Guerrero("Arturo", 100, 20, -5)
    except ValueError as e:
        print("Defensa < 0 rechazada correctamente:", e)

    # 5. Aplicacion correcta de la habilidad del Guerrero
    # Ejemplo de la guia: Ataque 30, Defensa enemiga 10 -> 30 * 1.2 = 36 - 10 = 26
    print("\n--- Caso 5: Habilidad del Guerrero (Golpe poderoso) ---")
    guerrero_prueba = Guerrero("Conan", 100, 30, 15)
    objetivo_g = Guerrero("SacoDeBoxeo", 100, 10, 10)
    danio_g = guerrero_prueba.atacar(objetivo_g)
    print(f"Danio esperado: 26 | Danio obtenido: {danio_g} | Vida restante objetivo: {objetivo_g.get_vida()}")

    # 6. Aplicacion correcta del ataque del Mago ignorando defensa
    # Ejemplo de la guia: Ataque 40, Defensa enemiga 20 -> Danio = 40
    print("\n--- Caso 6: Habilidad del Mago (Hechizo penetrante) ---")
    mago_prueba = Mago("Merlin", 80, 40, 5)
    objetivo_m = Guerrero("Tanque", 100, 10, 20)
    danio_m = mago_prueba.atacar(objetivo_m)
    print(f"Danio esperado: 40 | Danio obtenido: {danio_m} | Vida restante objetivo: {objetivo_m.get_vida()}")

    # 7. Aplicacion correcta del disparo critico del Arquero
    # Ejemplo de la guia: Ataque 35, Defensa 15 -> Base 20 * 2 = 40
    print("\n--- Caso 7: Habilidad del Arquero (Disparo critico) ---")
    arquero_prueba = Arquero("Robin", 90, 35, 10)
    objetivo_a = Guerrero("Guardia", 100, 10, 15)
    danio_a = arquero_prueba.atacar(objetivo_a)
    print(f"Danio esperado: 40 | Danio obtenido: {danio_a} | Vida restante objetivo: {objetivo_a.get_vida()}")

    # 8. Imposibilidad de tener vida negativa
    print("\n--- Caso 8: Control de vida no negativa ---")
    debil = Mago("Aprendiz", 20, 10, 5)
    verdugo = Mago("JefeFinal", 100, 50, 10)
    danio_efectivo = verdugo.atacar(debil)
    print(f"Aprendiz tenia 20 de vida y recibio ataque de 50. Danio efectivo: {danio_efectivo} | Vida actual: {debil.get_vida()}")

    # 9. Imposibilidad de atacar estando derrotado
    print("\n--- Caso 9: Imposibilidad de atacar estando derrotado ---")
    try:
        debil.atacar(verdugo)
    except ValueError as e:
        print("Ataque de personaje derrotado bloqueado correctamente:", e)

    # 10 y 11. Ejecucion de un combate completo e identificacion del ganador (Ejemplo de la seccion 6)
    print("\n--- Casos 10 y 11: Combate completo Arthas vs Gandalf ---")
    arthas = Guerrero("Arthas", 100, 30, 10)  # Defensa 10 para que Gandalf reciba 26 y de exacto a la tabla
    gandalf = Mago("Gandalf", 80, 40, 10)
    combate1 = Combate(arthas, gandalf)
    ganador = combate1.iniciar()
    print(f"Verificacion del ganador devuelto: {ganador.get_nombre()}")

    # 12. Finalizacion de un combate sin danio mediante empate tecnico
    print("\n--- Caso 12: Combate con empate tecnico (sin danio) ---")
    muralla1 = Guerrero("Muralla 1", 100, 10, 50)
    muralla2 = Arquero("Muralla 2", 100, 15, 50)
    combate_empate = Combate(muralla1, muralla2)
    combate_empate.iniciar()


# =====================================================================
# RETO EXTRA 2: PRUEBAS AUTOMATIZADAS CON PYTEST
# Para ejecutarlas en consola: pytest main.py
# =====================================================================

def test_creacion_personajes_validos():
    g = Guerrero("Arthas", 100, 30, 20)
    m = Mago("Gandalf", 80, 40, 10)
    a = Arquero("Legolas", 90, 35, 15)
    assert g.get_nombre() == "Arthas"
    assert m.get_vida() == 80
    assert a.get_ataque() == 35

def test_rechazo_valores_incorrectos():
    # Vida mayor a 100 y negativa
    with pytest.raises(ValueError):
        Guerrero("ErrorVida", 120, 20, 10)
    with pytest.raises(ValueError):
        Mago("ErrorVidaNeg", -5, 20, 10)
    # Nombre vacio
    with pytest.raises(ValueError):
        Arquero("", 80, 20, 10)
    # Ataque y defensa invalidos
    with pytest.raises(ValueError):
        Guerrero("ErrorAtaque", 80, 0, 10)
    with pytest.raises(ValueError):
        Guerrero("ErrorDefensa", 80, 20, -1)

def test_calculo_danio_clases():
    # Guerrero: 30 * 1.2 = 36 - 10 = 26
    g = Guerrero("G", 100, 30, 10)
    obj1 = Guerrero("O1", 100, 10, 10)
    assert g.atacar(obj1) == 26

    # Mago: ignora defensa (40 directo)
    m = Mago("M", 100, 40, 10)
    obj2 = Guerrero("O2", 100, 10, 20)
    assert m.atacar(obj2) == 40

    # Arquero: (35 - 15) * 2 = 40
    a = Arquero("A", 100, 35, 10)
    obj3 = Guerrero("O3", 100, 10, 15)
    assert a.atacar(obj3) == 40

def test_vida_nunca_negativa():
    atacante = Mago("MagoFuerte", 100, 80, 10)
    victima = Guerrero("Soldado", 30, 10, 10)
    danio_real = atacante.atacar(victima)
    assert victima.get_vida() == 0
    assert danio_real == 30

def test_derrotado_no_puede_atacar():
    muerto = Guerrero("Caido", 0, 30, 10)
    vivo = Guerrero("Vivo", 100, 30, 10)
    with pytest.raises(ValueError):
        muerto.atacar(vivo)

def test_resultado_combate_y_empate():
    arthas = Guerrero("Arthas", 100, 30, 20)
    gandalf = Mago("Gandalf", 80, 40, 10)
    pelea = Combate(arthas, gandalf)
    ganador = pelea.iniciar()
    assert ganador == gandalf
    assert gandalf.get_vida() == 2
    assert arthas.get_vida() == 0

    # Prueba de empate tecnico
    tanque1 = Guerrero("T1", 100, 10, 50)
    tanque2 = Guerrero("T2", 100, 10, 50)
    pelea_empate = Combate(tanque1, tanque2)
    assert pelea_empate.iniciar() is None


if __name__ == "__main__":
    ejecutar_pruebas_manuales()