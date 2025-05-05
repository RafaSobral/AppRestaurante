import tkinter as tk
from classes import Cliente, Prato, Pedido, Acompanhamento, Caixa


janela = tk.Tk()
janela.title("Bom Apetite")
janela.geometry("1440x960")

app_Cliente = Cliente() 
app_Prato = Prato()
app_Pedido = Pedido()
app_Acompanhamentos = Acompanhamento()
app_Caixa = Caixa()

botao_cadastrarCliente = tk.Button(janela, text="Cadastrar Cliente(1)", command = app_Cliente.abrir_cadastrarCliente)
botao_cadastrarCliente.grid(row = 0, column= 0)
def acionar_cadastrar_cliente(event=None):
    botao_cadastrarCliente.invoke()
janela.bind("1", acionar_cadastrar_cliente)


botao_gerenciarClientes = tk.Button(janela, text="Gerenciar Clientes(5)", command=app_Cliente.abrir_gerenciarClientes)
botao_gerenciarClientes.grid(row=0,column=2)
def acionar_gerenciar_cliente(event=None):
    botao_gerenciarClientes.invoke()
janela.bind("5", acionar_gerenciar_cliente)


botao_cadastrarPratos = tk.Button(janela, text="Cadastrar Pratos(2)", command=app_Prato.abrir_cadastrarPratos)
botao_cadastrarPratos.grid(row=1,column=0)
def acionar_cadastrar_pratos(event=None):
    botao_cadastrarPratos.invoke()
janela.bind("2", acionar_cadastrar_pratos)

botao_gerenciarPratos = tk.Button(janela, text="Gerenciar Pratos(6)", command=app_Prato.abrir_gerenciarPratos)
botao_gerenciarPratos.grid(row=1,column=2)
def acionar_gerenciar_pratos(event=None):
    botao_gerenciarPratos.invoke()
janela.bind("6", acionar_gerenciar_pratos)

botao_cadastrarAcompanhamentos = tk.Button(janela, text="Cadastrar Acomp(3)", command=app_Acompanhamentos.abrir_cadastrarAcompanhamentos)
botao_cadastrarAcompanhamentos.grid(row=2,column=0)
def acionar_cadastrar_acomp(event=None):
    botao_cadastrarAcompanhamentos.invoke()
janela.bind("3", acionar_cadastrar_acomp)

botao_gerenciarAcompanhamentos = tk.Button(janela, text="Gerenciar Acomp(7)", command=app_Acompanhamentos.abrir_gerenciarAcompanhamentos)
botao_gerenciarAcompanhamentos.grid(row=2,column=2)
def acionar_gerenciar_acomp(event=None):
    botao_gerenciarAcompanhamentos.invoke()
janela.bind("7", acionar_gerenciar_acomp)

botao_cadastrarPedidos = tk.Button(janela, text="Cadastrar Pedidos(4)", command=app_Pedido.abrir_cadastrarPedido)
botao_cadastrarPedidos.grid(row=3,column=0)
def acionar_cadastrar_pedidos(event=None):
    botao_cadastrarPedidos.invoke()
janela.bind("4", acionar_cadastrar_pedidos)


botao_gerenciarPedidos = tk.Button(janela, text="Gerenciar Pedidos(8)", command=app_Pedido.abrir_gerenciarPedidos)
botao_gerenciarPedidos.grid(row=3,column=2)
def acionar_gerenciar_pedido(event=None):
    botao_gerenciarPedidos.invoke()
janela.bind("8", acionar_gerenciar_pedido)

botao_fecharCaixa = tk.Button(janela, text="Fechar Caixa(9)", command=app_Caixa.abrir_fecharCaixa)
botao_fecharCaixa.grid(row=8,column=0)
def acionar_fechar_caixa(event=None):
    botao_fecharCaixa.invoke()
janela.bind("9", acionar_fechar_caixa)




janela.mainloop()
