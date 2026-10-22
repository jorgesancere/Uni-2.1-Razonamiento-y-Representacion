'''
' Creado por Diego Viejo 
' El 6/10/2026
'
' Ejemplo de sistema experto difuso para calcular la propina a dejar en función de la calidad de la comida y del servicio recibido
'''
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider  # Importamos el slider nativo
from fuzzy_expert.variable import FuzzyVariable
from fuzzy_expert.rule import FuzzyRule
from fuzzy_expert.inference import DecompositionalInference

#Especificamos las variables difusas y sus términos lingüísticos
variables = {
    "calidad_comida": FuzzyVariable(
        universe_range=(0, 10),
        terms={
            "Rancia": [(0, 1), (1, 1), (3, 0)],
            "Deliciosa": [(7, 0), (9, 1)],
        }
    ),
    "calidad_servicio": FuzzyVariable(
        universe_range=(0, 10),
        terms={
            "Pobre": ('zmf', 1, 4),
            "Buena": ('gaussmf', 5, 1.5),
            "Excelente": ('smf', 6, 9),
        }
    ),
    "propina": FuzzyVariable(
        universe_range=(0, 30), 
        terms={
            "Tacaña": [(0, 1), (5, 1), (10, 0)],
            "Promedio": [(5, 0), (15, 1), (25, 0)],
            "Generosa": [(20, 0), (25, 1), (30, 0)],
        }
    ),
}   

#Especificamos las reglas del sistema experto difuso
reglas = {
    FuzzyRule(
        premise=[
            ("calidad_comida", "Rancia"),
            ("OR", "calidad_servicio", "Pobre")
        ],
        consequence=[
            ("propina", "Tacaña")
        ]
    ),
    FuzzyRule(
        premise=[
            ("calidad_servicio", "Buena")
        ],
        consequence=[
            ("propina", "Promedio")
        ]
    ),
    FuzzyRule(
        premise=[
            ("calidad_servicio", "Excelente"),
            ("OR", "calidad_comida", "Deliciosa")
        ],
        consequence=[
            ("propina", "Generosa")
        ]
    )
}


#Especificamos el motor de inferencia difusa con las funciones de agregación y defuzzificación
modeloPropina = DecompositionalInference(
    and_operator="min",
    or_operator="max",
    implication_operator="Rc",
    composition_operator="max-min",
    production_link="max",
    defuzzification_operator="cog",
)

comida = 8
servicio = 3

resultado, _ = modeloPropina(
    variables=variables,
    rules=reglas,
    calidad_comida=comida,
    calidad_servicio=servicio,
)

print('La propina recomendada para comida: {} y servicio: {}, es: {}'.format(comida, servicio, resultado.get("propina")))

#Mostramos una gráfica con los resultados del sistema experto difuso
plt.figure(figsize=(10,6))
modeloPropina.plot(
    variables=variables,
    rules=reglas,
    calidad_comida=comida,
    calidad_servicio=servicio,
)

plt.show()
