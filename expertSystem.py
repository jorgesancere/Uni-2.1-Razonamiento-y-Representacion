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
        
        
        
        #True: el robot va hacia el primer punto del tramo (el inicio de la racta o el punto medio del triángulo)
        # False: el robot ya va hacia el punto final
        self.estado_inicio = True


        # True solo al principio de todo. Sirve para controlar el arranque del primer objetivo (pq hay angulos que no pilla, entonces vamos con cuidadito para evitar problemas)
        # Cuando se alinea pasa a False y ya no se vuelve a usar
        self.primer_objetivo_global = True 

    #Guarda en objetivoActual el objetivo al que tiene que moverse el robot.
    #También pone estado_inicio a True, así en cada objetivo nuevo el robot va primero
    def setObjetivo(self, objetivo):
        self.objetivoActual = objetivo
        self.estado_inicio = True

    #   Recibe la diferencia en X y en Y entre el robot y un punto, y devuelve el ángulo
    #   Paso el anguo a grados
    def funcionangulo(self, difx, dify):


        # Uso trigonometría basica: tan(angulo) = dify / difx, o sea: angulo = arctan(dify / difx).
        # Tengo que usar atan2 porque tiene en cuenta los signos de dify y difx y funciona hacia cualquier lado
        angulo = math.atan2(dify, difx) # Sale en radianes

        # Lo pasamos a grados porque la orientación del robot también está en grados
        angulo_objetivo = angulo * 180/math.pi
        return angulo_objetivo

    #   Saca de la pose del robot su posición (x, y) y su orientación en grados.
    def inicio(self, poseRobot):
        xrobot = poseRobot[0]
        yrobot = poseRobot[1]
        orientacion = poseRobot[2]
        return xrobot, yrobot, orientacion

    #   Devuelve el tipo del objetivo actual: 1 si es un segmento y 2 si es un triángulo
    def tipo_recorrido(self):
        tipo = self.objetivoActual.getType()
        return tipo

    # Calcula cuánto tiene que girar el robot para mirar al punto (ángulo del objetivo menos orientación)
    #  Si es positivo el punto está a la izquierda del robot y si es negativo, a la derecha
    def calculo_diferencia(self, angulo_objetivo, orientacion):
        diferencia  = angulo_objetivo - orientacion
        while diferencia > 180:
            diferencia -= 360 # Si se pasa de 180 le restamos 360 (por ejemplo, 340 pasa a ser -20)
        while diferencia < -180:
            diferencia += 360 # Si es menor de -180 le sumamos 360
        return diferencia

    # Recibe la posición de un punto y la del robot, y devuelve: la diferencia en X, la diferencia en Y
    def distancia(self, xiniobj, xrobot, yiniobj, yrobot):
        difx = xiniobj - xrobot
        dify = yiniobj - yrobot 
        distancia_objetivo = abs(difx)+abs(dify)
        angulo_objetivo = self.funcionangulo(difx, dify) # Sacamos el ángulo con la función de arriba
        return difx, dify, distancia_objetivo, angulo_objetivo


    #Recibe la distancia al punto de destino y el error de ángulo (diferencia), y devuelve x = velocidad lineal, y = velocidad angular.
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

        # Para el primer punto, 
        if self.primer_objetivo_global:
            if distancia_objetivo <= 3.5:
                self.estado_inicio = False # Asignación explícita para evitar oscilaciones

            if self.estado_inicio:
                # Antes de llegar al punto, le bajo la velocidad, y asievito problemas con inercia
                if distancia_objetivo <= 5:
                    x = 1
            else:
                # Hasta que no este alineado le limito la vel
                if abs(diferencia) > 10:
                    x = 1.0
                else:
                    self.primer_objetivo_global = False 

        #Compruebo estado según la distancia al objetivo inicial
        if distancia_objetivo <= 2 and self.estado_inicio:
            self.estado_inicio = False
            x = 0.2

        return x, y
    
    #Es la funcion que se repite constantemente, necesita los valores de x e y
    def tomarDecision(self, poseRobot):

        x , y = 0 , 0 # Empezamos con velocidad 0 por si acaso

        #Si todavía no hay objetivo, el robot se queda parado
        if self.objetivoActual is None:
            return x, y

        #Saco la posición y la orientación del robot
        xrobot, yrobot, orientacion = self.inicio(poseRobot)

        #Miramos si el tramo es un segmento (1) o un triángulo (2)
        tipo = self.tipo_recorrido()

        if tipo == 1:
            # SEGMENTO : primero el inicio y luego el final
            punto = self.objetivoActual.getInicio() if self.estado_inicio == True else self.objetivoActual.getFin()
        else:
            # TRIANGULO: primero el punto medio (para rodear el triángulo) y luego el final
            punto = self.objetivoActual.getMedio() if self.estado_inicio == True else self.objetivoActual.getFin()

        #Aqui calculo la distancia y el agnulo
        difx, dify, distancia_objetivo, angulo_objetivo = self.distancia(punto[0], xrobot, punto[1], yrobot)

        # Calculamos cuánto tiene que girar el robot
        # Angulo entre 180 y -180
        diferencia = self.calculo_diferencia(angulo_objetivo, orientacion)

        # Con eso, iraobjetivo nos da la velocidad lineal (x) y la angular (y)
        x, y = self.iraobjetivo(distancia_objetivo, diferencia)
        return x, y
