import tkinter as tk
from tablero import *
from solver import *
from tkinter.filedialog import askopenfilename
from time import time

AppTittle = "RRDC P2 2026 - SuDoKu"


def open_file():

    """Open a file for editing."""

    filepath = askopenfilename(

        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]

    )

    if not filepath:

        return

    with open(filepath, mode="r", encoding="utf-8") as input_file:

        text = input_file.read()

        tablero.leeStringFichero(text)

    window.title(f"{AppTittle} - {filepath}")
    reDraw()
    solver.notificarFicheroCargado()
    lb_estado["text"] = "Estado: Sin resultado"
    return
##end open_file
    
def cleanBoard():
    tablero.limpiarTablero()
    solver.notificarFicheroCargado()
    lb_estado["text"] = "Estado: Sin resultado"
    reDraw()
    return

def runBackTracking():
    initTime = time()
    solver.ejecutarBackTracking(tablero)
    endTime = time()
    executionTime = endTime - initTime
    reDraw()
    comprobarSolucion()
    texto = "Tiempo de ejecución Backtracking: {:.3f} segundos"
    print(texto.format(executionTime))
    return

def runAC3():
    initTime = time()
    solver.ejecutarAC3(tablero)
    endTime = time()
    executionTime = endTime - initTime
    reDraw()
    comprobarSolucion()
    texto = "Tiempo de ejecución AC3: {:.3f} segundos"
    print(texto.format(executionTime))
    return

def runForwardChecking():
    initTime = time()
    solver.ejecutarForwardChecking(tablero)
    endTime = time()
    executionTime = endTime - initTime
    reDraw()
    comprobarSolucion()
    texto = "Tiempo de ejecución Forward checking: {:.3f} segundos"
    print(texto.format(executionTime))
    return
    
def reDraw():
    frm_tablero = tk.Frame(frm_left, relief=tk.RAISED, bd=2, bg="green")
    for i in range(9):
        for j in range(9):
            frame = tk.Frame(
                master=frm_tablero,
                relief=tk.RAISED,
                borderwidth=1,
                bg="white"
            )
            frame.grid(row=i, column=j, padx=2, pady=2, sticky = "nsew")
            valor = tablero.getCasilla(i, j)
            if valor!=0:
                label = tk.Label(master=frame, text=f"{valor}", bg="white")
            else:
                label = tk.Label(master=frame, text=f"  ", bg="white")
            label.pack(padx=8, pady=5)

    frm_tablero.grid(row=1, column=0, sticky="nsew")
    return
## end reDraw

def comprobarSolucion():
    if tablero.esTableroCompleto():
        if tablero.esTableroCorrecto():
            lb_estado["text"] = "Estado: completado\nSolución: Correcta"
        else:
            lb_estado["text"] = "Estado: completado\nSolución: INCORRECTA"
    else:
        lb_estado["text"] = "Estado: incompleto"
    return

window = tk.Tk()

window.title(AppTittle)

tablero = Tablero()
solver = Solver()


#botones superiores
frm_left = tk.Frame(window, relief=tk.RAISED, bd=2)

frm_buttons = tk.Frame(frm_left, relief=tk.RAISED, bd=2)


btn_open = tk.Button(frm_buttons, text="Cargar SuDoKu", command=open_file)

btn_clean = tk.Button(frm_buttons, text="Limpiar Tablero", command=cleanBoard)


btn_open.grid(row=0, column=0, sticky="ew", padx=3, pady=7)

btn_clean.grid(row=0, column=1, sticky="ew", padx=3, pady=7)


frm_buttons.grid(row=0, column=0, sticky="nsew")

#botones de acción
frm_right = tk.Frame(window, relief=tk.RAISED, bd=2)

btn_backTracking = tk.Button(frm_right, text="Back Tracking", command=runBackTracking)
btn_AC3 = tk.Button(frm_right, text="AC3", command=runAC3)
btn_FC = tk.Button(frm_right, text="Forward Checking", command=runForwardChecking)
lb_estado = tk.Label(master=frm_right, text=f"Estado: Sin resultado")

btn_backTracking.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
btn_AC3.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
btn_FC.grid(row=2, column=0, sticky="nsew", padx=2, pady=2)
lb_estado.grid(row=3, column=0, sticky="nsew", padx=2, pady=8)

frm_right.grid(row=0, column=1, sticky="nsew")
frm_left.grid(row=0, column=0, sticky="nsew")


reDraw()

window.mainloop()
