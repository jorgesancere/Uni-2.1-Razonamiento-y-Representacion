'''
 Sistema Experto para el guiado de un robot
 Esta clase contendrá el código creado por los alumnos de RyRDC para el control 
 y guiado de un robot móvil sobre un plano cartesiano

 Creado por: Diego Viejo
 el 11/09/2026

 Modificado por: Jorge Sánchez Cerezo
 el 29/09/2026
'''


from objetivo import *
import math

class ExpertSystem:
    def __init__(self) -> None:
        self.objetivoActual = None
        self.nombreAlumno = "Jorge Sánchez Cerezo" #IMPORTANTE: Cambia el valor de esta propiedad por tu nombre completo
        self.estado_inicio = True
        self.primer_objetivo_global = True # Bandera para controlar la alineación del primer segmento

    #   función setObjetivo
    #   Almacena en la propiedad objetivoActual el objetivo al que tiene que moverse el robot
    def setObjetivo(self, objetivo):
        self.objetivoActual = objetivo
        self.estado_inicio = True

    def funcionangulo(self, difx, dify):
        #Con trigonometria básica, calculamos el angulo (tan = dify/dix): angulo = arctan dify difx
        angulo = math.atan2(dify, difx) #Como esta en radianes, vamos a pasarlo a grados
        angulo_objetivo = angulo * 180/math.pi
        return angulo_objetivo

    def inicio(self, poseRobot):
        #Asignamos variables a los datos del robot (coordenadas y angulo que mira)
        xrobot = poseRobot[0]
        yrobot = poseRobot[1]
        orientacion = poseRobot[2]
        return xrobot, yrobot, orientacion

    def tipo_recorrido(self):
        tipo = self.objetivoActual.getType()
        return tipo

    def calculo_diferencia(self, angulo_objetivo, orientacion):
        diferencia  = angulo_objetivo - orientacion
        while diferencia > 180:
            diferencia -= 360 # si ha dado mas de media vuelta en sentido horario, es decir, mas alla de los 180 grados, lo ponemos en -180, y asi lo situamos como que esta en la parte izquierda del robot (zona negativa | zona positiva) 
        while diferencia < -180:
            diferencia += 360
        return diferencia

    def distancia(self, xiniobj, xrobot, yiniobj, yrobot):
        difx = xiniobj - xrobot
        dify = yiniobj - yrobot 
        distancia_objetivo = abs(difx)+abs(dify)
        angulo_objetivo = self.funcionangulo(difx, dify) # Llamada a funcionangulo para promover el uso de funciones
        return difx, dify, distancia_objetivo, angulo_objetivo


    def iraobjetivo(self, distancia_objetivo, diferencia):
        # Giro a la DERECHA (diferencia positiva)
        if diferencia > 0.3:
            if diferencia > 15:
                x = 2
                y = 0.5
            elif diferencia > 10:
                x = 2.5
                y = 0.3
            else:
                x = 3
                y = 0.1
        # Giro a la izquierda (diferencia negativa)
        elif diferencia < -0.3:
            if diferencia < -15:
                x = 2
                y = -0.5
            elif diferencia < -10:
                x = 2.5
                y = -0.3
            else:
                x = 3
                y = -0.1
        # Alineado con el objetivo (avanza recto)
        else:
            x = 3
            y = 0

        # CONTROL DE VELOCIDAD EN DOS FASES PARA EL ARRANQUE INICIAL
        if self.primer_objetivo_global:
            if distancia_objetivo <= 3.5:
                self.estado_inicio = False # Asignación explícita para evitar oscilaciones

            if self.estado_inicio:
                # FASE 1: Aproximación a P_inicio a velocidad moderada (1.0 m/s)
                if distancia_objetivo <= 5:
                    x = 1.5
            else:
                # FASE 2: Mantener 1.0 m/s tras cruzar P_inicio hasta alinearse con la recta (< 5 grados)
                if abs(diferencia) > 10:
                    x = 1.0
                else:
                    self.primer_objetivo_global = False # Alineación completada, liberar alta velocidad

        # 2. Comprobación de estado según la distancia al objetivo inicial
        if distancia_objetivo <= 2 and self.estado_inicio:
            self.estado_inicio = False # Asignación explícita para evitar oscilaciones
            x = 0

        return x, y

    #   función tomarDecision. 
    #   Recibe una tupla de 3 valores con la pose del robot: posición X, posición Y, orientación
    #   Devuelve una tupla con la velocidad lineal y angular que se quiere dar al robot
    def tomarDecision(self, poseRobot):
        x , y = 0 , 0 #Inicializamos las variables a cero por si acaso

        if self.objetivoActual is None:
            return x, y

        #Llamamos a inicio, en el que obtenemos los datos del robot
        xrobot, yrobot, orientacion = self.inicio(poseRobot)

        #Calculamos el tipo de recorrido (1 segmento, 2 triangulo)
        tipo = self.tipo_recorrido()

        # Selección del punto objetivo activo según el tipo y el estado
        if tipo == 1:
            # SEGMENTO
            punto = self.objetivoActual.getInicio() if self.estado_inicio == True else self.objetivoActual.getFin()
        else:
            # TRIANGULO
            punto = self.objetivoActual.getMedio() if self.estado_inicio == True else self.objetivoActual.getFin()

        #Calculamos la distancia a la que estamos del punto
        difx, dify, distancia_objetivo, angulo_objetivo = self.distancia(punto[0], xrobot, punto[1], yrobot)

        #Ahora lo que queremos es calcular la diferencia
        # (Angulo objetivo le restamos nuestra orientacion, y asi obtenemos lo que debe girar nuestro robot)
        diferencia = self.calculo_diferencia(angulo_objetivo, orientacion)

        # Obtenemos las velocidades lineal (x) y angular (y)
        x, y = self.iraobjetivo(distancia_objetivo, diferencia)

        return x, y

    #NOTAS

        #Me doy cuenta dce que el angulo del robot lo imprimo en grados (orientarse (que es poseRobot[2])), por lo tanto
        #para girar en sentido horario hay que usar el menos, por lo que el angulo bueno (el ue queremos en 360), hay que pillar el resto de dividir entre 360:
        # ejemplo -- 0 grados mira hacia arriba, 180 abajo, 360 arriba otra vez, por lo que lo reseteamos a 0, pero tenemos que calcular como que el 0 esta igual de cerca del 270 que del 90, por lo que if orientacion

    #DUDAS

        # - siempre se alterna segmento, triangulo?
        #   pueden haber dos trozos separados (el circuito es todo conectado o hay saltos?)