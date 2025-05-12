import sqlite3
import tkinter as tk
from tkinter import ttk
from classes.Prato import Prato
from classes.Caixa import Caixa
from classes.Pedido import Pedido
from classes.Bebidas import Bebidas
from classes.Cliente import Cliente
from classes.Acompanhamento import Acompanhamento
from utils import carregar_pedidos, deletar_pedido, editar_pedido, imprimir_pedido_daruma 

conn = sqlite3.connect("bomapetite.db")
cursor = conn.cursor()

janela = tk.Tk()
janela.title("Bom Apetite")
janela.geometry("1360x500")
janela.iconphoto(False, tk.PhotoImage(file='logo.png'))

app_Cliente = Cliente() 
app_Prato = Prato()
app_Pedido = Pedido()
app_Acompanhamentos = Acompanhamento()
app_Caixa = Caixa()
app_Bebidas = Bebidas()

tree = ttk.Treeview(
    janela,
    columns=("id", "N. Pedido:", "Nome Cliente:", "Prato:", "Acompanhamento 1:", "Acompanhamento 2:",
             "Observacao:", "Tamanho:", "Pagamento:", "Troco:", "Taxa:", "Total:", "Data:"),
    show="headings"
)

tree.heading("id", text="id")
tree.column("id", width=0, stretch=False) 

tree.heading("N. Pedido:", text="N. Pedido:")
tree.column("N. Pedido:", width=38)

tree.heading("Nome Cliente:", text="Nome Cliente:")
tree.column("Nome Cliente:", width=60)

tree.heading("Prato:", text="Prato:")
tree.column("Prato:", width=100)

tree.heading("Acompanhamento 1:", text="Acompanhamento 1:")
tree.column("Acompanhamento 1:", width=130)

tree.heading("Acompanhamento 2:", text="Acompanhamento 2:")
tree.column("Acompanhamento 2:", width=130)

tree.heading("Observacao:", text="Observacao:")
tree.column("Observacao:", width=150)

tree.heading("Tamanho:", text="Tamanho:")
tree.column("Tamanho:", width=38)

tree.heading("Pagamento:", text="Pagamento:")
tree.column("Pagamento:", width=70)

tree.heading("Troco:", text="Troco:")
tree.column("Troco:", width=38)

tree.heading("Taxa:", text="Taxa:")
tree.column("Taxa:", width=38)

tree.heading("Total:", text="Total:")
tree.column("Total:", width=38)

tree.heading("Data:", text="Data:")
tree.column("Data:", width=60)

tree.pack(fill="both", expand=True, padx=10, pady=10)

carregar_pedidos(tree, cursor)
    
frame_botoes = tk.Frame(janela)
frame_botoes.pack(fill="x", padx=10, pady=10)

botao_gerenciarClientes = tk.Button(frame_botoes, text="Gerir Clientes [1]", command=app_Cliente.abrir_gerenciarClientes)
botao_gerenciarClientes.pack(side="left", padx=5)
janela.bind("1", lambda e: botao_gerenciarClientes.invoke())

botao_gerenciarPratos = tk.Button(frame_botoes, text="Gerir Pratos [2]", command=app_Prato.abrir_gerenciarPratos)
botao_gerenciarPratos.pack(side="left", padx=5)
janela.bind("2", lambda e: botao_gerenciarPratos.invoke())

botao_gerenciarAcompanhamentos = tk.Button(frame_botoes, text="Gerir Acomp [3]", command=app_Acompanhamentos.abrir_gerenciarAcompanhamentos)
botao_gerenciarAcompanhamentos.pack(side="left", padx=5)
janela.bind("3", lambda e: botao_gerenciarAcompanhamentos.invoke())

botao_gerenciarBebidas = tk.Button(frame_botoes, text="Gerir Bebidas [4]", command=app_Bebidas.abrir_gerenciarBebidas)
botao_gerenciarBebidas.pack(side="left", padx=5)
janela.bind("4", lambda e: botao_gerenciarBebidas.invoke())

botao_cadastrarBebidas = tk.Button(frame_botoes, text="Criar Bebidas [5]", command=app_Bebidas.abrir_cadastrarBebidas)
botao_cadastrarBebidas.pack(side="left", padx=5)
janela.bind("5", lambda e: botao_cadastrarBebidas.invoke())

botao_cadastrarPedidos = tk.Button(frame_botoes, text="Criar Pedido [6]", command=app_Pedido.abrir_cadastrarPedido)
botao_cadastrarPedidos.pack(side="left", padx=5)
janela.bind("6", lambda e: botao_cadastrarPedidos.invoke())

botao_cadastrarCliente = tk.Button(frame_botoes, text="Criar Cliente [7]", command=app_Cliente.abrir_cadastrarCliente)
botao_cadastrarCliente.pack(side="left", padx=5)
janela.bind("7", lambda e: botao_cadastrarCliente.invoke())

botao_cadastrarPratos = tk.Button(frame_botoes, text="Criar Pratos [8]", command=app_Prato.abrir_cadastrarPratos)
botao_cadastrarPratos.pack(side="left", padx=5)
janela.bind("8", lambda e: botao_cadastrarPratos.invoke())

botao_cadastrarAcompanhamentos = tk.Button(frame_botoes, text="Criar Acomp [9]", command=app_Acompanhamentos.abrir_cadastrarAcompanhamentos)
botao_cadastrarAcompanhamentos.pack(side="left", padx=5)
janela.bind("9", lambda e: botao_cadastrarAcompanhamentos.invoke())

botao_atualizar = tk.Button(frame_botoes, text="Atualizar [F5]", command=lambda:carregar_pedidos(tree, cursor))
botao_atualizar.pack(side="right", pady=10)
def acionar_atualizar(_):
    botao_atualizar.invoke()
janela.bind("<F5>", acionar_atualizar)

botao_editar = tk.Button(frame_botoes, text="Editar [E]", command=lambda: editar_pedido(tree, cursor, conn))
botao_editar.pack(side="right", padx=5, pady=10)
def acionar_editar(_):
    botao_editar.invoke()
janela.bind("<Key-e>", acionar_editar)

botao_deletar = tk.Button(frame_botoes, text="Deletar [Del]",  command=lambda: deletar_pedido(tree, cursor, conn))
botao_deletar.pack(side="right", padx=5, pady=10)
def acionar_deletar(_):
    botao_deletar.invoke()
janela.bind("<Delete>", acionar_deletar)

btn_imprimir = tk.Button(frame_botoes, text="Re-imprimir [i]", command=lambda: imprimir_pedido_daruma(tree))
btn_imprimir.pack(side="right", padx=5, pady=10)
def acionar_imprimir(_):
    btn_imprimir.invoke()
janela.bind("<Key-i>", acionar_imprimir)

botao_fecharCaixa = tk.Button(frame_botoes, text="Caixa [0]", command=app_Caixa.abrir_fecharCaixa)
botao_fecharCaixa.pack(side="right", padx=5)
janela.bind("0", lambda e: botao_fecharCaixa.invoke())

janela.mainloop()
