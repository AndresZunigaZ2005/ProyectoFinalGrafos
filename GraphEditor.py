import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class Grafo:
    def __init__(self):
        self.grafo = nx.Graph()
        
    def agregar_nodo(self, nodo):
        if nodo:
            self.grafo.add_node(nodo)
        else:
            messagebox.showerror("Error", "Debe ingresar un nombre para el nodo.")

    def eliminar_nodo(self, nodo):
        if nodo in self.grafo.nodes:
            self.grafo.remove_node(nodo)
        else:
            messagebox.showerror("Error", "El nodo no existe en el grafo.")

    def agregar_arista(self, inicio, fin, nombre):
        if inicio in self.grafo.nodes and fin in self.grafo.nodes:
            if not nombre:
                messagebox.showerror("Error", "Debe ingresar un nombre para la arista.")
            else:
                self.grafo.add_edge(inicio, fin, name=nombre)
        else:
            messagebox.showerror("Error", "Ambos nodos deben existir en el grafo.")

    def eliminar_arista(self, inicio, fin):
        if inicio in self.grafo.nodes and fin in self.grafo.nodes:
            if self.grafo.has_edge(inicio, fin):
                self.grafo.remove_edge(inicio, fin)
            else:
                messagebox.showerror("Error", "La arista no existe en el grafo.")
        else:
            messagebox.showerror("Error", "Ambos nodos deben existir en el grafo.")

    def matriz_adyacencia(self):
        nodos = sorted(list(self.grafo.nodes))
        matriz = nx.adjacency_matrix(self.grafo, nodelist=nodos).todense()
        return matriz, nodos

    def matriz_incidencia(self):
        nodos = sorted(list(self.grafo.nodes))
        aristas = sorted(list(self.grafo.edges))
        matriz = nx.incidence_matrix(self.grafo, nodelist=nodos, edgelist=aristas, oriented=True).todense()
        return matriz, aristas, nodos

    def elevar_matriz_adyacencia(self, grado):
        matriz, nodos = self.matriz_adyacencia()
        matriz_elevada = np.linalg.matrix_power(matriz, grado)
        return matriz_elevada

class InterfazGrafica:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Grafo")

        self.grafo = Grafo()

        self.frame_grafo = tk.Frame(ventana)
        self.frame_grafo.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.frame_grafo.grid_rowconfigure(0, weight=1)
        self.frame_grafo.grid_columnconfigure(0, weight=1)

        self.figura_grafo = plt.figure(figsize=(5, 4))
        self.ax = self.figura_grafo.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figura_grafo, master=self.frame_grafo)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Frame para controles de nodos y aristas
        self.frame_controles_nodos_aristas = tk.Frame(ventana, bd=2, relief=tk.SOLID)
        self.frame_controles_nodos_aristas.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_controles_nodos_aristas.grid_rowconfigure(0, weight=1)
        self.frame_controles_nodos_aristas.grid_columnconfigure(0, weight=1)

        ttk.Label(self.frame_controles_nodos_aristas, text="Nodo:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nodo = ttk.Entry(self.frame_controles_nodos_aristas)
        self.entry_nodo.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.frame_controles_nodos_aristas, text="Agregar Nodo", command=self.agregar_nodo).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(self.frame_controles_nodos_aristas, text="Eliminar Nodo", command=self.eliminar_nodo).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(self.frame_controles_nodos_aristas, text="Inicio:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_inicio = ttk.Entry(self.frame_controles_nodos_aristas)
        self.entry_inicio.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self.frame_controles_nodos_aristas, text="Fin:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_fin = ttk.Entry(self.frame_controles_nodos_aristas)
        self.entry_fin.grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(self.frame_controles_nodos_aristas, text="Nombre (obligatorio):").grid(row=3, column=0, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(self.frame_controles_nodos_aristas)
        self.entry_nombre.grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(self.frame_controles_nodos_aristas, text="Agregar Arista", command=self.agregar_arista).grid(row=3, column=2, padx=5, pady=5)
        ttk.Button(self.frame_controles_nodos_aristas, text="Eliminar Arista", command=self.eliminar_arista).grid(row=3, column=3, padx=5, pady=5)

        # Frame para controles de matrices
        self.frame_controles_matrices = tk.Frame(ventana, bd=2, relief=tk.SOLID)
        self.frame_controles_matrices.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.frame_controles_matrices.grid_rowconfigure(0, weight=1)
        self.frame_controles_matrices.grid_columnconfigure(0, weight=1)

        ttk.Button(self.frame_controles_matrices, text="Mostrar Matriz de Adyacencia", command=self.mostrar_matriz_adyacencia).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(self.frame_controles_matrices, text="Mostrar Matriz de Incidencia", command=self.mostrar_matriz_incidencia).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Nuevo grupo de controles con un rectángulo negro
        self.frame_controles_adicionales = tk.Frame(ventana, bd=2, relief=tk.SOLID)
        self.frame_controles_adicionales.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_controles_adicionales.grid_rowconfigure(0, weight=1)
        self.frame_controles_adicionales.grid_columnconfigure(0, weight=1)

        ttk.Label(self.frame_controles_adicionales, text="Elevar matriz de adyacencia al grado:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_grado = ttk.Entry(self.frame_controles_adicionales)
        self.entry_grado.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.frame_controles_adicionales, text="Generar cantidad caminos", command=self.generar_caminos).grid(row=0, column=2, padx=5, pady=5)

        ventana.grid_rowconfigure(0, weight=1)
        ventana.grid_rowconfigure(1, weight=0)
        ventana.grid_columnconfigure(0, weight=1)
        ventana.grid_columnconfigure(1, weight=0)

    def agregar_nodo(self):
        nodo = self.entry_nodo.get()
        self.grafo.agregar_nodo(nodo)

    def eliminar_nodo(self):
        nodo = self.entry_nodo.get()
        self.grafo.eliminar_nodo(nodo)

    def agregar_arista(self):
        inicio = self.entry_inicio.get()
        fin = self.entry_fin.get()
        nombre = self.entry_nombre.get() if self.entry_nombre.get() else None
        self.grafo.agregar_arista(inicio, fin, nombre)

    def eliminar_arista(self):
        inicio = self.entry_inicio.get()
        fin = self.entry_fin.get()
        self.grafo.eliminar_arista(inicio, fin)

    def mostrar_matriz_adyacencia(self):
        matriz, nodos = self.grafo.matriz_adyacencia()
        texto_matriz = "Matriz de Adyacencia:\n\n"
        texto_matriz += "  " + "  ".join(nodos) + "\n"
        for i in range(len(nodos)):
            texto_matriz += nodos[i] + " " + " ".join(map(str, matriz[i].tolist()[0])) + "\n"
        messagebox.showinfo("Matriz de Adyacencia", texto_matriz)

    def mostrar_matriz_incidencia(self):
        matriz, aristas, nodos = self.grafo.matriz_incidencia()
        texto_matriz = "Matriz de Incidencia:\n\n"
        texto_matriz += "  " + "  ".join(nodos) + "\n"
        for i in range(len(aristas)):
            texto_matriz += aristas[i] + " " + " ".join(map(str, matriz[i].tolist()[0])) + "\n"
        messagebox.showinfo("Matriz de Incidencia", texto_matriz)

    def generar_caminos(self):
        grado = int(self.entry_grado.get())
        matriz_elevada = self.grafo.elevar_matriz_adyacencia(grado)
        texto_matriz_elevada = "Matriz elevada a la potencia {}:\n\n".format(grado)
        for fila in matriz_elevada:
            texto_matriz_elevada += " ".join(map(str, fila)) + "\n"
        messagebox.showinfo("Matriz Elevada", texto_matriz_elevada)


def main():
    ventana = tk.Tk()
    app = InterfazGrafica(ventana)
    ventana.mainloop()

if __name__ == "__main__":
    main()
