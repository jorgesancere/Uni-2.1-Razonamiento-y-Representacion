# Razonamiento y Representación del Conocimiento

Práctica 1: Sistemas Expertos

Jorge Sánchez Cerezo - Universidad de Alicante - Curso 2026/2027

---

## De qué va

En esta práctica se pretende elaborar métodos para el control de un robot móvil utilizando un
sistema experto. Se va a considerar un robot móvil que puede desplazarse por un plano horizontal
mediante comandos de velocidad lineal y velocidad angular. El objetivo del robot será recorrer lo
más cercanamente posible un camino a través de su entorno. El entorno está libre de obstáculos y no
se tendrán en cuenta los posibles sensores del robot. Conoceremos únicamente su pose, es decir, la
posición (x, y) del robot en el plano y la orientación del robot.
Se proporcionará un proyecto que realizará la simulación del movimiento del robot y la visualizará.
Según el robot vaya alcanzando los objetivos que vaya recibiendo irá obteniendo una puntuación de
recompensa de acuerdo a lo bien que se ajuste su trayectoria a los objetivos y el tiempo que emplee
en alcanzarlos.

La práctica tiene dos ejercicios que resuelven el mismo problema de dos formas:

- **Ejercicio 1:** sistema experto clásico, con reglas if-then (`expertSystem.py`).
- **Ejercicio 2:** sistema experto difuso, con la librería fuzzy-expert (`fuzzyExpert.py`). Parte de la lógica del ejercicio 1.

## Archivos

Los que he escrito yo:

| Archivo | Qué es |
|---|---|
| `expertSystem.py` | Ejercicio 1: sistema experto clásico |
| `fuzzyExpert.py` | Ejercicio 2: sistema experto difuso |

Los que vienen dados por el profesor:

| Archivo | Qué es |
|---|---|
| `P1Launcher.py` | Lanza la simulación y la ventana gráfica |
| `robot.py` | El robot y su dinámica |
| `objetivo.py` | Los objetivos que tiene que recorrer el robot |
| `recorrido*.json` | Los circuitos de prueba |
| `calculaPropina.py` | Ejemplo de sistema difuso |
| `EnunciadoP1.pdf` | Enunciado de la práctica |

## Cómo ejecutarlo

Hace falta Python y estas dos librerías:

```
pip install pygame fuzzy-expert
```

Para lanzar la simulación:

```
python P1Launcher.py
```

Por defecto se usa el sistema experto. Para probar el difuso hay que cambiar esta variable al principio de `P1Launcher.py`:

```python
useFuzzySystem = True
```

Al terminar cada objetivo, el simulador imprime por la terminal la puntuación de ese tramo, y al final la puntuación total.

## Cómo funciona

Los dos ejercicios siguen la misma idea:

1. El robot va primero al primer punto del tramo (el inicio de la recta, o el punto medio del triángulo para rodearlo).
2. Cuando está cerca, cambia el destino al punto final.
3. En cada instante calcula cuánto tiene que girar para mirar al punto, y de ahí saca la velocidad lineal y la angular.

En el ejercicio 1 las reglas cambian de golpe según el error de ángulo. En el ejercicio 2 las mismas reglas cambian de forma gradual.

## Documentación

La explicación completa (evolución del trabajo, código, reglas, resultados y conclusiones) está en el PDF de la documentación de la práctica.
