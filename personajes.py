from abc import ABC, abstractmethod

# 3.1. Clase abstracta Personaje
class Personaje(ABC):
    def __init__(self, nombre, vida, ataque, defensa):
        # Inicializamos los atributos privados en None y luego usamos los setters para validar
        self.__nombre = None
        self.__vida = None
        self.__ataque = None
        self.__defensa = None

        self.set_nombre(nombre)
        self.set_vida(vida)
        self.set_ataque(ataque)
        self.set_defensa(defensa)

    # --- GETTERS ---
    def get_nombre(self):
        return self.__nombre

    def get_vida(self):
        return self.__vida

    def get_ataque(self):
        return self.__ataque

    def get_defensa(self):
        return self.__defensa

    # --- SETTERS CON VALIDACIONES ---
    def set_nombre(self, nombre):
        if type(nombre) != str or nombre.strip() == "":
            raise ValueError("Error: El nombre debe ser un texto y no puede estar vacio.")
        self.__nombre = nombre.strip()

    def set_vida(self, vida):
        if type(vida) != int or vida < 0 or vida > 100:
            raise ValueError("Error: La vida debe ser un numero entero entre 0 y 100.")
        self.__vida = vida

    def set_ataque(self, ataque):
        if type(ataque) != int or ataque <= 0:
            raise ValueError("Error: El ataque debe ser un numero entero positivo mayor a 0.")
        self.__ataque = ataque

    def set_defensa(self, defensa):
        if type(defensa) != int or defensa < 0:
            raise ValueError("Error: La defensa debe ser un numero entero mayor o igual a 0.")
        self.__defensa = defensa

    # --- METODOS COMUNES ---
    def recibir_danio(self, cantidad):
        if type(cantidad) != int or cantidad < 0:
            raise ValueError("Error: La cantidad de danio no puede ser negativa.")

        vida_antes = self.__vida
        nueva_vida = self.__vida - cantidad

        # Evitamos que la vida quede negativa
        if nueva_vida < 0:
            self.__vida = 0
        else:
            self.__vida = nueva_vida

        # Devolvemos el danio que realmente le bajo a la vida
        danio_efectivo = vida_antes - self.__vida
        return danio_efectivo

    def esta_vivo(self):
        if self.__vida > 0:
            return True
        else:
            return False

    def mostrar_estado(self):
        return f"{self.__nombre} (Vida: {self.__vida}, Ataque: {self.__ataque}, Defensa: {self.__defensa})"

    # Metodo auxiliar para no repetir las validaciones de ataque en cada hijo
    def validar_antes_de_atacar(self, objetivo):
        if not isinstance(objetivo, Personaje):
            raise ValueError("Error: El objetivo no es un personaje valido.")
        if not self.esta_vivo():
            raise ValueError(f"Error: {self.__nombre} esta derrotado y no puede atacar.")
        if not objetivo.esta_vivo():
            raise ValueError(f"Error: El objetivo {objetivo.get_nombre()} ya esta derrotado.")

    @abstractmethod
    def atacar(self, objetivo):
        pass


# 3.2. Clase Guerrero
class Guerrero(Personaje):
    def __init__(self, nombre, vida, ataque, defensa):
        super().__init__(nombre, vida, ataque, defensa)

    def atacar(self, objetivo):
        self.validar_antes_de_atacar(objetivo)

        # Habilidad: Golpe poderoso (aumenta 20% y se redondea hacia abajo con int)
        ataque_potenciado = int(self.get_ataque() * 1.20)
        danio_calculado = ataque_potenciado - objetivo.get_defensa()

        if danio_calculado < 0:
            danio_calculado = 0

        danio_real = objetivo.recibir_danio(danio_calculado)
        return danio_real


# 3.3. Clase Mago
class Mago(Personaje):
    def __init__(self, nombre, vida, ataque, defensa):
        super().__init__(nombre, vida, ataque, defensa)

    def atacar(self, objetivo):
        self.validar_antes_de_atacar(objetivo)

        # Habilidad: Hechizo penetrante (ignora la defensa del objetivo)
        danio_calculado = self.get_ataque()

        if danio_calculado < 0:
            danio_calculado = 0

        danio_real = objetivo.recibir_danio(danio_calculado)
        return danio_real


# 3.4. Clase Arquero
class Arquero(Personaje):
    def __init__(self, nombre, vida, ataque, defensa):
        super().__init__(nombre, vida, ataque, defensa)

    def atacar(self, objetivo):
        self.validar_antes_de_atacar(objetivo)

        # Habilidad: Disparo critico (si supera la defensa, duplica el danio base)
        if self.get_ataque() > objetivo.get_defensa():
            danio_base = self.get_ataque() - objetivo.get_defensa()
            danio_calculado = danio_base * 2
        else:
            danio_calculado = 0

        danio_real = objetivo.recibir_danio(danio_calculado)
        return danio_real


# 4. Clase Combate
class Combate:
    def __init__(self, personaje1, personaje2):
        if not isinstance(personaje1, Personaje) or not isinstance(personaje2, Personaje):
            raise ValueError("Error: Ambos participantes deben ser objetos de tipo Personaje.")

        self.p1 = personaje1
        self.p2 = personaje2
        self.atacante_actual = self.p1
        self.defensor_actual = self.p2
        self.ganador = None
        self.motivo_fin = ""
        self.rondas_jugadas = 0

    def cambiar_turno(self):
        if self.atacante_actual == self.p1:
            self.atacante_actual = self.p2
            self.defensor_actual = self.p1
        else:
            self.atacante_actual = self.p1
            self.defensor_actual = self.p2

    def verificar_ganador(self):
        if self.p1.esta_vivo() and not self.p2.esta_vivo():
            self.ganador = self.p1
            return self.p1
        elif self.p2.esta_vivo() and not self.p1.esta_vivo():
            self.ganador = self.p2
            return self.p2
        else:
            return None

    def iniciar(self):
        print("\n==================================================")
        print(f"INICIO DEL COMBATE: {self.p1.get_nombre()} vs {self.p2.get_nombre()}")
        print(f"Estado inicial -> {self.p1.mostrar_estado()} | {self.p2.mostrar_estado()}")
        print("==================================================")

        turno = 1
        ronda = 1

        while ronda <= 50:
            self.rondas_jugadas = ronda
            danio_en_la_ronda = 0

            # Una ronda completa tiene 2 ataques (uno de cada personaje)
            for i in range(2):
                if self.atacante_actual.esta_vivo() and self.defensor_actual.esta_vivo():
                    # Polimorfismo: llamamos a atacar() sin importar que clase de personaje sea
                    danio_hecho = self.atacante_actual.atacar(self.defensor_actual)
                    danio_en_la_ronda = danio_en_la_ronda + danio_hecho

                    print(f"Turno {turno} | Ataca: {self.atacante_actual.get_nombre()} | Danio causado: {danio_hecho}")
                    print(f"   -> Vida {self.p1.get_nombre()}: {self.p1.get_vida()} | Vida {self.p2.get_nombre()}: {self.p2.get_vida()}")

                    turno = turno + 1

                    # Revisamos si alguien ya gano
                    if self.verificar_ganador() is not None:
                        self.motivo_fin = f"Ganador: {self.ganador.get_nombre()}"
                        self.mostrar_resultado()
                        return self.ganador

                    self.cambiar_turno()

            # Regla 6: Si termina la ronda (los 2 atacaron) y ninguno hizo danio, es empate tecnico
            if danio_en_la_ronda == 0:
                self.motivo_fin = "Empate tecnico (ningun personaje pudo hacer danio en la ronda)."
                self.mostrar_resultado()
                return None

            ronda = ronda + 1

        # Regla 7: Si llegan a 50 rondas sin ganador
        self.motivo_fin = "Empate por limite de 50 rondas alcanzadas."
        self.mostrar_resultado()
        return None

    def mostrar_resultado(self):
        print("--------------------------------------------------")
        print(f"RESULTADO FINAL: {self.motivo_fin}")
        print("--------------------------------------------------")