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
import numpy as np
from fuzzy_expert.variable import FuzzyVariable
from fuzzy_expert.rule import FuzzyRule
from fuzzy_expert.inference import DecompositionalInference

from objetivo import *

class FuzzySystem:
    def __init__(self) -> None:
        self.objetivoActual = None
        self.estado_inicio = True  # Para controlar los waypoints (inicio vs fin / medio)

        # 1. DEFINICIÓN DE VARIABLES DIFUSAS
        self.variables = {
            "error_angulo": FuzzyVariable(
                universe_range=(-180, 180),
                terms={
                    "Mucho_Izquierda": [(-180, 1), (-180, 1), (-45, 1), (-15, 0)],
                    "Poco_Izquierda": [(-30, 0), (-15, 1), (-2, 0)],
                    "Alineado": [(-10, 0), (0, 1), (10, 0)],
                    "Poco_Derecha": [(2, 0), (15, 1), (30, 0)],
                    "Mucho_Derecha": [(15, 0), (45, 1), (180, 1), (180, 1)],
                }
            ),
            "distancia": FuzzyVariable(
                universe_range=(0, 50),
                terms={
                    "Muy_Cerca": [(0, 1), (0, 1), (1, 1), (3, 0)],
                    "Cerca": [(2, 0), (5, 1), (10, 0)],
                    "Lejos": [(8, 0), (15, 1), (50, 1)],
                }
            ),
            "v_lineal": FuzzyVariable(
                universe_range=(0, 3),
                terms={
                    "Lenta": [(0, 1), (0.5, 1), (1.2, 0)],
                    "Media": [(0.8, 0), (1.8, 1), (2.2, 0)],
                    "Rapida": [(1.8, 0), (2.5, 1), (3.0, 1)],
                }
            ),
            "v_angular": FuzzyVariable(
                universe_range=(-1.0, 1.0),
                terms={
                    "Giro_Izquierda_Fuerte": [(-1.0, 1), (-0.8, 1), (-0.4, 0)],
                    "Giro_Izquierda_Suave": [(-0.5, 0), (-0.25, 1), (0, 0)],
                    "Recto": [(-0.1, 0), (0, 1), (0.1, 0)],
                    "Giro_Derecha_Suave": [(0, 0), (0.25, 1), (0.5, 0)],
                    "Giro_Derecha_Fuerte": [(0.4, 0), (0.8, 1), (1.0, 1)],
                }
            )
        }

        # 2. ESPECIFICACIÓN DE REGLAS DIFUSAS
        self.reglas = [
            # Reglas de alineación y dirección
            FuzzyRule(
                premise=[("error_angulo", "Alineado")],
                consequence=[("v_angular", "Recto"), ("v_lineal", "Rapida")]
            ),
            FuzzyRule(
                premise=[("error_angulo", "Mucho_Derecha")],
                consequence=[("v_angular", "Giro_Derecha_Fuerte"), ("v_lineal", "Lenta")]
            ),
            FuzzyRule(
                premise=[("error_angulo", "Poco_Derecha")],
                consequence=[("v_angular", "Giro_Derecha_Suave"), ("v_lineal", "Media")]
            ),
            FuzzyRule(
                premise=[("error_angulo", "Mucho_Izquierda")],
                consequence=[("v_angular", "Giro_Izquierda_Fuerte"), ("v_lineal", "Lenta")]
            ),
            FuzzyRule(
                premise=[("error_angulo", "Poco_Izquierda")],
                consequence=[("v_angular", "Giro_Izquierda_Suave"), ("v_lineal", "Media")]
            ),
            # Regla de frenado al aproximarse al objetivo
            FuzzyRule(
                premise=[("distancia", "Muy_Cerca")],
                consequence=[("v_lineal", "Lenta")]
            )
        ]

        # 3. MOTOR DE INFERENCIA
        self.modelo = DecompositionalInference(
            and_operator="min",
            or_operator="max",
            implication_operator="Rc",
            composition_operator="max-min",
            production_link="max",
            defuzzification_operator="cog",
        )

    def setObjetivo(self, obj):
        self.objetivoActual = obj
        self.estado_inicio = True

    def tomarDecision(self, poseRobot):
        xrobot, yrobot, orientacion = poseRobot[0], poseRobot[1], poseRobot[2]

        # Determinar el punto objetivo según el tipo y fase del recorrido
        if self.objetivoActual.getType() == 1:  # Segmento
            if self.estado_inicio:
                target = self.objetivoActual.getInicio()
            else:
                target = self.objetivoActual.getFin()
        else:  # Triángulo
            if self.estado_inicio:
                target = self.objetivoActual.getMedio()
            else:
                target = self.objetivoActual.getFin()

        # Cálculo de distancias y errores angulares
        difx = target[0] - xrobot
        dify = target[1] - yrobot
        distancia_obj = math.hypot(difx, dify)

        # Transición de estado si está suficientemente cerca del waypoint intermedio
        if self.estado_inicio and distancia_obj < 2.0:
            self.estado_inicio = False

        angulo_objetivo = math.degrees(math.atan2(dify, difx))
        error_ang = angulo_objetivo - orientacion

        # Normalizar el error angular al rango [-180, 180]
        while error_ang > 180:
            error_ang -= 360
        while error_ang < -180:
            error_ang += 360

        # Inferencia difusa mediante la librería
        resultado, _ = self.modelo(
            variables=self.variables,
            rules=self.reglas,
            error_angulo=error_ang,
            distancia=distancia_obj,
        )

        # Extracción de valores desdifusificados
        V = resultado.get("v_lineal", 0.0)
        W = resultado.get("v_angular", 0.0)

        return (V, W)