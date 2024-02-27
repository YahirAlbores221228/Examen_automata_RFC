import re
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import Frame
from tkinter import messagebox

expresion_regular =re.compile(r'^[A-Za-z]{4}$')
curp_predeterminado = "ALMY"

def validarcurp(curp_ingresado):
    inicial = curp_ingresado[0].upper()
    if inicial != 'A':
        messagebox.showerror("Error", "El RFC no comienza con A: La expresion es invalida")
        return False
    
    inciales_permitidas = curp_predeterminado[1:]
    
    for letra in curp_ingresado[1:]:
        if letra.upper() not in inciales_permitidas:
            messagebox.showerror("Error", f"La letra '{letra}' no es valida, El RFC es invalida")
            return False
        
    messagebox.showinfo("Exito", "EL RFC ingresado es valido")
    return True

def generar_automata(curp_ingresado):
    G=nx.DiGraph()
    estados = ['Inicio', 'q1', 'q2', 'q3', 'Final']

    for i in range(len(estados)):
        G.add_node(estados[i], label=estados[i])
        G.add_edge('Inicio', 'q1')
        G.add_edge('q1', 'q2')
        G.add_edge('q2', 'q3')
        G.add_edge('q3', 'Final')
        
    for i in range(len(curp_ingresado)):
        G.add_edge(estados[i], estados[i + 1], label=curp_ingresado[i])
       
    pos = nx.spring_layout(G)
    labels = {estado: G.nodes[estado]['label'] for estado in G.nodes()}
    edge_labels = {(u, v): G.edges[u, v].get('label', '') for u, v in G.edges()}
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=2000, node_color='yellow', font_size=16, font_weight='bold', arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    plt.title("Automata de la CURP" + curp_ingresado, fontsize=18)
    plt.show()


def  verificar_curp():
    curp_ingresado = curp.get().strip()
    if curp_ingresado.lower() == '0':
            root.destroy()
    elif len(curp_ingresado) !=4:
        messagebox.showerror("Error", "El RFC debe tener 4 letras")
    elif validarcurp(curp_ingresado):
         generar_automata(curp_ingresado) 

  
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (width / 2))
    y_coordinate = int((screen_height / 2) - (height / 2))
    
    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

root = tk.Tk()
root.title("Verificación del RFC")

ventana = Frame(root, width=300, height=150)
ventana.pack()

label_entradas = tk.Label(ventana, text="Ingrese el RFC a verificar ('0' para salir):", fg='blue')
label_entradas.pack(pady=10)

curp = tk.Entry(ventana, width=40)
curp.pack(pady=10)

button = tk.Button(ventana, text="Realizar verificación", width=20, fg='white', bg='green', bd=0 , command=verificar_curp)
button.pack(pady=5)

center_window(root, 300, 150)

root.mainloop()