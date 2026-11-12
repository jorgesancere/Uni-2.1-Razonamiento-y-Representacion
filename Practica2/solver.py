from tablero import *

class Solver:
    def __init__(self) -> None:
        self.numBackJumps = 0
        self.calcularDominios = True
        return
    
    def notificarFicheroCargado(self):
        self.calcularDominios = True
        return
    
    def ejecutarBackTracking(self, tablero):
        self.numBackJumps = 0


        ### Elimina la siguiente instrucción añade aquí tu código para backTracking
        print("BackTracking: Función no implementada")

        ### Es una buena idea mostrar el número de saltos atrás que hace backtracking
        text ="BackTracking: {} saltos atrás" 
        print(text.format(self.numBackJumps))
        return

    def ejecutarAC3(self, tablero):
        ### Elimina la siguiente instrucción añade aquí tu código para AC3
        print("AC3: Función no implementada")
        return

    def ejecutarForwardChecking(self, tablero):

        ### Elimina la siguiente instrucción añade aquí tu código para forwardChecking
        print("ForwardChecking: Función no implementada")
        return
    
