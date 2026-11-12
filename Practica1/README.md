# Razonamiento y Representación del Conocimiento

Práctica 1: Sistemas Expertos

Jorge Sánchez Cerezo, Universidad de Alicante

## Introducción

En esta práctica hay que controlar un robot móvil que se mueve por un plano sin obstáculos. Lo único que sabemos del robot es su posición y hacia dónde mira, y lo único que podemos hacer es darle una velocidad lineal y una velocidad angular. Con eso, el robot tiene que recorrer un circuito lo más pegado posible al camino y tardando lo menos posible. Cuanto mejor lo haga, más puntuación le da el simulador.

El circuito está formado por tramos de dos tipos: segmentos rectos y triángulos, que el robot tiene que rodear sin entrar dentro.

La práctica tiene dos ejercicios que resuelven el mismo problema de dos formas distintas:

- **Ejercicio 1:** un sistema experto clásico, con reglas if-then.
- **Ejercicio 2:** un sistema experto difuso, con reglas difusas. Lo hice a partir del ejercicio 1, pasando sus reglas y sus valores al sistema difuso.

## Documentación

Todo el trabajo está explicado en la memoria de la práctica (el PDF): cómo fue evolucionando cada ejercicio, qué hace el código, las reglas que he usado, los resultados y las conclusiones.
