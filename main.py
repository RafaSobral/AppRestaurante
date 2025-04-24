import tkinter as tk
from classes import Cliente, Prato


janela = tk.Tk()
janela.title("Bom Apetite")
janela.geometry("700x500")

app_Cliente = Cliente()
app_Prato = Prato()

botao_cadastrar = tk.Button(janela, text="Cadastrar Cliente", command = app_Cliente.abrir_cadastrarCliente)
botao_cadastrar.grid(row = 0, column= 0)

botao_visualizarClientes = tk.Button(janela, text="Visualizar Clientes", command = app_Cliente.abrir_visualizarClientes)
botao_visualizarClientes.grid(row = 1, column= 0)

botao_cadastrarPratos = tk.Button(janela, text="Cadastrar Pratos", command=app_Prato.abrir_cadastrarPratos)
botao_cadastrarPratos.grid(row=2,column=0)

botao_visualizarPratos = tk.Button(janela, text="Visualizar Pratos", command=app_Prato.abrir_visualizarPratos)
botao_visualizarPratos.grid(row=3,column=0)


janela.mainloop()
