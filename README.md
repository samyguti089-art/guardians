# Guardians of the Ancient Kingdom - Sistema de Combate por Turnos

Proyecto integrador para la asignatura de **Programación Orientada a Objetos con Python**.

---

## 1. Descripción del proyecto
**Guardians of the Ancient Kingdom** es un programa en Python que simula enfrentamientos por turnos entre tres tipos de guardianes del reino de Eldoria: Guerreros, Magos y Arqueros. 
El problema que resuelve es automatizar las reglas de un combate de rol (calcular daños según las habilidades de cada clase, proteger que la vida no baje de cero, validar que no entren datos erróneos y alternar turnos automáticamente) hasta determinar qué personaje gana o si ocurre un empate.

---

## 2. Estructura del repositorio
El proyecto está dividido en tres archivos principales:
* `personajes.py`: Contiene toda la lógica orientada a objetos. Aquí están programadas la clase abstracta `Personaje`, las clases hijas (`Guerrero`, `Mago`, `Arquero`) y la clase `Combate`. No ejecuta nada por sí solo al importarse.
* `main.py`: Es el archivo principal de ejecución. Importa las clases de `personajes.py`, pone a prueba los 12 casos obligatorios en consola y además incluye las pruebas automatizadas con `pytest`.
* `README.md`: Documento donde explico cómo está diseñado el programa, cómo se aplicaron los temas de clase y el desarrollo de los retos extra.

---

## 3. Responsabilidad de las clases
* **`Personaje` (Clase Abstracta):** Es la plantilla base. Se encarga de guardar y validar los atributos básicos (`nombre`, `vida`, `ataque`, `defensa`), controlar cómo se resta la vida en `recibir_danio()`, verificar si el personaje sigue con vida y obligar a las clases hijas a tener su propio método `atacar()`.
* **`Guerrero`:** Hereda de `Personaje`. Su responsabilidad es implementar el ataque aplicando el "Golpe poderoso" (aumenta su ataque un 20% antes de restar la defensa del rival).
* **`Mago`:** Hereda de `Personaje`. Su responsabilidad es atacar con "Hechizo penetrante", haciendo un daño igual a su ataque sin importar cuánta defensa tenga el enemigo.
* **`Arquero`:** Hereda de `Personaje`. Su responsabilidad es el "Disparo crítico", que duplica el daño normal siempre y cuando su ataque sea estrictamente mayor a la defensa del oponente.
* **`Combate`:** Administra la pelea entre dos personajes. Controla de quién es el turno, llama a los ataques, verifica después de cada golpe si alguien ya ganó y detiene la pelea si hay un empate técnico o si pasan 50 rondas.

---

## 4. Relaciones entre clases
1. **Herencia (`Guerrero`, `Mago` y `Arquero` heredan de `Personaje`):** Se usó porque los tres son tipos de personajes y tienen exactamente los mismos atributos y validaciones. Así evitamos copiar y pegar el mismo código tres veces.
2. **Asociación (`Personaje` interactúa con otro `Personaje`):** Se ve en el método `atacar(objetivo)`. Un objeto personaje recibe a otro como parámetro y usa sus métodos `get_defensa()` y `recibir_danio()` para interactuar con él.
3. **Agregación (`Combate` tiene dos `Personaje`):** En `main.py` creamos primero a `arthas` y a `gandalf`, y luego se los pasamos a `Combate(arthas, gandalf)`. Es agregación porque si el objeto `Combate` se destruye o termina, los objetos de los personajes siguen existiendo por separado.

---

## 5. Aplicación de los conceptos de POO
* **Abstracción:** Se aplicó al crear la clase `Personaje` con `ABC` y marcar `atacar()` con `@abstractmethod`. Definimos qué debe hacer todo personaje sin importar todavía cómo calcula el daño cada orden.
* **Encapsulamiento:** Los atributos se definieron como privados usando doble guion bajo (`__nombre`, `__vida`, `__ataque`, `__defensa`). Nadie puede cambiar la vida a `-50` desde afuera directamente; todo cambio pasa por los métodos `set_` o por `recibir_danio()`, donde hay condicionales `if` que lanzan un `ValueError` si el dato es inválido.
* **Herencia:** Las subclases usan `super().__init__(...)` para reutilizar el constructor y heredan métodos como `esta_vivo()`, `mostrar_estado()` y `recibir_danio()`.
* **Polimorfismo:** Dentro del método `iniciar()` de la clase `Combate`, el programa simplemente ejecuta `self.atacante_actual.atacar(self.defensor_actual)`. La clase `Combate` nunca usa `if type(atacante) == Guerrero`, sino que cada objeto responde ejecutando su propia versión de `atacar()`.

---

## 6. Lógica del combate y administración de turnos
En cada turno, el `atacante_actual` ejecuta su método `atacar()` contra el `defensor_actual`:
* **Guerrero:** `int(ataque * 1.20) - defensa_rival` (si da menor a 0, el daño es 0).
* **Mago:** `ataque` directo.
* **Arquero:** Si `ataque > defensa_rival`, hace `(ataque - defensa_rival) * 2`. Si no la supera, hace `0`.

Una **ronda** equivale a 2 turnos (un ataque de cada participante). Si tras un turno la vida del defensor llega a `0`, `verificar_ganador()` detecta al vencedor y termina el ciclo `while`. Si no, `cambiar_turno()` intercambia las variables `atacante_actual` y `defensor_actual`. Si terminan los 2 turnos de la ronda y la suma de daño fue `0`, se declara empate técnico para no quedar en un bucle infinito.

---

## 7. Instrucciones de ejecución

### Ejecutar el programa principal
1. Clonar este repositorio o descargar los archivos en una misma carpeta.
2. Abrir la terminal en esa carpeta y ejecutar:
```bash
python main.py