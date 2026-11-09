'''
 Sistema Experto Difuso para el guiado de un robot
 Esta clase contendrá el código creado por los alumnos de RyRDC para el control 
 y guiado de un robot móvil sobre un plano cartesiano para recorrer diferentes 
 objetivos utilizando un esquema de sistema experto difuso

 Creado por: Diego Viejo
 el 24/10/2024
 Modificado por: Diego Viejo. 

'''
import math

from fuzzy_expert.variable import FuzzyVariable
from fuzzy_expert.rule import FuzzyRule
from fuzzy_expert.inference import DecompositionalInference

from objetivo import *


class FuzzySystem:
    def __init__(self) -> None:
        self.objetivoActual = None
        # Igual que en el sistema experto:
        # True: el robot va hacia el primer punto del tramo (el inicio de la recta o el punto medio del triángulo)
        # False: el robot ya va hacia el punto final
        self.estado_inicio = True
        # True solo al principio de todo, para controlar el arranque del primer objetivo
        self.primer_objetivo_global = True

        # 1. VARIABLES DIFUSAS
        # Los conjuntos del error angular salen de los rangos del sistema experto:
        #   alineado (menos de 0.5°), pequeño (hasta 10°), medio (de 12° a 14°) y grande (a partir de 16°)
        # Entre un rango y otro el cambio es gradual, no de golpe como en el sistema experto.
        # Positivo = el punto está a la izquierda del robot, negativo = a la derecha
        
        self.variables = {
            "error_angulo": FuzzyVariable(
                universe_range=(-180, 180),
                terms={
                    "Izq_Grande":  [(14, 0), (16, 1), (180, 1)],
                    "Izq_Media":   [(10, 0), (12, 1), (14, 1), (16, 0)],
                    "Izq_Pequena": [(0, 0), (0.5, 1), (10, 1), (12, 0)],
                    "Alineado":    [(-0.5, 0), (0, 1), (0.5, 0)],
                    "Der_Pequena": [(-12, 0), (-10, 1), (-0.5, 1), (0, 0)],
                    "Der_Media":   [(-16, 0), (-14, 1), (-12, 1), (-10, 0)],
                    "Der_Grande":  [(-180, 1), (-16, 1), (-14, 0)],
                }
            ),
            # Vale 1 solo durante el arranque del primer objetivo (como primer_objetivo_global en el sistema experto)
            "arranque": FuzzyVariable(
                universe_range=(0, 1),
                terms={
                    "No": [(0, 1), (1, 0)],
                    "Si": [(0, 0), (1, 1)],
                }
            ),
            # Los valores de V y W son los mismos que usa el sistema experto
            "v_lineal": FuzzyVariable(
                universe_range=(0, 3.5),
                terms={
                    "Arranque": [(0.5, 0), (1.0, 1), (1.5, 0)],
                    "Lenta":    [(1.5, 0), (2.0, 1), (2.5, 0)],
                    "Media":    [(2.0, 0), (2.5, 1), (3.0, 0)],
                    "Rapida":   [(2.5, 0), (3.0, 1), (3.5, 0)],
                }
            ),
            "v_angular": FuzzyVariable(
                universe_range=(-0.8, 0.8),
                terms={
                    "Der_Fuerte": [(-0.6, 0), (-0.5, 1), (-0.4, 0)],
                    "Der_Media":  [(-0.4, 0), (-0.3, 1), (-0.2, 0)],
                    "Der_Suave":  [(-0.2, 0), (-0.1, 1), (0.0, 0)],
                    "Recto":      [(-0.1, 0), (0.0, 1), (0.1, 0)],
                    "Izq_Suave":  [(0.0, 0), (0.1, 1), (0.2, 0)],
                    "Izq_Media":  [(0.2, 0), (0.3, 1), (0.4, 0)],
                    "Izq_Fuerte": [(0.4, 0), (0.5, 1), (0.6, 0)],
                }
            ),
        }

        # 2. REGLAS DIFUSAS
        # Son las mismas reglas que iraobjetivo (G1 a G5), pero cada una se aplica "un poco" según lo cerca que esté el error de cada conjunto
        giros = [
            ("Izq_Grande", "Izq_Fuerte"),
            ("Izq_Media", "Izq_Media"),
            ("Izq_Pequena", "Izq_Suave"),
            ("Alineado", "Recto"),
            ("Der_Pequena", "Der_Suave"),
            ("Der_Media", "Der_Media"),
            ("Der_Grande", "Der_Fuerte"),
        ]
        velocidades = [
            ("Izq_Grande", "Lenta"),
            ("Izq_Media", "Media"),
            ("Izq_Pequena", "Rapida"),
            ("Alineado", "Rapida"),
            ("Der_Pequena", "Rapida"),
            ("Der_Media", "Media"),
            ("Der_Grande", "Lenta"),
        ]
        # Reglas de dirección: cuanto más error, más fuerte se gira
        self.reglas = [
            FuzzyRule(
                premise=[("error_angulo", error)],
                consequence=[("v_angular", giro)]
            )
            for error, giro in giros
        ]
        # Reglas de velocidad (fuera del arranque): cuanto más error, menos velocidad
        self.reglas += [
            FuzzyRule(
                premise=[("error_angulo", error), ("AND", "arranque", "No")],
                consequence=[("v_lineal", vel)]
            )
            for error, vel in velocidades
        ]
        # Regla del arranque (A1 y A2): en el arranque del primer objetivo se va a 1 m/s
        self.reglas.append(
            FuzzyRule(
                premise=[("arranque", "Si")],
                consequence=[("v_lineal", "Arranque")]
            )
        )

        # 3. MOTOR DE INFERENCIA
        self.modelo = DecompositionalInference(
            and_operator="min",
            or_operator="max",
            implication_operator="Rc",
            composition_operator="max-min",
            production_link="max",
            defuzzification_operator="cog",
        )

    # función setObjetivo
    #   Guarda el objetivo y pone estado_inicio a True, igual que en el sistema experto
    def setObjetivo(self, obj):
        self.objetivoActual = obj
        self.estado_inicio = True

    def tomarDecision(self, poseRobot):
        V = W = 0

        # Si todavía no hay objetivo, el robot se queda parado
        if self.objetivoActual is None:
            return (V, W)

        xrobot, yrobot, orientacion = poseRobot[0], poseRobot[1], poseRobot[2]

        # Punto al que vamos: igual que en el sistema experto
        if self.objetivoActual.getType() == 1:
            punto = self.objetivoActual.getInicio() if self.estado_inicio else self.objetivoActual.getFin()
        else:
            punto = self.objetivoActual.getMedio() if self.estado_inicio else self.objetivoActual.getFin()

        # Distancia (suma de |difx| y |dify|, como en el sistema experto) y error de ángulo
        difx = punto[0] - xrobot
        dify = punto[1] - yrobot
        distancia = abs(difx) + abs(dify)
        error_ang = math.degrees(math.atan2(dify, difx)) - orientacion
        while error_ang > 180:
            error_ang -= 360
        while error_ang < -180:
            error_ang += 360

        # Control de estados: es la misma lógica que tiene iraobjetivo, solo que aquí no cambia
        # la velocidad directamente, sino la variable "arranque" que usa el sistema difuso
        arranque = 0
        if self.primer_objetivo_global:
            if distancia <= 3.5:
                self.estado_inicio = False
            if self.estado_inicio:
                if distancia <= 5:
                    arranque = 1
            else:
                if abs(error_ang) > 10:
                    arranque = 1
                else:
                    self.primer_objetivo_global = False

        # Cambio de destino cuando estamos a 2 o menos del primer punto del tramo
        if distancia <= 2 and self.estado_inicio:
            self.estado_inicio = False

        # Uso el modelo difuso para obtener V y W
        resultado, _ = self.modelo(
            variables=self.variables,
            rules=self.reglas,
            error_angulo=error_ang,
            arranque=arranque,
        )
        V = resultado.get("v_lineal", 0.0)
        W = resultado.get("v_angular", 0.0)
        return (V, W)
