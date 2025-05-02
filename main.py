import tkinter as tk
from classes import Cliente, Prato, Pedido, Acompanhamento, Caixa


janela = tk.Tk()
janela.title("Bom Apetite")
janela.geometry("170x220")

app_Cliente = Cliente() 
app_Prato = Prato()
app_Pedido = Pedido()
app_Acompanhamentos = Acompanhamento()
app_Caixa = Caixa()

botao_cadastrar = tk.Button(janela, text="Cadastrar Cliente", command = app_Cliente.abrir_cadastrarCliente)
botao_cadastrar.grid(row = 0, column= 0)

botao_visualizarClientes = tk.Button(janela, text="Visualizar Clientes", command = app_Cliente.abrir_visualizarClientes)
botao_visualizarClientes.grid(row = 1, column= 0)

botao_cadastrarPratos = tk.Button(janela, text="Cadastrar Pratos", command=app_Prato.abrir_cadastrarPratos)
botao_cadastrarPratos.grid(row=2,column=0)

botao_visualizarPratos = tk.Button(janela, text="Visualizar Pratos", command=app_Prato.abrir_visualizarPratos)
botao_visualizarPratos.grid(row=3,column=0)

botao_cadastrarAcompanhamentos = tk.Button(janela, text="Cadastrar Acompanhamentos", command=app_Acompanhamentos.abrir_cadastrarAcompanhamentos)
botao_cadastrarAcompanhamentos.grid(row=4,column=0)

botao_visualizarAcompanhamentos = tk.Button(janela, text="Visualizar Acompanhamentos", command=app_Acompanhamentos.abrir_visualizarAcompanhamentos)
botao_visualizarAcompanhamentos.grid(row=5,column=0)

botao_cadastrarPedidos = tk.Button(janela, text="Cadastrar Pedidos", command=app_Pedido.abrir_cadastrarPedido)
botao_cadastrarPedidos.grid(row=6,column=0)

botao_visualizarPedidos = tk.Button(janela, text="Visualizar Pedidos", command=app_Pedido.abrir_visualizarPedidos)
botao_visualizarPedidos.grid(row=7,column=0)

botao_fecharCaixa = tk.Button(janela, text="Fechar Caixa", command=app_Caixa.abrir_fecharCaixa)
botao_fecharCaixa.grid(row=8,column=0)

janela.mainloop()
