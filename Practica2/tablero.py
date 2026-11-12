FILAS = 9
COLS = 9

class Tablero:
    def __init__(self):
        self.tablero = []

        for i in range(FILAS):
            self.tablero.append([])
            for j in range(COLS):
                self.tablero[i].append(0)

    def limpiarTablero(self):
        for fila in range(FILAS):
            for col in range(COLS):
                self.tablero[fila][col] = 0
    
    def getCasilla(self, fila, col):
        return self.tablero[fila][col]
    
    def setCasilla(self, fila, col, valor):
        self.tablero[fila][col] = valor
    
    def leeStringFichero(self, text):
        pos = 0
        for fila in range(FILAS):
            for col in range(COLS):
                self.tablero[fila][col] = int(text[pos])
                pos = pos+2

    def esTableroVacio(self):
        vacio = True

        for fila in range(FILAS):
            for col in range(COLS):
                if self.tablero[fila][col] != 0:
                    vacio = False
                    break
            if vacio!=True:
                break
        
        return vacio
    
    def esTableroCompleto(self):
        completo = True

        for fila in range(FILAS):
            for col in range(COLS):
                if self.tablero[fila][col] == 0:
                    completo = False
                    break
            if not completo:
                break
        return completo
    
    
    def estaEnFila(self, fila, col, casillaActual):
        ret = False
        for iter in range(COLS):
            if iter!=col and self.tablero[fila][iter]==casillaActual:
                ret = True
                break
        return ret
    
    def estaEnCol(self, fila, col, casillaActual):
        ret = False
        for iter in range(FILAS):
            if iter != fila and self.tablero[iter][col]==casillaActual:
                ret = True
                break
        return ret
    
    def estaEnMiniTablero(self, fila, col, casillaActual):
        ret = False
        stride = 3
        filaTablero = int(int(fila)/3) * stride
        colTablero = int(int(col)/3) * stride

        for it_fila in range(stride):
            for it_col in range(stride):
                if filaTablero+it_fila != fila and colTablero+it_col != col and self.tablero[filaTablero+it_fila][colTablero+it_col]==casillaActual:
                    ret = True
        return ret

    def esTableroCorrecto(self):
        correcto = True

        for fila in range(FILAS):
            for col in range(COLS):
                casilla = self.tablero[fila][col]
                if casilla!=0:
                    correcto = not(self.estaEnFila(fila, col, casilla) or self.estaEnCol(fila, col, casilla) or
                        self.estaEnMiniTablero(fila, col, casilla))
                if not correcto:
                    return False
        return correcto
    




    

